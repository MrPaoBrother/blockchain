# -*- coding:utf8 -*-

"""
Name: Blockchain Client
Author: power
Datetime: 2018-07-24
"""
import binascii
import json
import settings
import logging
import Crypto
import Crypto.Random
from collections import OrderedDict
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from pyutil.net import fetch_html


def read_file(file_path):
    with open(file_path, 'rb') as fs:
        data = fs.readlines()
    return data


def write_file(file_path, data):
    with open(file_path, 'wb') as fs:
        fs.write(data)


class BlockchainClient(object):
    def __init__(self, sender_addr=None, sender_priv=None, receive_addr=None, money=0):
        """
        :param sender_addr: sender address/sender public key
        :param sender_priv: sender private key
        :param receive_addr: receive address/recive public key
        :param money: how much money you trade
        """
        self.sender_addr = sender_addr
        self.sender_priv = sender_priv
        self.receive_addr = receive_addr
        self.money = money

    def dict_trade(self):
        """
        cannot contain private_key
        :return:
        """
        trade_msg = dict(sender_addr=self.sender_addr, receive_addr=self.receive_addr, money=self.money)
        return OrderedDict(trade_msg)

    def get_trade_sign(self):
        """
        user private key sign the trade
        :return:
        """
        private_key = RSA.importKey(binascii.unhexlify(self.sender_priv))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.dict_trade()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

    def build_wallet(self):
        """
        build a new wallet
        :return: private_key and public_key/your address
        """
        import os
        if os.path.exists('./wallet/wallet.json'):
            keys = read_file('./wallet/wallet.json')
            if keys:
                print "已经创建过钱包, 正在读密钥..."
                keys = json.loads(keys[0])
                return keys["priv_key"], keys["pub_key"]
        print "未创建钱包,正在自动生成..."
        random_gen = Crypto.Random.new().read
        priv_key = RSA.generate(1024, random_gen)
        pub_key = priv_key.publickey()
        priv_key = binascii.hexlify(priv_key.exportKey(format='DER')).decode('ascii')
        pub_key = binascii.hexlify(pub_key.exportKey(format='DER')).decode('ascii')
        write_file('./wallet/wallet.json', json.dumps(dict(pub_key=pub_key, priv_key=priv_key)))
        return priv_key, pub_key


    def generate_trade(self):
        """
        generate a trade
        :return: generate_msg, True/False
        """
        if self.sender_addr and self.sender_priv and self.receive_addr and self.money:
            generate_msg = dict(trade=self.dict_trade(), sign=self.get_trade_sign())
            return generate_msg, True
        return None, False

    def sync_data(self):
        api = "http://%s:%d/api/blockchain/sync_data" % (settings.host, settings.port)
        code, body = fetch_html(api)
        if code != 200:
            logging.info("code %s , cannot sync data" % str(code))
        write_file(settings.block_save_file, body)

    def mine(self):
        api = "http://%s:%d/api/blockchain/mine" % (settings.host, settings.port)
        code, body = fetch_html(api)
        if code != 200:
            logging.info("code %s , cannot sync data" % str(code))
        return body

    def register_nodes(self, nodes=None):
        api = "http://%s:%d/api/blockchain/nodes/register" % (settings.host, settings.port)
        code, body = fetch_html(api, data=json.dumps(dict(nodes=nodes)))
        if code != 200:
            print "code %s , cannot register_nodes" % str(code)
            logging.info("code %s , cannot register_nodes" % str(code))
            return None
        return body

    def full_chain(self):
        api = "http://%s:%d/api/blockchain/chain" % (settings.host, settings.port)
        code, body = fetch_html(api)
        if code != 200:
            print "code %s , cannot register_nodes" % str(code)
            logging.info("code %s , cannot get full_chain" % str(code))
            return None
        return body

    def consensus(self):
        api = "http://%s:%d/api/blockchain/nodes/resolve" % (settings.host, settings.port)
        code, body = fetch_html(api)
        if code != 200:
            print "code %s , cannot solve consensus" % str(code)
            logging.info("code %s , cannot solve consensus" % str(code))
            return None
        return body

    def new_transaction(self):
        api = "http://%s:%d/api/blockchain/new/transaction" % (settings.host, settings.port)
        data = json.dumps(dict(sender_address=self.sender_addr, recipient_address=self.receive_addr,
                    value=self.money, signature=self.get_trade_sign()))
        code, body = fetch_html(url=api, data=data)
        if code != 200:
            print "code %s , cannot solve consensus" % str(code)
            logging.info("code %s , cannot solve consensus" % str(code))
            return None
        return body

blockchain_cli = BlockchainClient()