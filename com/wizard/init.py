# -*- coding: utf-8 -*-
import HuobiService as huobi
import matplotlib.pyplot as plt

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

#     plt.text(tempx, tempy, "sss %s %s" % (tempx,tempy))  
#     plt.plot(tempx,tempy,'ro',color='red' )
    plt.plot(klinex, kliney, label='xrpusdt')
   
    plt.legend()
    plt.show()