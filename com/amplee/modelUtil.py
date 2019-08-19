import fileOperUtil as fileOperUtil
from TransactionModel import TransactionModel
from BuyModel import BuyModel
from UrgentSellModel import UrgentSellModel

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

            tradeModel = TransactionModel(symbol, everyExpense, tradeGap, minIncome, period,precision)
            pairs.append(tradeModel)

    return pairs

def getBuyModel(symbol):
    lines = fileOperUtil.readAll("buy/"+symbol+"buy")
    models = []

    for model in lines:

        if model != '' and model != '\n':
            params = model.split(',')
            price = params[0]
            amount = params[1]
            orderId = params[2]
            index = params[3]
            minIncome = params[4]

            buyModel = BuyModel(price, index, amount, orderId,minIncome)
            models.append(buyModel)

    return models

def modBuyModel(oldBuyModel,newBuyModel,symbol):
    fileOperUtil.delMsgFromFile(oldBuyModel, "buy/" + symbol + "buy")
    fileOperUtil.write(newBuyModel, "buy/" + symbol + "buy")

def getUrgentSellModel(symbol):
    lines = fileOperUtil.readAll("sell/"+symbol+"sell")
    models = []

    for model in lines:

        if model != '' and model != '\n':
            params = model.split(',')
            price = params[0]
            amount = params[1]
            orderId = params[2]
            index = params[3]
            minIncome = params[4]
            sellIndex = params[5]
            sellOrderId = params[6]
            sellPrice = params[7]
            sellMinIncome = params[8]

            buyModel = BuyModel(price, index, amount, orderId,minIncome)

            urgentSellModel = UrgentSellModel(buyModel,sellIndex,sellOrderId,sellPrice,sellMinIncome)

            models.append(urgentSellModel)

    return models

def getAllPairAvgBuyExpense():
    pairsModel = getAllPair()

    count = 0

    for model in pairsModel:
        expense = model.everyExpense
        count += float(expense)

    return float(count/len(pairsModel))

if __name__ == '__main__':
   print(getAllPairAvgBuyExpense())
