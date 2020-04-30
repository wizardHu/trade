class BuyModel:
    id = 0
    symbol = ''
    price = 0.0
    oriPrice = 0.0
    index = 0
    amount = 0.0
    orderId = 0
    minIncome = 0.0
    lastPrice = 0.0
    status = 0 # 1 被止损了  2 进入买交易队列了  3进入卖交易队列  4进入挂单

    def __init__(self,id, symbol,price,oriPrice, index, amount, orderId,minIncome,lastPrice,status):
        self.id = id
        self.symbol = symbol
        self.price = price
        self.status = status
        self.oriPrice = oriPrice
        self.amount = amount
        self.orderId = orderId
        self.index = index
        self.minIncome = minIncome
        self.lastPrice = lastPrice

    def getValue(self):
        return "{},{},{},{},{},{},{},{},{},{}".format(self.id,self.symbol,self.price,self.oriPrice, self.index, self.amount, self.orderId,self.minIncome,self.lastPrice,self.status)


    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()