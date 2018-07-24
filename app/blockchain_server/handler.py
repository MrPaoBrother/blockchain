# -*- coding:utf8 -*-
import json
from argparse import ArgumentParser
from flask import Flask, jsonify, request
from server import blockchain_server
import settings
import logging
logging.basicConfig(filename='../../log/%s.log' % settings.psm, level=logging.INFO)
app = Flask(__name__)


@app.route('/api/blockchain/sync_data', methods=['GET'])
def sync_data():
    response = blockchain_server.sync_data()
    return jsonify(response)


@app.route('/api/blockchain/new/transaction', methods=['POST'])
def new_transaction():
    values = request.data
    values = json.loads(values)
    response = blockchain_server.new_transaction(**values)
    return jsonify(response)


@app.route('/api/blockchain/transactions/get', methods=['GET'])
def get_transactions():
    response = blockchain_server.get_transactions()
    return jsonify(response)


@app.route('/api/blockchain/chain', methods=['GET'])
def full_chain():
    response = blockchain_server.full_chain()
    return jsonify(response)


@app.route('/api/blockchain/mine', methods=['GET'])
def mine():
    response = blockchain_server.mine()
    return jsonify(response)


@app.route('/api/blockchain/nodes/register', methods=['GET', 'POST'])
def register_nodes():
    remote_addr = request.remote_addr
    try:
        values = json.loads(request.data).get("nodes")
    except Exception as e :
        logging.info("register values empty reason: %s" % str(e))
    if not values:
        values = json.dumps(dict(nodes=remote_addr+":5000"))
    values = json.loads(values)
    response = blockchain_server.register_nodes(**values)
    return jsonify(response)


@app.route('/api/blockchain/nodes/resolve', methods=['GET'])
def consensus():
    response = blockchain_server.consensus()
    return jsonify(response)


@app.route('/api/blockchain/nodes/get', methods=['GET'])
def get_nodes():
    response = blockchain_server.get_nodes()
    return jsonify(response)


def init_args(parser):
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    parser.add_argument('-host', '--host', default='0.0.0.0', type=str, help='host')
    parser.add_argument('-d', '--debug', default=True, type=bool, help='debug program')


def start_pipeline():
    parser = ArgumentParser()
    init_args(parser)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug)
