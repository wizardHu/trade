prices = []
amounts = []

def add(data, index):
    global prices
    global amounts

    Cn = data['close']
    amount = data['amount']
    prices.append(Cn)
    amounts.append(amount)

    if len(prices) > 720:
        prices = prices[1:]
        amounts = amounts[1:]