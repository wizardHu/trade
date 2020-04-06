# -*- coding: utf-8 -*-
import HuobiService as huobi
import KDJUtil as kDJUtil
import RSIUtil as rSIUtil
import MAUtil as mAUtil
import commonUtil as commonUtil
import BiTradeUtil as biTradeUtil
import BollUtil as bollUtil
import AmountUtil as amountUtil
import logUtil
import Refresh as refresh
import time

#策略模块
def dealData(data,transactionModel,env):
    try:
        kdjFlag = kDJUtil.judgeBuy(transactionModel.symbol)
        rSIFlag = rSIUtil.rsiJudgeBuy(transactionModel.symbol, 12)
        maFlag = mAUtil.maJudgeBuy(data, transactionModel.symbol)
        avgFlag = commonUtil.juideAllGap(data['close'], transactionModel.symbol, transactionModel.tradeGap)
        highFlag = commonUtil.juideHighest(data['close'], transactionModel.symbol)
        bollFlag = bollUtil.judgeBollBuy(data['close'], transactionModel.symbol)
        lowFlag = commonUtil.juideLowest(data['close'], transactionModel.symbol)
        riskFlag = amountUtil.judgeRisk(transactionModel.symbol)

        sellFlag = kDJUtil.judgeSell(transactionModel.symbol)

        logUtil.info(("kdjFlag={}, rSIFlag={}, maFlag={}, avgFlag={}, highFlag={}, bollFlag={}, lowFlag={}, riskFlag={} sellFlag={}").format(kdjFlag, rSIFlag, maFlag, avgFlag, highFlag, bollFlag, lowFlag, riskFlag,sellFlag))

        price = float(data['close'])

        if commonUtil.nextBuy and avgFlag:
            amount = round(float(transactionModel.everyExpense) / price, int(transactionModel.precision))
            isSuccess = biTradeUtil.buy(env, price, amount, transactionModel.symbol, data['id'],transactionModel.minIncome)
            logUtil.info(("is next buy symbol={},price={},data['id']={} issuccess={}").format(transactionModel.symbol,price,data['id'],isSuccess))

            if isSuccess:
               commonUtil.nextBuy = False

        elif kdjFlag and rSIFlag and maFlag and avgFlag and highFlag:
            amount = round(float(transactionModel.everyExpense) / price, int(transactionModel.precision))
            isSuccess = biTradeUtil.buy(env, price, amount, transactionModel.symbol, data['id'],transactionModel.minIncome)
            logUtil.info(("is first buy symbol={},price={},data['id']={} issuccess={}").format(transactionModel.symbol, price, data['id'],isSuccess))


        elif avgFlag and lowFlag and bollFlag and riskFlag and highFlag:
            commonUtil.nextBuy = True

        if sellFlag:
            sellPackage = commonUtil.canSell(data['close'], transactionModel.symbol, transactionModel.minIncome, env)

            logUtil.info(sellPackage)

            if len(sellPackage) > 0:
                for buyModel in sellPackage:
                    biTradeUtil.sell(env, price, data['id'], buyModel, transactionModel.symbol)

    except Exception as err:
        logUtil.info('deal error', err)

#止损模块
def dealStopLoss(data,transactionModel,env):
    try:

        price = float(data['close'])
        neesStopLossPackage = commonUtil.getStopLossBuyModel(data['close'], transactionModel.symbol,
                                                             transactionModel.stopLoss)
        if len(neesStopLossPackage) > 0:  # 价格到达止损点
            for buyModel in neesStopLossPackage:
                logUtil.info("can stop loss ", buyModel)
                biTradeUtil.stopLossSell(env, price, buyModel, transactionModel.symbol)

        stopLossPackage = commonUtil.getCanBuyStopLoss(data['close'], transactionModel.symbol)
        if len(stopLossPackage) > 0:
            for stopLoss in stopLossPackage:
                logUtil.info("buy stop loss ", stopLoss)
                biTradeUtil.stopLossBuy(env, price, stopLoss, transactionModel.symbol,
                                        transactionModel.minIncome)

    except Exception as err:
        logUtil.info('dealStopLoss error', err)

if __name__ == '__main__':

    env = "dev"

    while True:
        transactionModels = refresh.getAllPairAndRefresh()

        lastDataDict = commonUtil.lastDataDict
        lastIdDict = commonUtil.lastIdDict

        try:

            for transactionModel in transactionModels:
                lastData = lastDataDict.get(transactionModel.symbol,[])
                lastId = lastIdDict.get(transactionModel.symbol,0)

                if len(lastData) == 0:
                    lastData = huobi.get_kline(transactionModel.symbol, transactionModel.period, 1)

                thisData = huobi.get_kline(transactionModel.symbol, transactionModel.period, 1)

                if thisData['status'] == 'ok' and thisData['data'] and len(thisData['data']) >= 1:
                    thisData['data'].reverse()
                else:
                    continue

                logUtil.info(thisData['data'],transactionModel.symbol)

                dealStopLoss(lastData['data'][0],transactionModel,env)#止损模块处理

                if lastId != thisData['data'][0]['id']: #策略模块处理
                    commonUtil.addSymbol(lastData['data'][0],transactionModel)
                    dealData(lastData['data'][0],transactionModel,env)

                commonUtil.lastDataDict[transactionModel.symbol] = thisData
                commonUtil.lastIdDict[transactionModel.symbol] = thisData['data'][0]['id']

        except Exception as err:
            logUtil.info('connect https error,retry...', err)

        time.sleep(1)
