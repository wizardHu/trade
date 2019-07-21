class BuyModel:
    price = 0.0
    index = 0
    amount = 0.0
    orderId = 0
    minIncome = 0.0

    def __init__(self, price, index, amount, orderId,minIncome):
        self.price = price
        self.amount = amount
        self.orderId = orderId
        self.index = index
        self.minIncome = minIncome

    def getValue(self):
        return "{},{},{},{},{}".format(self.price, self.amount, self.orderId, self.index,self.minIncome)


    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()