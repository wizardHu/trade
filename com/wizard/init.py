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


if __name__ == '__main__':
    
    test = huobi.get_kline('xrpusdt','1min',1200)
    test['data'].reverse()
  
    klineXY = get_kline_xy(test['data'])
    klinex = klineXY[0]
    kliney = klineXY[1]
    
    MA60XY = get_MA(test['data'],60)
    MA30XY = get_MA(test['data'],30)
    MA10XY = get_MA(test['data'],10)

#     plt.text(tempx, tempy, "sss %s %s" % (tempx,tempy))  
#     plt.plot(tempx,tempy,'ro',color='red' )
    plt.plot(klinex, kliney, label='xrpusdt')
    plt.plot(MA60XY[0], MA60XY[1], label='ma60')
    plt.plot(MA30XY[0], MA30XY[1], label='ma30')
    plt.plot(MA10XY[0], MA10XY[1], label='ma10')
   
    plt.legend()
    plt.show()