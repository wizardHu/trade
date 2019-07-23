class UrgentSellModel:
    buyModel = None
    sellPrice = 0.0
    orderId = 0
    index = 0

    def __init__(self, buyModel, index, orderId,sellPrice):
        self.sellPrice = sellPrice
        self.orderId = orderId
        self.index = index
        self.buyModel = buyModel

    def getValue(self):
        return "{},{},{},{}".format(self.buyModel, self.index, self.orderId,self.sellPrice)

    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()