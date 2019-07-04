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

            tradeModel = TransactionModel(symbol, everyExpense, tradeGap, minIncome, period)
            pairs.append(tradeModel)

    return pairs

def getBuyModel(symbol):
    lines = fileOperUtil.readAll(symbol+"buy")
    models = []

    for model in lines:

        if model != '' and model != '\n':
            params = model.split(',')
            price = params[0]
            amount = params[1]
            orderId = params[2]
            index = params[3]

            buyModel = BuyModel(price, index, amount, orderId)
            models.append(buyModel)

    return models

if __name__ == '__main__':
    print(getBuyModel("eosusdt"))
