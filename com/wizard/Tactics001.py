# -*- coding: utf-8 -*-
import HuobiService as huobi
import Point as point
from inspect import isbuiltin


# data = {u'count': 7, u'vol': 749.703232, u'high': 0.736, u'amount': 1018.77,
#         u'low': 0.7348, u'close': 0.7348, u'open': 0.7352, u'id': 1518072240}

# 当k线数值高于90，同时D线数值高于80以上，并且J线数值连续三天高于100以上时，即称之为KDJ超买
# 当k线数值低于10以下，同时D线数值低于20以下，并且J线数值连续三天低于0以下时，即称之为KDJ超卖
# KDJ数值在40至60之间波动，KDJ三线互相反复粘合纠结，则被看作是多空平衡信号，属于股价暂时没有方向
# 若KDJ三线的金叉属于K值小于10，D值小于20，J值小于0，三线在超卖区形成的金叉
# 若KDJ三线的死叉属于K值大于90，D值大于80，J值大于100，三线在超买区形成的死叉时
# 当股价连续上涨一段时间，股价仍在继续向上创新高，而KDJ技术指标与紧相邻的前一高点相比较。并没有创新高。即股价创新高，KDJ并没有同时跟随创出新高时，即称之为KDJ顶背离，预示股价短期上涨乏力
# 指的是当股价连续下跌一段时间，股价仍在继续向下创新高，而KDJ技术指标与紧相邻的前一低点相比较。并没有创新低。即股价创新低，KDJ并没有同时跟随创出新低时，即称之为KDJ底背离

lastK = [50]
lastD = [50]
lastJ = [50]
lastBuy = 0;
last100 = [0]

def judgeBuy(data,index):
    
    print data['amount'],index
    
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
    
    if K<D and lastK[-1]>lastD[-1]  and D-K>2  and lastK[-1]-lastD[-1]>2: #普通下穿
        p1=point.Point(index-1,lastK[-1])
        p2=point.Point(index,K)
        line1=point.Line(p1,p2)
        
        p3=point.Point(index-1,lastD[-1])
        p4=point.Point(index,D)
        line2=point.Line(p3,p4)
        
        pointXY = point.GetCrossPoint(line1, line2)
        if pointXY.y < 55:
            isBuy = True
    
    if len(lastJ) >= 2: # J 连续为负数3个周期
        if lastJ[-1] < 0  and lastJ[-2] < 0 and J < 0 :
            isBuy = True
    
    
    if K>55 and D>55 or abs(J-lastJ[-1])<30:
        isBuy = False
        
    if isBuy:
        if Cn >= last100[-1]:
            isBuy = False
     
    
    lastK.append(K)
    lastJ.append(J)
    lastD.append(D)
    
    
    if len(lastK)>10:
        lastK = lastK[1:]
        lastD = lastD[1:]
        lastJ = lastJ[1:]
    
    
    last100.append(data['close'])
    last100.sort()
    if len(last100) >100:
        last100 = last100[1:]
    
    return isBuy


if __name__ == '__main__':
    test = huobi.get_kline('eosusdt','1min',100)
    test['data'].reverse()
    
    for i in test['data']:
        judgeBuy(i,test['data'].index(i))
    
    

    
    