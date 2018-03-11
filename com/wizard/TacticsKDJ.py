# -*- coding: utf-8 -*-
import HuobiService as huobi
import Point as point


# data = {u'count': 7, u'vol': 749.703232, u'high': 0.736, u'amount': 1018.77,
#         u'low': 0.7348, u'close': 0.7348, u'open': 0.7352, u'id': 1518072240}


lastK = [50]
lastD = [50]
lastJ = [50]
lastBuy = 0;
last100 = []

def judgeBuy(data,index):
    
    global lastK
    global lastD
    global lastJ
    global last100
    isBuy = False
    
    Cn = data['close']
    Ln = data['low']
    Hn = data['high']
    if Hn==Ln:
        False
        
    RSV = (Cn-Ln)/(Hn-Ln)*100 
    K = 2.0/3*lastK[-1]+1.0/3*RSV
    D = 2.0/3*lastD[-1]+1.0/3*K
    J = 3*K-2*D
    
    if K<D and lastK[-1]>lastD[-1]  and D-K>1  and lastK[-1]-lastD[-1]>1: #普通下穿
        p1=point.Point(index-1,lastK[-1])
        p2=point.Point(index,K)
        line1=point.Line(p1,p2)
        
        p3=point.Point(index-1,lastD[-1])
        p4=point.Point(index,D)
        line2=point.Line(p3,p4)
        
        pointXY = point.GetCrossPoint(line1, line2)
        if pointXY.y < 60:
            isBuy = True
    
    if len(lastJ) >= 2: # J 连续为负数3个周期
        if lastJ[-1] < 0  and lastJ[-2] < 0 and J < 0 :
            isBuy = True
    
    
    if K>55 and D>55 or abs(J-lastJ[-1])<30:
        isBuy = False
        
    if isBuy:
        if len(last100) > 1 and Cn >= last100[-1] :
            isBuy = False
    
#     if len(last100)>90 and Cn <= last100[0]:
#         isBuy = True
    
    
    lastK.append(K)
    lastJ.append(J)
    lastD.append(D)
    
    
    if len(lastK)>10:
        lastK = lastK[1:]
        lastD = lastD[1:]
        lastJ = lastJ[1:]
    
    
    last100.append(data['close'])
    last100.sort()
    if len(last100) >101:
        last100 = last100[1:]
    
    return isBuy


if __name__ == '__main__':
    test = huobi.get_kline('eosusdt','1min',100)
    test['data'].reverse()
    
    for i in test['data']:
        judgeBuy(i,test['data'].index(i))
    
    

    
    