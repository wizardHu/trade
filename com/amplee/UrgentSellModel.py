class UrgentSellModel:
    buyModel = None
    sellPrice = 0.0
    orderId = 0
    index = 0
    minIncome = 0

    def __init__(self, buyModel, index, orderId,sellPrice,minIncome):
        self.sellPrice = sellPrice
        self.orderId = orderId
        self.index = index
        self.buyModel = buyModel
        self.minIncome = minIncome

    def getValue(self):
        return "{},{},{},{},{}".format(self.buyModel, self.index, self.orderId,self.sellPrice,self.minIncome)

    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()