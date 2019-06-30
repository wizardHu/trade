# -*- coding: utf-8 -*-
import HuobiService as huobi
import modelUtil as modelUtil
import klineUtil as klineUtil
import KDJUtil as kDJUtil


if __name__ == '__main__':
    transactionModels = modelUtil.getAllPair()

    for transactionModel in transactionModels:
        print(transactionModel)
        kline = huobi.get_kline(transactionModel.symbol, transactionModel.period, 3)

        datas = kline['data']
        datas.reverse()

        for data in datas:
            klineUtil.add(data, transactionModel.symbol)
            kDJUtil.addJDK(data,transactionModel.symbol)

        print(kDJUtil.kdjDict)


