class BuyModel:
    price = 0.0
    index = 0
    amount = 0.0
    orderId = 0

    def __init__(self, price, index, amount, orderId):
        self.price = price
        self.amount = amount
        self.orderId = orderId
        self.index = index

    def getValue(self):
        return "{},{},{},{}".format(self.price, self.amount, self.orderId, self.index)


    def __str__(self):
        return self.getValue()

    def __repr__(self):
        return self.getValue()