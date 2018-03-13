# -*- coding: utf-8 -*-

import numpy as np

amount = []
uplow = []
prices = []

def amountJudgeBuy(data,index):
    global amount
    global uplow
    global prices
    
    volsma5 = 0
    volsma10 = 0
    
    deal = data['amount']
    price = data['close']
    
    close = data['close']
    open = data['open']
    up = 1
    
    if close <= open :
        up = 0
    
    
    print deal,"======",index,"==",up
    
    amount.append(deal)
    uplow.append(up)
    prices.append(price)
    
    if len(amount) > 100:
        amount = amount[1:]
        uplow = uplow[1:]
        prices = prices[1:]
    
    if len(amount) >= 5:
        list5 = amount[-5:]
        volsma5 = np.mean(list5)
    
    if len(amount) >= 10:
        list10 = amount[-10:]
        volsma10 = np.mean(list10)
    
    avg = (volsma5 + volsma10)/2
    
    if avg > deal:
        return False
    
    return True

def isLowest(price,exchangeamount):
    global amount
    global uplow
    global prices
    
    if len(prices)<90:
        return False
    
    for i in prices:
        if i < price:
            return False
    
    for i in amount:
        index = amount.index(i)
        if uplow[index] == 0:
            if i > exchangeamount:
                return False
    
    return True
    
if __name__ == '__main__':
    amountJudgeBuy(1,2)


