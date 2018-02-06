# -*- coding: utf-8 -*-
import HuobiService as huobi
import matplotlib.pyplot as plt

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
    KDJ = []
    KXY = []
    DXY = []
    JXY = []
    
    x = []
    ky = []
    dy = []
    jy = []
    
    lastK = 50
    lastD = 50
    
    for i in data:
        Cn = i['close']
        Ln = i['low']
        Hn = i['high']
        RSV = (Cn-Ln)/(Hn-Ln)*100 
        
        K = 2.0/3*lastK+1.0/3*RSV
        D = 2.0/3*lastD+1.0/3*K
        J = 3*K-2*D        
         
        x.append(data.index(i))
        ky.append(K)
        dy.append(D)
        jy.append(J)
        
        lastK = K
        lastD = D
    
    KXY.append(x)
    KXY.append(ky)
    
    DXY.append(x)
    DXY.append(dy)
    
    JXY.append(x)
    JXY.append(jy)
    
    KDJ.append(KXY)
    KDJ.append(DXY)
    KDJ.append(JXY)
    
    return KDJ


if __name__ == '__main__':
    
    fig = plt.figure()
    test = huobi.get_kline('btcusdt','1day',1200)
    test['data'].reverse()
  
    klineXY = get_kline_xy(test['data'])
    klinex = klineXY[0]
    kliney = klineXY[1]
    
    MA60XY = get_MA(test['data'],60)
    MA30XY = get_MA(test['data'],30)
    MA10XY = get_MA(test['data'],10)

    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    ax1.plot(klinex, kliney, label='xrpusdt')
    ax1.plot(MA60XY[0], MA60XY[1], label='ma60')
    ax1.plot(MA30XY[0], MA30XY[1], label='ma30')
    ax1.plot(MA10XY[0], MA10XY[1], label='ma10')
   
    KDJ = get_KDJ(test['data'])
    ax2.plot(KDJ[0][0], KDJ[0][1], color="red")
    ax2.plot(KDJ[1][0], KDJ[1][1], color='blue')
    ax2.plot(KDJ[2][0], KDJ[2][1], color='green')
   
   
    plt.show()
    
    
    