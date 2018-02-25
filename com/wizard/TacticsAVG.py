# -*- coding: utf-8 -*-

price = []

def avgJudgeBuy(data,index):
    global price
    
    Cn = data['close']
    
    price.append(Cn)
    
    if len(price) > 100:
        price = price[1:]
    
    count = 0.0
    for p in price:
        count += p
    
    avg = round(count/len(price),2)
    
    print avg,"==========",Cn,index
    
    if len(price)<=5:
        return False
    
    if avg<=Cn  :
        return False
    
    return True