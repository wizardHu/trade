import time

class TradeModel:
    price = 0.0
    index = 0
    amount = 0.0
    orderId = 0
    sellAmount = 0
    buyPrice = 0
    symbol = ''

    def __init__(self, price, index, amount, orderId,symbol):
        self.price = price
        self.amount = amount
        self.orderId = orderId
        self.symbol = symbol
        timestamp = int(index) / 1000
        time_local = time.localtime(timestamp)
        #         self.index = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        self.index = index

    def getValue(self):
        return "{},{},{},{},{}".format(self.price, self.amount, self.orderId, self.index,self.symbol)

    def printTradeModel(self):
        print('price={} index={} amount={} orderId={} sellAmount={} buyPrice={} symbol={}'.format(self.price,
                                                                                                      self.index,
                                                                                                      self.amount,
                                                                                                      self.orderId,
                                                                                                      self.sellAmount,
                                                                                                      self.buyPrice,self.symbol))

    def __str__(self):
        return "{}".format(self.price)

    def __repr__(self):
        return "{}".format(self.price)