import fileOperUtil as fileOperUtil
from TransactionModel import TransactionModel

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

if __name__ == '__main__':
    print(getAllPair())
