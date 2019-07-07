# -*- coding: utf-8 -*-
import HuobiService as huobi
import modelUtil as modelUtil
import klineUtil as klineUtil
import KDJUtil as kDJUtil
import RSIUtil as rSIUtil
import MAUtil as mAUtil
import commonUtil as commonUtil
import BiTradeUtil as biTradeUtil
import fileOperUtil as fileOperUtil
import BollUtil as bollUtil

if __name__ == '__main__':
    transactionModels = modelUtil.getAllPair()
    env = "dev"

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
            bollFlag = bollUtil.judgeBoll(data['close'],transactionModel.symbol)
            lowFlag = commonUtil.juideLowest(data['close'],transactionModel.symbol)

            sellFlag = kDJUtil.judgeSell(transactionModel.symbol)

            if data['id'] == 1562337900:
                lowFlag = True
                print(kdjFlag,rSIFlag,maFlag,avgFlag,highFlag,lowFlag,bollFlag,kDJUtil.kdjDict.get(transactionModel.symbol)[-1].K,kDJUtil.kdjDict.get(transactionModel.symbol)[-1].D,kDJUtil.kdjDict.get(transactionModel.symbol)[-1].J)

            price = float(data['close'])

            if commonUtil.nextBuy and avgFlag:
                amount = round(float(transactionModel.everyExpense) / price, 2)
                biTradeUtil.buy(env, price, amount, transactionModel.symbol, data['id'])
                commonUtil.nextBuy = False
                print("222222")

            elif kdjFlag and rSIFlag and maFlag and avgFlag and highFlag:
                amount = round(float(transactionModel.everyExpense)/price,2)
                biTradeUtil.buy(env,price,amount,transactionModel.symbol,data['id'])

            elif avgFlag and lowFlag and bollFlag:
                commonUtil.nextBuy = True

            if sellFlag:
                sellPackage = commonUtil.canSell(data['close'],transactionModel.symbol,transactionModel.minIncome,"dev")
                if len(sellPackage) > 0:
                    for buyModel in sellPackage:
                        biTradeUtil.sell("dev",price,data['id'],buyModel,transactionModel.symbol)

        print(rSIUtil.rsiDice)
        fileOperUtil.delAll(transactionModel.symbol+"buy")


