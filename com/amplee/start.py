# -*- coding: utf-8 -*-
import HuobiService as huobi
import modelUtil as modelUtil
import klineUtil as klineUtil
import KDJUtil as kDJUtil
import RSIUtil as rSIUtil
import MAUtil as mAUtil
import commonUtil as commonUtil
import BiTradeUtil as biTradeUtil

if __name__ == '__main__':
    transactionModels = modelUtil.getAllPair()

    for transactionModel in transactionModels:
        print(transactionModel)
        kline = huobi.get_kline(transactionModel.symbol, transactionModel.period, 2000)

        datas = kline['data']
        datas.reverse()

        for data in datas:
            klineUtil.add(data, transactionModel.symbol)
            kDJUtil.add(data,transactionModel.symbol)
            rSIUtil.add(transactionModel.symbol,12)
            mAUtil.add(transactionModel.symbol,10)
            mAUtil.add(transactionModel.symbol, 30)
            mAUtil.add(transactionModel.symbol, 60)

            kdjFlag = kDJUtil.judgeBuy(transactionModel.symbol)
            rSIFlag = rSIUtil.rsiJudgeBuy(transactionModel.symbol,12)
            maFlag = mAUtil.maJudgeBuy(data,transactionModel.symbol)
            avgFlag = commonUtil.juideAllGap(data['close'],transactionModel.symbol,transactionModel.tradeGap)
            highFlag = commonUtil.juideHighest(data['close'],transactionModel.symbol)

            if kdjFlag and rSIFlag and maFlag and avgFlag and highFlag:
                price = float(data['close'])
                amount = round(float(transactionModel.everyExpense)/price,2)
                biTradeUtil.buy("dev",price,amount,transactionModel.symbol,data['id'])

        print(rSIUtil.rsiDice)


