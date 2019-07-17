# -*- coding: utf-8 -*-
import HuobiService as huobi
import modelUtil as modelUtil
import KDJUtil as kDJUtil
import RSIUtil as rSIUtil
import MAUtil as mAUtil
import commonUtil as commonUtil
import BiTradeUtil as biTradeUtil
import fileOperUtil as fileOperUtil
import BollUtil as bollUtil
import AmountUtil as amountUtil
import logUtil

if __name__ == '__main__':
    transactionModels = modelUtil.getAllPair()
    env = "dev"
    lastIndex = 0

    for transactionModel in transactionModels:
        logUtil.info(transactionModel)
        kline = huobi.get_kline(transactionModel.symbol, transactionModel.period, 2000)

        datas = kline['data']
        datas.reverse()

        for data in datas:
            commonUtil.addSymbol(data ,transactionModel)

            kdjFlag = kDJUtil.judgeBuy(transactionModel.symbol)
            rSIFlag = rSIUtil.rsiJudgeBuy(transactionModel.symbol,12)
            maFlag = mAUtil.maJudgeBuy(data,transactionModel.symbol)
            avgFlag = commonUtil.juideAllGap(data['close'],transactionModel.symbol,transactionModel.tradeGap)
            highFlag = commonUtil.juideHighest(data['close'],transactionModel.symbol)
            bollFlag = bollUtil.judgeBoll(data['close'],transactionModel.symbol)
            lowFlag = commonUtil.juideLowest(data['close'],transactionModel.symbol)
            riskFlag = amountUtil.judgeRisk(transactionModel.symbol)

            sellFlag = kDJUtil.judgeSell(transactionModel.symbol)

            price = float(data['close'])

            if 1562683380 == data['id']:
                logUtil.info(kdjFlag,rSIFlag,maFlag,avgFlag,highFlag,bollFlag,lowFlag,riskFlag,lastIndex)

            lastIndex = data['id']

            if commonUtil.nextBuy and avgFlag:
                amount = round(float(transactionModel.everyExpense) / price, transactionModel.precision)
                biTradeUtil.buy(env, price, amount, transactionModel.symbol, data['id'])
                commonUtil.nextBuy = False

            elif kdjFlag and rSIFlag and maFlag and avgFlag and highFlag:
                amount = round(float(transactionModel.everyExpense)/price,transactionModel.precision)
                biTradeUtil.buy(env,price,amount,transactionModel.symbol,data['id'])

            elif avgFlag and lowFlag and bollFlag and riskFlag and highFlag:
                commonUtil.nextBuy = True

            if sellFlag:
                sellPackage = commonUtil.canSell(data['close'],transactionModel.symbol,transactionModel.minIncome,"dev")
                if len(sellPackage) > 0:
                    for buyModel in sellPackage:
                        biTradeUtil.sell("dev",price,data['id'],buyModel,transactionModel.symbol)

        logUtil.info(rSIUtil.rsiDice)
        fileOperUtil.delAll("buy/"+transactionModel.symbol+"buy")


