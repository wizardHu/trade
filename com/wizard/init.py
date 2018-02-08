# -*- coding: utf-8 -*-
import HuobiService as huobi
import Tactics001 as tac
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator
from matplotlib.ticker import  FormatStrFormatter

balance = 10
lastBuy = 0
packageBuy = []
buynum = 0;

def get_MA(datas,count):
    
    list = []
    x = []
    y = []
    xy = []
        
    for data in datas:
        index = datas.index(data)
        close = data['close']
        
        list.insert(0, close)
        if len(list)>count:
            list.pop()

        if len(list)==count:
            priceCount = 0
            for price in list:
                priceCount += price
            
            ma = priceCount/count
            y.append(ma)
            x.append(index)    

    xy.append(x)
    xy.append(y)
    
    return xy
    
#得到K线图的xy
def get_kline_xy(data):
    xy = [0]*2
  
    x = []
    y = []
  
    for i in data:
        x.append(data.index(i))
        y.append(i['close'])

    xy[0] = x
    xy[1] = y
    return xy


def get_KDJ(data):
    global balance
    global lastBuy
    global packageBuy
    global buynum
    KDJ = []
    KXY = []
    DXY = []
    JXY = []
    
    x = []
    ky = []
    dy = []
    jy = []
    
    BUYXY = []
    SENDXY = []
    
    buyx = []
    buyy = []
    sendx = []
    sendy = []
    
    lastK = 50
    lastD = 50
    lastJ = 50
    
    buy = 0
    send = 0
    
    for i in data:
         
        Cn = i['close']
        Ln = i['low']
        Hn = i['high']
        if Hn==Ln:
            continue
        RSV = (Cn-Ln)/(Hn-Ln)*100 
        
        K = 2.0/3*lastK+1.0/3*RSV
        D = 2.0/3*lastD+1.0/3*K
        J = 3*K-2*D        
         
        x.append(data.index(i))
        ky.append(K)
        dy.append(D)
        jy.append(J)
        
        if tac.judgeBuy(i,data.index(i)) and buy == 0:
            buy= 1
         
            buyx.append(data.index(i))
            buyy.append(i['close'])
            balance -= i['close']
            lastBuy = i['close']
            buynum= 0.998
            
            print '购买',i['close'],'余额',balance
            
        if check_send(K, D, J, lastK, lastD, lastJ, i['close'], buy):
            buy = 0
            sendx.append(data.index(i))
            sendy.append(i['close'])
            balance += (buynum*i['close']*0.98)
            buynum = 0
            print '卖出',i['close'],'余额',balance,'\n'
        
        lastK = K
        lastD = D
        lastJ = J
    
    BUYXY.append(buyx)
    BUYXY.append(buyy)
    SENDXY.append(sendx)
    SENDXY.append(sendy)
        
    KXY.append(x)
    KXY.append(ky)
    
    DXY.append(x)
    DXY.append(dy)
    
    JXY.append(x)
    JXY.append(jy)
    
    KDJ.append(KXY)
    KDJ.append(DXY)
    KDJ.append(JXY)
    KDJ.append(BUYXY)
    KDJ.append(SENDXY)
    
    return KDJ



def check_send(K,D,J,lastK,lastD,lastJ,close,buy):
    global lastBuy
    global buynum
    isSend = False
    if buy== 1:
        
        if (D>K and lastK>lastD  or J>100 ) :
            isSend = True
        
        if J < lastJ and J>50:
            isSend = True
        
        gap = (buynum*close*0.998) - lastBuy*1.002
        if isSend:
            print buynum,close,lastBuy,gap
        
        
        if gap<0:
            isSend = False
        
    return isSend

if __name__ == '__main__':
    
    fig = plt.figure()
    test = huobi.get_kline('eosusdt','1min',100)
    test['data'].reverse()
    
    xmajorLocator = MultipleLocator(1);
  
    klineXY = get_kline_xy(test['data'])
    klinex = klineXY[0]
    kliney = klineXY[1]
    
    MA60XY = get_MA(test['data'],60)
    MA30XY = get_MA(test['data'],30)
    MA10XY = get_MA(test['data'],10)

    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    KDJ = get_KDJ(test['data'])

    ax1.plot(klinex, kliney, label='xrpusdt')
#     ax1.plot(MA60XY[0], MA60XY[1], label='ma60')
#     ax1.plot(MA30XY[0], MA30XY[1], label='ma30')
#     ax1.plot(MA10XY[0], MA10XY[1], label='ma10')
    ax1.scatter(KDJ[3][0], KDJ[3][1],marker = 'x', color = 'm', label='1' )
    ax1.scatter(KDJ[4][0], KDJ[4][1], label='1' )
    ax1.xaxis.set_major_locator(xmajorLocator)
    
    ax2.plot(KDJ[0][0], KDJ[0][1], color="red")
    ax2.plot(KDJ[1][0], KDJ[1][1], color='blue')
    ax2.plot(KDJ[2][0], KDJ[2][1], color='green')
    ax2.xaxis.set_major_locator(xmajorLocator)
   
    print balance
   
    ax1.grid(linestyle='--')
    ax2.grid(linestyle='--')
    plt.show()
    
     
    
    
    