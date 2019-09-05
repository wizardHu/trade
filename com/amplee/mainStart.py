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

def addQueue(price,transactionModel):
    isCanAddToSellQueue = commonUtil.needAddToSellQueue()  # 是否需要加入卖的队列
    if isCanAddToSellQueue:
        buyModel = commonUtil.findHighToSell(price, transactionModel.symbol, False)  # 先读取buy目录下的buyModel
        if buyModel is not None:
            commonUtil.addToSellQueue(buyModel, transactionModel.symbol)  # 将该buyModel加入待紧急卖队列 并且修改状态
            logUtil.info(("add to queue {} symbol={}").format(buyModel, transactionModel.symbol))

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
               addQueue(price, transactionModel)

        elif kdjFlag and rSIFlag and maFlag and avgFlag and highFlag:
            amount = round(float(transactionModel.everyExpense) / price, int(transactionModel.precision))
            isSuccess = biTradeUtil.buy(env, price, amount, transactionModel.symbol, data['id'],transactionModel.minIncome)
            logUtil.info(("is first buy symbol={},price={},data['id']={} issuccess={}").format(transactionModel.symbol, price, data['id'],isSuccess))

            if isSuccess:
               addQueue(price, transactionModel)

        elif avgFlag and lowFlag and bollFlag and riskFlag and highFlag:
            commonUtil.nextBuy = True

        if sellFlag:
            sellPackage = commonUtil.canSell(data['close'], transactionModel.symbol, transactionModel.minIncome, env)

            logUtil.info(sellPackage)

            if len(sellPackage) > 0:
                for buyModel in sellPackage:
                    biTradeUtil.sell(env, price, data['id'], buyModel, transactionModel.symbol)

        # 当前最高价紧急卖策略
        isHighest = commonUtil.isHighest(price, transactionModel.symbol)
        canSell = commonUtil.canUrgentSell(price, transactionModel.symbol, transactionModel.minIncome)
        if isHighest and canSell:
            buyModel = commonUtil.findHighToSell(price, transactionModel.symbol,False) #先读取buy目录下的buyModel
            if buyModel is not None:
                commonUtil.addToSellQueue(buyModel,transactionModel.symbol) # 将该buyModel加入待紧急卖队列 并且修改状态
                newBuyModel = commonUtil.findHighToSell(price, transactionModel.symbol, True) # 从队列中找到最合适的
                biTradeUtil.urgentSell(env,price,data['id'],newBuyModel, transactionModel.symbol,0.025) #卖掉 并且删除队列记录

        # 买回来
        canBuyPackage = commonUtil.canUrgentBuy(price, transactionModel.symbol,env)
        if len(canBuyPackage) > 0:
            for canBuy in canBuyPackage:
                logUtil.info("can urgent buy ",canBuy)
                biTradeUtil.urgentBuy(env,price,data['id'],canBuy,transactionModel.symbol)

        # 读取队列卖
        amountUrgentBuy = amountUtil.judgeUrgentSell(transactionModel.symbol)
        bollUrgentBuy = bollUtil.judgeBollSell(data,transactionModel.symbol)
        logUtil.info(("amountUrgentBuy={}, bollUrgentBuy={}").format(amountUrgentBuy, bollUrgentBuy))

        if amountUrgentBuy and bollUrgentBuy and canSell:
            newBuyModel = commonUtil.findHighToSell(price, transactionModel.symbol, True)  # 从队列中找到最合适的
            biTradeUtil.urgentSell(env, price, data['id'], newBuyModel, transactionModel.symbol, 0.015)  # 卖掉 并且删除队列记录

    except Exception as err:
        logUtil.info('deal error', err)


if __name__ == '__main__':

    env = "pro"

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

                if lastId != thisData['data'][0]['id']:
                    commonUtil.addSymbol(lastData['data'][0],transactionModel)
                    dealData(lastData['data'][0],transactionModel,env)

                commonUtil.lastDataDict[transactionModel.symbol] = thisData
                commonUtil.lastIdDict[transactionModel.symbol] = thisData['data'][0]['id']

        except Exception as err:
            logUtil.info('connect https error,retry...', err)

        time.sleep(1)
