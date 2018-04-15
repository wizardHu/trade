import time

class Transaction:
    price = 0.0
    index = 0
    amount = 0.0
    orderId = 0
    isSpecial = 0
    
    def __init__(self,price,index,amount,orderId,isSpecial):
        self.price = price
        self.amount = amount
        self.orderId = orderId
        self.isSpecial = isSpecial
        timestamp = int(index)/1000
        time_local = time.localtime(timestamp)
#         self.index = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        self.index = index
        
    def getValue(self):
        return "{},{},{},{},{}".format(self.price,self.amount,self.orderId,self.index,self.isSpecial)
        
    def printTransaction(self):
        print('price={} index={} amount={} orderId={} isSpecial={}'.format(self.price,self.index,self.amount,self.orderId,self.isSpecial)) 
    
    def __str__(self):
        return "{}".format(self.price)
    
    def __repr__(self):
        return "{}".format(self.price)