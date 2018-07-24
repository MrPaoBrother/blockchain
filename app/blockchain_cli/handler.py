# -*- coding:utf8 -*-

from argparse import ArgumentParser
from client import blockchain_cli
import settings
import logging
logging.basicConfig(filename='../../log/%s.log' % settings.psm, level=logging.INFO)


def init_args(parser):
    parser.add_argument('-p', '--process', default=-1, type=int, help='different number present different process')


def get_menu():
    menu = """
        -------------------------------{tip}-------------------------------
                                    0  按键提示
                                    1  生成钱包
                                    2  同步节点数据
                                    3  转账
                                    4  挖矿
                                    5  注册节点
                                    6  查看区块数据
                                    7  解决冲突(如果存在更长的链)
                                    8  退出
        -----------------------------------------------------------------------
        """
    menu = menu.format(tip="区块链客户端提示")
    return menu


def process(args):
    if args.process == 0:
        print get_menu()
    elif args.process == 1:
        priv_key, pub_key = blockchain_cli.build_wallet()
        print "生成\n私钥:    %s\n\n公钥:     %s" % (priv_key.encode("utf8"), pub_key.encode("utf8"))
    elif args.process == 2:
        blockchain_cli.sync_data()
        print "链上所有数据同步完成,请在目录block_data下查看"
    elif args.process == 3:
        # 以下数据是测试数据
        priv_key, pub_key = blockchain_cli.build_wallet()
        blockchain_cli.sender_addr = pub_key
        blockchain_cli.receive_addr = "BCHVis"
        blockchain_cli.sender_priv = priv_key
        blockchain_cli.money = 100
        transaction_detail = blockchain_cli.new_transaction()
        if not transaction_detail:
            print "转账失败"
        print "转账成功，详情如下:\n"
        print transaction_detail
    elif args.process == 4:
        mine_detail = blockchain_cli.mine()
        print "挖矿成功,增加新区快,详情如下:\n"
        print mine_detail
    elif args.process == 5:
        register_detail = blockchain_cli.register_nodes()
        if not register_detail:
            print "注册失败"
        print "注册成功,详情如下:\n"
        print register_detail
    elif args.process == 6:
        chain_detail = blockchain_cli.full_chain()
        if not chain_detail:
            print "查询失败"
        print "查询成功,详情如下:\n"
        print chain_detail
    elif args.process == 7:
        solve_result = blockchain_cli.consensus()
        if not solve_result:
            print "冲突解决失败"
        print "链正常，详情如下:"
        print solve_result
    elif args.process == 8:
        import sys
        print "bye bye"
        sys.exit(0)
    else:
        print "没有这个功能"
        return


def process_input(args):
    while True:
        input_num = input("需要什么操作(0查看帮助, 8退出), 请输入:")
        args.process = input_num
        process(args)


def start_pipeline():
    parser = ArgumentParser()
    init_args(parser)
    args = parser.parse_args()
    if args.process == -1:
        process_input(args)
    else:
        process(args)




