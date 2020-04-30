class StopLossModel:  #在{什么时候} 以 {什么价格} 卖出 {原价是什么} 的 {多少个} {原来的orderId} {这次的orderId}
    id = 0
    symbol = ""
    # time = ""
    sellPrice = 0
    oriPrice = 0.0
    oriAmount = 0
    oriOrderId = "0"
    orderId = "0"
    status = 0 #默认状态  1 进入交易队列

    def __init__(self,id, symbol, sellPrice, oriPrice, oriAmount,oriOrderId,orderId,status):
        self.id = id
        self.symbol = symbol
        self.sellPrice = sellPrice
        self.oriPrice = oriPrice
        self.oriAmount = oriAmount
        self.oriOrderId = oriOrderId
        self.orderId = orderId
        self.status = status

    def getValue(self):
        return "{},{},{},{},{},{},{}".format(self.id, self.symbol, self.sellPrice, self.oriPrice, self.oriAmount,self.oriOrderId,self.orderId,self.status)


    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()