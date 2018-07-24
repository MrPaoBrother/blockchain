# -*- coding:utf8 -*-
import json
import settings
from blockchain import blockchain


class BlockchainServer(object):
    def __init__(self):
        self.blockchain = blockchain

    def sync_data(self):
        """
        数据同步模块
        :return:
        """
        with open(settings.block_save_file, 'rb') as fs:
            data = fs.readlines()
            if not data:
                return "no block"
            return json.loads(data[0].replace("\n", ""))

    def new_transaction(self, **values):
        """
        新交易
        :param values:
        :return:
        """
        required = ['sender_address', 'recipient_address', 'value', 'signature']
        if not all(k in values for k in required):
            return 'Missing values'
        # Create a new Transaction
        transaction_result = self.blockchain.submit_transaction(values['sender_address'], values['recipient_address'],
                                                           values['value'], values['signature'])
        if not transaction_result:
            response = {'message': 'Invalid Transaction!'}
        else:
            response = {'message': 'Transaction will be added to Block ' + str(transaction_result)}
        return response

    def get_transactions(self):
        transactions = self.blockchain.chain[-1].transactions
        response = {'transactions': transactions}
        return response

    def full_chain(self):
        # 这里暂时返回最后一个区块的数据
        response = {
            'chain': str(self.blockchain.chain),
            'length': len(self.blockchain.chain),
        }
        return response

    def mine(self):
        last_block = self.blockchain.chain[-1]
        nonce = self.blockchain.proof_of_work()
        previous_hash = self.blockchain.hash(last_block)
        block = self.blockchain.create_block(nonce, previous_hash)
        self.blockchain.chain.append(block)
        self.blockchain.submit_transaction(sender_address=settings.default_miner, recipient_address=blockchain.node_id,
                                      value=settings.reward, signature="")
        self.blockchain.update_chain(block)
        response = {
            'message': "New Block Generated",
            'block_number': block.height,
            'transactions': block.transactions,
            'nonce': block.nonce,
            'previous_hash': block.pre_hash,
        }
        return response

    def register_nodes(self, **values):
        nodes = values.get('nodes').replace(" ", "").split(',')
        if nodes is None:
            return "Error: Please supply a valid list of nodes"
        for node in nodes:
            self.blockchain.register_node(node)
        response = {
            'message': 'New nodes have been added',
            'total_nodes': [node for node in self.blockchain.nodes],
        }
        return response

    def consensus(self):
        replaced = self.blockchain.resolve_conflicts()
        if replaced:
            response = {
                'message': 'Our chain was replaced',
                'new_chain': str(self.blockchain.chain)
            }
        else:
            response = {
                'message': 'Our chain is authoritative',
                'chain': str(self.blockchain.chain)
            }
        return response

    def get_nodes(self):
        nodes = list(blockchain.nodes)
        response = {'nodes': nodes}
        return response

blockchain_server = BlockchainServer()