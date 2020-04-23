class BuyModel:
    price = 0.0
    oriPrice = 0.0
    index = 0
    amount = 0.0
    orderId = 0
    minIncome = 0.0 # 小数：已经交易了，待下一步处理  1 被止损了  2 进入买交易队列了  3进入卖交易队列  4进入挂单
    lastPrice = 0.0

    def __init__(self, price,oriPrice, index, amount, orderId,minIncome,lastPrice):
        self.price = price
        self.oriPrice = oriPrice
        self.amount = amount
        self.orderId = orderId
        self.index = index
        self.minIncome = minIncome
        self.lastPrice = lastPrice

    def getValue(self):
        return "{},{},{},{},{},{},{}".format(self.price,self.oriPrice, self.index, self.amount, self.orderId,self.minIncome,self.lastPrice)


    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()