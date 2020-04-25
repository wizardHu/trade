# -*- coding: utf-8 -*-
import modelUtil as modelUtil
import klineUtil as klineUtil
import KDJUtil as kDJUtil
import RSIUtil as rSIUtil
import MAUtil as mAUtil
import AmountUtil as amountUtil
import logUtil
from BuyModel import BuyModel
import HuobiService as huobi
import fileOperUtil as fileOperUtil
from TransactionModel import TransactionModel

nextBuy = False
lastIdDict = {}
lastDataDict = {}
highCount = {}

def juideAllGap(price,symbol,tradeGap):
    buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史 #查询购买历史

    for model in buyPackage:

        minIncome = float(model.minIncome)
        if minIncome == 1 or minIncome == 3 or minIncome == 4:
            continue

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

def canSell(price,symbol,env):

    sellPackage = []

    try:
        buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史 #查询购买历史

        for buyModel in buyPackage:

            minIncome = float(buyModel.minIncome)

            if minIncome == 1 or minIncome == 2 or minIncome == 3 or minIncome == 4:
                continue

            if "pro" == env:
                minIncome = minIncome - 0.01 #生产环境提前先挂单

            buyModelPrice = buyModel.price;

            gap = price - float(buyModelPrice)
            gap = gap / float(buyModelPrice)

            if gap >= minIncome:
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

            if minIncome == 1 or minIncome == 2 or minIncome == 3 or minIncome == 4 or buyModelPrice <= price:
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

            status = int(stopLossModel.status)
            if status == 1:
                continue

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

    if length <4:
        length = 4

    return length

# 判断订单的状态
def checkOrderIsFilled(env,orderId):
    if "pro" == env:
        result = huobi.order_info(orderId)
        data = result['data']
        state = data['state']
        if state == 'filled':
            return True
    else:
        return True

    return False

def doMerge(env,list, transactionModel):

    if len(list) < 1:
        return None

    decimallength = calDecimal(list[0].price)
    price = 0.0
    amount = 0.0
    index = 0
    orderId = 0
    shouldDel = []

    for buyModel in list:
        if checkOrderIsFilled(env,buyModel.orderId):
            logUtil.info("doMerge=" ,buyModel)
            shouldDel.append(buyModel)
            price = price + float(buyModel.price)*float(buyModel.amount)
            amount = amount + float(buyModel.amount)
            index = buyModel.index #这两个随便
            orderId = buyModel.orderId


    if len(shouldDel) < 2:
        return None

    amount = round(amount,int(transactionModel.precision))
    avgPrice = round(price / amount, decimallength)

    newBuyModel = BuyModel(avgPrice, avgPrice, index, amount, orderId,
                           transactionModel.minIncome, avgPrice)

    for shouldDelBuyModel in shouldDel:
        fileOperUtil.delMsgFromFile(shouldDelBuyModel,"buy/"+transactionModel.symbol+"buy")

    fileOperUtil.write(newBuyModel,"buy/"+transactionModel.symbol+"buy")

    return newBuyModel

    # 合并购买的
def mergeBuyModel(env,buyModels,transactionModel,price):

    list = []
    resultList = []
    unDealList = []

    everyBuyAmount = float(transactionModel.everyExpense) / price

    if len(buyModels) > 0:
        for buyModel in buyModels:

            amount = float(buyModel.amount)
            if amount > everyBuyAmount * 3:#合并过很多次就不处理了
                unDealList.append(buyModel)
                continue

            list.append(buyModel)
            if len(list) == 3:#暂时是三合一
                mergeBuyModel = doMerge(env,list,transactionModel)
                if mergeBuyModel != None:
                    resultList.append(mergeBuyModel)
                    list.clear()

    if len(resultList) > 0:
        if len(list) > 0:
            resultList = resultList + list
        if len(unDealList) > 0:
            resultList = resultList + unDealList

        return resultList

    return buyModels

if __name__ == '__main__':
    minIncome = "1.0"
    a = float(minIncome)
    print(a == 1)