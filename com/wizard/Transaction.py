import time

class Transaction:
    price = 0.0
    index = 0
    amount = 0.0
    orderId = 0
    
    def __init__(self,price,index,amount,orderId):
        self.price = price
        self.amount = amount
        self.orderId = orderId
        timestamp = int(index)/1000
        time_local = time.localtime(timestamp)
        self.index = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        
    def getValue(self):
        return "{},{},{},{}".format(self.price,self.amount,self.orderId,self.index)
        
    def printTransaction(self):
        print('price={} index={} amount={} orderId={}'.format(self.price,self.index,self.amount,self.orderId)) 