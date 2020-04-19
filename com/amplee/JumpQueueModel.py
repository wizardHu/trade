class JumpQueueModel:
    # type,orderId,lowPrice,highPrice,jumpPrice,jumpCount,time,index
    # 操作类型，订单Id，价格区间低，价格区间高，触发跳跃的最低价格，跳跃次数,加入的时间，当时操作的index
    type = 0 #为单数即为买  1 正常买  2 正常卖  3 止损后买
    orderId = 0
    lowPrice = 0.0
    highPrice = 0.0
    jumpPrice = 0.0
    jumpCount = 0
    time = ""
    index = 0

    def __init__(self, type,orderId, lowPrice, highPrice, jumpPrice,jumpCount,time,index):
        self.type = type
        self.orderId = orderId
        self.lowPrice = lowPrice
        self.highPrice = highPrice
        self.jumpPrice = jumpPrice
        self.jumpCount = jumpCount
        self.time = time
        self.index = index

    def getValue(self):
        return "{},{},{},{},{},{},{},{}".format(self.type,self.orderId, self.lowPrice, self.highPrice, self.jumpPrice,self.jumpCount,self.time,self.index)


    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()