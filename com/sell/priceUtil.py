prices = []

def add(data, index):
    global prices

    Cn = data['close']
    prices.append(Cn)

    if len(prices) > 720:
        prices = prices[1:]