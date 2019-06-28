# -*- coding: utf-8 -*-
import HuobiService as huobi
import modelUtil as modelUtil
from TransactionModel import TransactionModel

if __name__ == '__main__':
    transactionModels = modelUtil.getAllPair()

    for transactionModel in transactionModels:
        print(transactionModel)
        kline = huobi.get_kline(transactionModel.symbol, transactionModel.period, 2000)
        print(kline)

