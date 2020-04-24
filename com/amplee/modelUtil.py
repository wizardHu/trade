import fileOperUtil as fileOperUtil
from JumpQueueModel import JumpQueueModel
from SellOrderModel import SellOrderModel
from TransactionModel import TransactionModel
from BuyModel import BuyModel
from StopLossModel import  StopLossModel

def getAllPair():
    lines = fileOperUtil.readAll("config")
    pairs = []

    for pair in lines:

        if pair != '' and pair != '\n':
            params = pair.split(',')
            symbol = params[0]
            everyExpense = params[1]
            tradeGap = params[2]
            minIncome = params[3]
            period = params[4]
            precision = params[5]
            stopLoss = params[6]

            tradeModel = TransactionModel(symbol, everyExpense, tradeGap, minIncome, period,precision,stopLoss)
            pairs.append(tradeModel)

    return pairs

def getBuyModel(symbol):
    lines = fileOperUtil.readAll("buy/"+symbol+"buy")
    models = []

    for model in lines:

        if model != '' and model != '\n':
            params = model.split(',')
            price = params[0]
            oriPrice = params[1]
            index = params[2]
            amount = params[3]
            orderId = params[4]
            minIncome = params[5]
            lastPrice = params[6]

            buyModel = BuyModel(price,oriPrice, index, amount, orderId,minIncome,lastPrice)
            models.append(buyModel)

    return models

def modBuyModel(oldBuyModel,newBuyModel,symbol):
    fileOperUtil.delMsgFromFile(oldBuyModel, "buy/" + symbol + "buy")
    fileOperUtil.write(newBuyModel, "buy/" + symbol + "buy")

def modJumpModel(oldJumpMode,newJumpMode,symbol):
    fileOperUtil.delMsgFromFile(oldJumpMode, "queue/" + symbol + "-queue")
    fileOperUtil.write(newJumpMode, "queue/" + symbol + "-queue")

def modStopLossModel(oldStopLossModel,newStopLossModel,symbol):
    fileOperUtil.delMsgFromFile(oldStopLossModel, "stopLossSell/" + symbol + "-sell")
    fileOperUtil.write(newStopLossModel, "stopLossSell/" + symbol + "-sell")


# 得到每次买需要的平均花费
def getAllPairAvgBuyExpense():
    pairsModel = getAllPair()

    count = 0

    for model in pairsModel:
        expense = model.everyExpense
        count += float(expense)

    return float(count/len(pairsModel))

def getStopLossModel(symbol):
    lines = fileOperUtil.readAll("stopLossSell/"+symbol+"-sell")
    models = []

    for model in lines:

        if model != '' and model != '\n':
            params = model.split(',')
            time = params[0]
            sellPrice = params[1]
            oriPrice = params[2]
            oriAmount = params[3]
            oriOrderId = params[4]
            orderId = params[5]
            status = params[6]

            stopLossModel = StopLossModel(time, sellPrice, oriPrice, oriAmount,oriOrderId,orderId,status)
            models.append(stopLossModel)

    return models

def getStopLossModelByOrderId(symbol,selectOrderId):
    lines = fileOperUtil.readAll("stopLossSell/" + symbol + "-sell")

    for model in lines:

        if model != '' and model != '\n':
            params = model.split(',')
            time = params[0]
            sellPrice = params[1]
            oriPrice = params[2]
            oriAmount = params[3]
            oriOrderId = params[4]
            orderId = params[5]
            status = params[6]

            if str(orderId) == str(selectOrderId):
                stopLossModel = StopLossModel(time, sellPrice, oriPrice, oriAmount, oriOrderId, orderId, status)
                return stopLossModel

    return None

def getBuyModelByOrderId(symbol,oriOrderId):
    lines = fileOperUtil.readAll("buy/"+symbol+"buy")

    for model in lines:

        if model != '' and model != '\n':
            params = model.split(',')
            price = params[0]
            oriPrice = params[1]
            index = params[2]
            amount = params[3]
            orderId = params[4]
            minIncome = params[5]
            lastPrice = params[6]

            if str(oriOrderId) == str(orderId):
                buyModel = BuyModel(price,oriPrice, index, amount, orderId,minIncome,lastPrice)
                return buyModel

    return None

def getJumpModel(symbol):
    lines = fileOperUtil.readAll("queue/"+symbol+"-queue")
    models = []

    #type,orderId,lowPrice,highPrice,jumpPrice,jumpCount
    for model in lines:

        if model != '' and model != '\n':
            params = model.split(',')
            type = params[0]
            orderId = params[1]
            lowPrice = params[2]
            highPrice = params[3]
            jumpPrice = params[4]
            jumpCount = params[5]
            time = params[6]
            price = params[7]

            jumpQueueModel = JumpQueueModel(type, orderId, lowPrice, highPrice,jumpPrice,jumpCount,time,price)
            models.append(jumpQueueModel)

    return models

def getSellOrderModels(symbol):
    lines = fileOperUtil.readAll("sellOrder/"+symbol+"-sellorder")
    models = []

    for model in lines:

        if model != '' and model != '\n':
            params = model.split(',')
            buyPrice = params[0]
            sellPrice = params[1]
            buyIndex = params[2]
            sellIndex = params[3]
            buyOrderId = params[4]
            sellOrderId = params[5]
            amount = params[6]
            time = params[7]

            sellOrderModel = SellOrderModel(buyPrice, sellPrice, buyIndex, sellIndex,buyOrderId,sellOrderId,amount,time)
            models.append(sellOrderModel)

    return models

if __name__ == '__main__':
   print(getBuyModelByOrderId("eosusdt","111121"))
