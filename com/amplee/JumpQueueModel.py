class JumpQueueModel:
    # type,orderId,lowPrice,highPrice,jumpPrice,jumpCount,time,oriPrice
    # 操作类型，订单Id，价格区间低，价格区间高，触发跳跃的最低价格，跳跃次数,加入的时间，原始的价格
    type = 0 #为单数即为买  1 正常买  2 正常卖  3 止损后买
    orderId = 0
    lowPrice = 0.0
    highPrice = 0.0
    jumpPrice = 0.0
    jumpCount = 0
    time = ""
    oriPrice = 0.0

    def __init__(self, type,orderId, lowPrice, highPrice, jumpPrice,jumpCount,time,oriPrice):
        self.type = type
        self.orderId = orderId
        self.lowPrice = lowPrice
        self.highPrice = highPrice
        self.jumpPrice = jumpPrice
        self.jumpCount = jumpCount
        self.time = time
        self.oriPrice = oriPrice

    def getValue(self):
        return "{},{},{},{},{},{},{},{}".format(self.type,self.orderId, self.lowPrice, self.highPrice, self.jumpPrice,self.jumpCount,self.time,self.oriPrice)


    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()