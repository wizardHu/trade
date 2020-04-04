import fileOperUtil as fileOperUtil
from TransactionModel import TransactionModel
from BuyModel import BuyModel

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

# 得到每次买需要的平均花费
def getAllPairAvgBuyExpense():
    pairsModel = getAllPair()

    count = 0

    for model in pairsModel:
        expense = model.everyExpense
        count += float(expense)

    return float(count/len(pairsModel))

if __name__ == '__main__':
   print(getAllPair())
