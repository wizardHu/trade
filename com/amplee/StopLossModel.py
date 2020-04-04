class StopLossModel:  #在{什么时候} 以 {什么价格} 卖出 {原价是什么} 的 {多少个} {原来的orderId} {这次的orderId}
    time = ""
    sellPrice = 0
    oriPrice = 0.0
    oriAmount = 0
    oriOrderId = "0"
    orderId = "0"

    def __init__(self, time, sellPrice, oriPrice, oriAmount,oriOrderId,orderId):
        self.time = time
        self.sellPrice = sellPrice
        self.oriPrice = oriPrice
        self.oriAmount = oriAmount
        self.oriOrderId = oriOrderId
        self.orderId = orderId

    def getValue(self):
        return "{},{},{},{},{},{}".format(self.time, self.sellPrice, self.oriPrice, self.oriAmount,self.oriOrderId,self.orderId)


    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()