# -*- coding: utf-8 -*-
import modelUtil as modelUtil
import klineUtil as klineUtil
import KDJUtil as kDJUtil
import RSIUtil as rSIUtil
import MAUtil as mAUtil
import AmountUtil as amountUtil
import logUtil
from BuyModel import BuyModel

nextBuy = False
lastIdDict = {}
lastDataDict = {}
highCount = {}

def juideAllGap(price,symbol,tradeGap):
    buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史 #查询购买历史

    for model in buyPackage:

        buyPrice = float(model.oriPrice)

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

#得到需要止损的
def getStopLossBuyModel(price,symbol,stopLoss):
    stopLossPackage = []

    stopLoss = float(stopLoss)
    try:
        buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史

        for buyModel in buyPackage:

            buyModelPrice = float(buyModel.price)
            buyModelOriPrice = float(buyModel.oriPrice)
            minIncome = float(buyModel.minIncome)
            lastPrice = float(buyModel.lastPrice)
            stopLosssTemp = stopLoss

            if minIncome == 1 or minIncome == 2 or buyModelPrice <= price:
                continue

            #判断有没有进行过止损
            if buyModelPrice != buyModelOriPrice:
                if price < lastPrice:
                    stopLosssTemp = stopLoss / 2
                    buyModelPrice = lastPrice
                else:
                    #与上一次买的价差率
                    lastGap = price - lastPrice
                    lastGap = lastGap/lastPrice

                    #与当前价格的价差率
                    nowGap = buyModelPrice - price
                    nowGap = nowGap/buyModelPrice

                    if lastGap < 0.02 or nowGap < stopLoss:
                        continue


            gap = buyModelPrice - price
            gap = gap / buyModelPrice

            if gap >= stopLosssTemp:
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
            minIncome = 0.03#暂定 3个百分点

            gap = sellPrice - price
            gap = gap / sellPrice

            if gap >= float(minIncome):
                stopLossPackage.append(stopLossModel)

    except Exception as err:
        logUtil.info("commonUtil--getCanBuyStopLoss" + err)

    return stopLossPackage

#计算小数点后的位数
def calDecimal(ori):
    oriStr = str(ori)
    index = oriStr.find(".")
    length = 4
    if index != -1:
        priceStr = oriStr[index + 1:]
        length = len(priceStr)
    return length

if __name__ == '__main__':
    #2.7919,2.846,1578493080,3.51,575060314,0.015,2.6496
    print(getStopLossBuyModel(2.6496,"eosusdt",0.05))