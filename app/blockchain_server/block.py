# -*- coding:utf8 -*-
import json


class Block(object):
    def __init__(self, transactions=[], height=0, pre_hash='', nonce=0, timestamp=0):
        self.transactions = transactions
        self.height = height
        self.pre_hash = pre_hash
        self.nonce = nonce
        self.timestamp = timestamp

    def __str__(self):
        block_detail = dict(transactions=self.transactions, height=self.height,
                            pre_hash=self.pre_hash, nonce=self.nonce, timestamp=self.timestamp)
        return json.dumps(block_detail)