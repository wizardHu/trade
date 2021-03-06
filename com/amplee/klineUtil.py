prices = {}
amounts = {}

def add(data,symbol):
    global prices
    global amount

    priceList = prices.get(symbol,[])
    amountList = amounts.get(symbol,[])

    Cn = data['close']
    priceList.append(Cn)

    amount = data['amount']
    amountList.append(amount)

    if len(priceList) > 1440:
        priceList = priceList[1:]
        amountList = amountList[1:]

    prices[symbol] = priceList
    amounts[symbol] = amountList

def delSymbol(symbol):
    global prices
    global amount

    prices[symbol] = []
    amounts[symbol] = []