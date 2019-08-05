class TickUtil:
    buySum = 0.0
    sellSum = 0.0

    def __init__(self, buySum, sellSum):
        self.buySum = buySum
        self.sellSum = sellSum

    def getValue(self):
        return "{},{}".format(self.buySum, self.sellSum)

    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()