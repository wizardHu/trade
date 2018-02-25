# -*- coding: utf-8 -*-

X = []
Y = []
lastPrice = []

def rsiJudgeBuy(data,index,pre):
    global X
    global Y
    global lastPrice
    
    Cn = data['close']
    lastPrice.append(Cn)
    
    down = 0.0
    up = 0.0
    
    if len(lastPrice) > pre:
        listPrice = lastPrice[-(pre+1):]
        for i in range(len(listPrice)-1):
            print i
            if listPrice[i]>=listPrice[i+1]:#前面的比后面的大 跌
                down += (listPrice[i]-listPrice[i+1])
            
            if listPrice[i]<listPrice[i+1]:
                up += (listPrice[i+1] - listPrice[i])
    
        avgDown = down/pre
        avgUp = up/pre
        
        rsi = 50
        if avgUp!=0 or avgDown != 0:
            rsi = 100*avgUp/(avgUp+avgDown)
        
        X.append(index)
        Y.append(rsi)
        
    if len(lastPrice) >30:
        lastPrice = lastPrice[1:]
    
    