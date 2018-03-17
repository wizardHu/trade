# -*- coding: utf-8 -*-

prices = []
amount = []

buyPackage = []
wait = 0
ma10 = []

def add(data,index):
    global prices
    global amount
    global ma10
    
    Cn = data['close']
    prices.append(Cn)
    
    deal = data['amount']
    amount.append(deal)
    
    count = 0.0
    if len(prices) > 10:
        lists = prices[(-10):]
        for p in lists:
            count += p
    
        ma = round(count/10,2)
        ma10.append(ma)
    
    if len(prices) >300:
        prices = prices[1:]
        amount = amount[1:]
        ma10 = ma10[1:]
        
    
def canSend(price):
    global buyPackage
    global wait
    global ma10
    
    listPrice = []
    
    for buyPrice in buyPackage:
        if buyPrice*1.007 <= price:
            ma = ma10[-2:]
            if len(ma) > 1:
                if ma[0] >= ma[1]:
                    listPrice.append(buyPrice) 
                elif wait==0:
                    wait+=1
                    print price ,"wait"
                elif wait == 1:
                    wait = 0
                    listPrice.append(buyPrice) 
    
    
    return listPrice

def send(priceList):
    global buyPackage
    
    for price in priceList:
        buyPackage.remove(price)
            
    