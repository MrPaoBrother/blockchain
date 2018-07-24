# -*- coding:utf8 -*-
import os
import requests
import hashlib
import json
import binascii
from urlparse import urlparse
import settings

from collections import OrderedDict

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from block import Block
from time import time
from uuid import uuid4


def read_file(file_path):
    with open(file_path, 'rb') as fs:
        data = fs.readlines()
    return data


def write_file(file_path, data):
    with open(file_path, 'wb') as fs:
        fs.write(data)


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.node_id = str(uuid4()).replace('-', '')
        self.init_chain()
        self.block = self.get_current_block()

    def init_chain(self):
        """
        初始化区块链
        :return:
        """
        block_data = None
        if os.path.exists(settings.block_save_file):
            block_data = read_file(settings.block_save_file)
        if not block_data:
            # 不存在则创建一个
            init_block = self.create_block(0, '00')
            json_data = dict()
            json_data["block_1"] = json.loads(str(init_block))
            json_data["total"] = 1
            self.chain.append(init_block)
            self.submit_transaction(sender_address=settings.default_miner, recipient_address=self.node_id, value=settings.reward, signature="")
            return
        json_data = json.loads(block_data[0])
        total = json_data.get("total")
        for i in range(1, total+1):
            block_detail = json_data["block_%d" % i]
            block = Block(block_detail["transactions"], block_detail["height"], block_detail["pre_hash"],
                          block_detail["nonce"], block_detail["timestamp"])
            self.chain.append(block)

    def get_current_block(self):
        if self.chain:
            return self.chain[-1]
        return ""

    def register_node(self, node_url):
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def verify_transaction_signature(self, sender_address, signature, transaction):
        public_key = RSA.importKey(binascii.unhexlify(sender_address))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(transaction).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(signature))

    def update_chain(self, block):
        self.chain[-1] = block
        with open(settings.block_save_file, 'wb') as fs:
            data_upd = dict()
            for i in range(1, len(self.chain) + 1):
                data_upd["block_%d" % i] = json.loads(str(self.chain[i-1]))
            data_upd["total"] = len(self.chain)
            fs.write(json.dumps(data_upd))

    def submit_transaction(self, sender_address, recipient_address, value, signature):
        transaction = OrderedDict({'sender_address': sender_address,
                                   'recipient_address': recipient_address,
                                   'value': value})
        block = self.chain[-1]
        if sender_address == settings.default_miner:
            block.transactions.append(transaction)
        else:
            transaction_verification = self.verify_transaction_signature(sender_address, signature, transaction)
            if transaction_verification:
                block.transactions.append(transaction)
            else:
                # 为了测试无论验证成功还是失败都加入该交易
                block.transactions.append(transaction)
                # return False
        # 更新链
        self.update_chain(block)
        return True

    def create_block(self, nonce, previous_hash):
        b = Block()
        b.height = len(self.chain) + 1
        b.timestamp = time()
        b.transactions = []
        b.nonce = nonce
        b.pre_hash = previous_hash
        return b

    def hash(self, block):
        block_string = json.dumps(json.loads(str(block)), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = self.hash(last_block)
        nonce = 0
        while self.valid_proof(self.chain[-1].transactions, last_hash, nonce) is False:
            nonce += 1
        return nonce

    def valid_proof(self, transactions, last_hash, nonce, difficulty=settings.hard):
        guess = (str(transactions) + str(last_hash) + str(nonce)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty] == '0' * difficulty

    def valid_chain(self, chain):
        # 1 后一个区块的hash是否等于前一个区块的hash
        # 2 每一个区块的随机数nounce是否正确
        if not chain:
            return False
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            if block.pre_hash != self.hash(last_block):
                return False
            transactions = block.transactions[:-1]
            transaction_elements = ['sender_address', 'recipient_address', 'value']
            transactions = [OrderedDict((k, transaction[k]) for k in transaction_elements) for transaction in
                            transactions]
            if not self.valid_proof(transactions, block['previous_hash'], block['nonce'], settings.hard):
                return False
            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
        for node in neighbours:
            print('http://' + node + '/chain')
            response = requests.get('http://' + node + '/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        return False

blockchain = Blockchain()