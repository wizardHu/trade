class SellOrderModel:
    buyPrice = 0.0
    sellPrice = 0.0
    buyIndex = 0
    sellIndex = 0
    buyOrderId = 0
    sellOrderId = 0
    amount = 0.0
    time = ''

    def __init__(self, buyPrice,sellPrice, buyIndex, sellIndex, buyOrderId,sellOrderId,amount,time):
        self.buyPrice = buyPrice
        self.sellPrice = sellPrice
        self.buyIndex = buyIndex
        self.sellIndex = sellIndex
        self.buyOrderId = buyOrderId
        self.sellOrderId = sellOrderId
        self.amount = amount
        self.time = time

    def getValue(self):
        return "{},{},{},{},{},{},{},{}".format(self.buyPrice,self.sellPrice, self.buyIndex, self.sellIndex, self.buyOrderId,self.sellOrderId,self.amount,self.time)


    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()