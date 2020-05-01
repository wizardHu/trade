class SellOrderModel:
    id = 0
    symbol = ""
    buyPrice = 0.0
    sellPrice = 0.0
    buyIndex = 0
    sellIndex = 0
    buyOrderId = 0
    sellOrderId = 0
    amount = 0.0

    def __init__(self, id,symbol,buyPrice,sellPrice, buyIndex, sellIndex, buyOrderId,sellOrderId,amount):
        self.id = id
        self.symbol = symbol
        self.buyPrice = buyPrice
        self.sellPrice = sellPrice
        self.buyIndex = buyIndex
        self.sellIndex = sellIndex
        self.buyOrderId = buyOrderId
        self.sellOrderId = sellOrderId
        self.amount = amount

    def getValue(self):
        return "{},{},{},{},{},{},{},{},{}".format(self.id,self.symbol,self.buyPrice,self.sellPrice, self.buyIndex, self.sellIndex, self.buyOrderId,self.sellOrderId,self.amount)


    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()