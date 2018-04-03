# -*- coding: utf-8 -*-

import numpy as np

prices = []
amount = []

buyPackage = []
wait = 0
nextBuy = 0
ma10 = []
closeGap = []

def add(data,index):
    global prices
    global amount
    global ma10
    global closeGap
    
    Cn = data['close']
    prices.append(Cn)
    
    deal = data['amount']
    amount.append(deal)
    
    if len(prices)>1:
        gap = prices[-1] - prices[-2]
        closeGap.append(gap)
    
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
        closeGap = closeGap[1:]
        
    
def canSell(price):
    global buyPackage
    global wait
    global ma10
    global closeGap
    
    listPrice = []
    
    for buyPrice in buyPackage:
        if buyPrice*1.007 <= price:
            ma = ma10[-2:]
            if len(ma) > 1:
                if ma[0] >= ma[1]:
                    listPrice.append(buyPrice) 
                elif wait==0:
                    wait+=1
                    print (price ,"wait")
                elif wait == 1:
                    wait = 0
                    listPrice.append(buyPrice) 
    
    flag = True
    for gap in closeGap[-50:]:
        if closeGap[-1] < gap:
            flag = False
    
    if flag:
        listPrice.clear()
        wait = 1
    
    return listPrice

def sell(priceList):
    global buyPackage
    
    for price in priceList:
        buyPackage.remove(price)
        
def getMa(period):
    global prices
    
    count = 0.0
    
    if len(prices) >= period:
        lists = prices[(-1*period):]
        for p in lists:
            count += p
    
    return round(count/period,2)   

def canBuy():
    global prices
    
    curPrice = prices[-1]
    lastPrice = prices[-2]
    
    if curPrice <= lastPrice:
        return True
    else:
        gap = curPrice - lastPrice
        times = gap/lastPrice
        if times < 0.002:
            return True
    
    return False
        
    