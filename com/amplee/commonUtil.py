# -*- coding: utf-8 -*-
import modelUtil as modelUtil
import klineUtil as klineUtil
import KDJUtil as kDJUtil
import RSIUtil as rSIUtil
import MAUtil as mAUtil
import AmountUtil as amountUtil
import logUtil

nextBuy = False
lastIdDict = {}
lastDataDict = {}
highCount = {}

def juideAllGap(price,symbol,tradeGap):
    buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史 #查询购买历史

    for model in buyPackage:

        buyPrice = float(model.price)

        #计算当前价格与以往每次的差值
        gap = abs(buyPrice - price)
        times = gap / buyPrice
        if times < float(tradeGap):
            return False

    return True

#判断能不能买
def juideHighest(price,symbol):
    lastPrice = klineUtil.prices.get(symbol, [])

    high = max(lastPrice)
    # 比最大值少两个点还要大就不要买了 风险高
    if price >= high * 0.98:
        return False

    return True

def juideLowest(price,symbol):
    lastPrice = klineUtil.prices.get(symbol, [])

    low = min(lastPrice)

    if price <= low:
        return True

    return False

def canSell(price,symbol,minIncome,env):

    sellPackage = []

    try:
        buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史 #查询购买历史

        for buyModel in buyPackage:

            buyModelPrice = buyModel.price;

            gap = price - float(buyModelPrice)
            gap = gap / float(buyModelPrice)

            if gap >= float(minIncome) and gap >= float(buyModel.minIncome):
                sellPackage.append(buyModel)

    except Exception as err:
        logUtil.info("commonUtil--canSell"+err)

    return sellPackage

def addSymbol(data,transactionModel):
    logUtil.info(data, "new data-----",transactionModel.symbol)

    klineUtil.add(data, transactionModel.symbol)
    kDJUtil.add(data, transactionModel.symbol)
    rSIUtil.add(transactionModel.symbol, 12)
    mAUtil.add(transactionModel.symbol, 10)
    mAUtil.add(transactionModel.symbol, 30)
    mAUtil.add(transactionModel.symbol, 60)
    amountUtil.add(data,transactionModel.symbol)

def delSymbol(transactionModel):
    klineUtil.delSymbol(transactionModel.symbol)
    kDJUtil.delSymbol(transactionModel.symbol)
    rSIUtil.delSymbol(transactionModel.symbol, 12)
    mAUtil.delSymbol(transactionModel.symbol, 10)
    mAUtil.delSymbol(transactionModel.symbol, 30)
    mAUtil.delSymbol(transactionModel.symbol, 60)
    amountUtil.delSymbol(transactionModel.symbol)
    lastDataDict[transactionModel.symbol] = []
    lastIdDict[transactionModel.symbol] = 0
    highCount[transactionModel.symbol] = 0

def getStopLossBuyModel(price,symbol,stopLoss):
    stopLossPackage = []

    try:
        buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史

        for buyModel in buyPackage:

            buyModelPrice = float(buyModel.price)
            minIncome = float(buyModel.minIncome)

            if minIncome == 1:
                continue

            gap = buyModelPrice - price
            gap = gap / buyModelPrice

            if gap >= float(stopLoss):
                stopLossPackage.append(buyModel)

    except Exception as err:
        logUtil.info("commonUtil--getStopLossBuyModel" + err)

    return stopLossPackage

#判断之前因为止损卖出的  现在可不可以买回来
def getCanBuyStopLoss(price,symbol):
    stopLossPackage = []

    try:
        sellPackage = modelUtil.getStopLossModel(symbol)  # 查询卖出历史

        for stopLossModel in sellPackage:

            sellPrice = float(stopLossModel.sellPrice)
            minIncome = 0.02#暂定 2个百分点

            gap = sellPrice - price
            gap = gap / sellPrice

            if gap >= float(minIncome):
                stopLossPackage.append(stopLossModel)

    except Exception as err:
        logUtil.info("commonUtil--getCanBuyStopLoss" + err)

    return stopLossPackage

if __name__ == '__main__':
    print(getCanBuyStopLoss(13.72,"eosusdt"))