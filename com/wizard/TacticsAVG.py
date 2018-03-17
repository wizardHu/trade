# -*- coding: utf-8 -*-

price = []

def avgJudgeBuy(data,index):
    global price
    
    Cn = data['close']
    
    price.append(Cn)
    
    if len(price) > 50:
        price = price[1:]
    
    ma10 = getMa(10)
    ma30 = getMa(30)
     
    if ma30 <= ma10 or ma30 == 0 or ma10 == 0:
        return False
     
    if Cn >= ma10:
        return False
    
    return True

def getMa(period):
    global price
    
    count = 0.0
    
    if len(price) >= period:
        lists = price[(-1*period):]
        for p in lists:
            count += p
    
    return round(count/period,2)


if __name__ == '__main__':
    price.append(1)
    price.append(2)
    price.append(3)
    price.append(4)
    price.append(5)
    print getMa(20)
    
    