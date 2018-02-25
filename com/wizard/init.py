# -*- coding: utf-8 -*-
import HuobiService as huobi
import TacticsKDJ as tac
import TacticsAVG as tacAvg
import TacticsRSI as tacRsi
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
    
    RSIXY = []
    
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
        
        tacRsi.rsiJudgeBuy(i, data.index(i), 12)
        
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
        
        flag = tacAvg.avgJudgeBuy(i,data.index(i))
#         flag = True
        if tac.judgeBuy(i,data.index(i)) and flag and buy == 0:
#             buy= 1
         
            buyx.append(data.index(i))
            buyy.append(i['close'])
            balance -= i['close']
            lastBuy = i['close']
            buynum= 0.998
            
#             print '购买',i['close'],'余额',balance
            
        if check_send(K, D, J, lastK, lastD, lastJ, i['close'], buy):
            buy = 0
            sendx.append(data.index(i))
            sendy.append(i['close'])
            balance += (buynum*i['close']*0.998)
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
    
    RSIXY.append(tacRsi.X)
    RSIXY.append(tacRsi.Y)
    
    KDJ.append(KXY)
    KDJ.append(DXY)
    KDJ.append(JXY)
    KDJ.append(BUYXY)
    KDJ.append(SENDXY)
    KDJ.append(RSIXY)
    
    print RSIXY
    
    return KDJ



def check_send(K,D,J,lastK,lastD,lastJ,close,buy):
    global lastBuy
    global buynum
    isSend = False
    if buy== 1:
        
        if (D<K and lastK<lastD  or J>100 ) :
            isSend = True
        
        if J < lastJ and J>50 and J>K:
            isSend = True
        
        gap = (buynum*close*0.998) - lastBuy*1.002
        
        if gap<0:
            isSend = False
        
    return isSend

if __name__ == '__main__':
    
    fig = plt.figure()
    test = {u'status': u'ok', u'ch': u'market.eosusdt.kline.1min', u'data': [{u'count': 6, u'vol': 22303.602389, u'high': 8.31, u'amount': 2687.0748, u'low': 8.3, u'close': 8.3, u'open': 8.31, u'id': 1519444680}, {u'count': 13, u'vol': 18481.67555, u'high': 8.3, u'amount': 2227.0185, u'low': 8.29, u'close': 8.3, u'open': 8.3, u'id': 1519444620}, {u'count': 14, u'vol': 17242.932873, u'high': 8.31, u'amount': 2076.8023, u'low': 8.29, u'close': 8.29, u'open': 8.3, u'id': 1519444560}, {u'count': 18, u'vol': 39024.811307, u'high': 8.32, u'amount': 4699.0462, u'low': 8.3, u'close': 8.3, u'open': 8.31, u'id': 1519444500}, {u'count': 29, u'vol': 13477.146292, u'high': 8.32, u'amount': 1621.0735, u'low': 8.31, u'close': 8.31, u'open': 8.31, u'id': 1519444440}, {u'count': 29, u'vol': 11692.984843, u'high': 8.32, u'amount': 1407.5552, u'low': 8.3, u'close': 8.31, u'open': 8.3, u'id': 1519444380}, {u'count': 40, u'vol': 25374.435041, u'high': 8.3, u'amount': 3059.9849, u'low': 8.28, u'close': 8.29, u'open': 8.29, u'id': 1519444320}, {u'count': 41, u'vol': 22955.728413, u'high': 8.3, u'amount': 2770.6006, u'low': 8.27, u'close': 8.29, u'open': 8.27, u'id': 1519444260}, {u'count': 23, u'vol': 29831.116054, u'high': 8.27, u'amount': 3613.6408, u'low': 8.25, u'close': 8.27, u'open': 8.27, u'id': 1519444200}, {u'count': 5, u'vol': 1585.094728, u'high': 8.28, u'amount': 191.8283, u'low': 8.26, u'close': 8.27, u'open': 8.26, u'id': 1519444140}, {u'count': 40, u'vol': 19933.385868, u'high': 8.27, u'amount': 2413.6633842805322, u'low': 8.25, u'close': 8.25, u'open': 8.26, u'id': 1519444080}, {u'count': 21, u'vol': 233426.751309, u'high': 8.26, u'amount': 28293.1353, u'low': 8.25, u'close': 8.26, u'open': 8.25, u'id': 1519444020}, {u'count': 1, u'vol': 725.868, u'high': 8.25, u'amount': 87.984, u'low': 8.25, u'close': 8.25, u'open': 8.25, u'id': 1519443960}, {u'count': 5, u'vol': 848.661475, u'high': 8.25, u'amount': 102.8923, u'low': 8.24, u'close': 8.25, u'open': 8.24, u'id': 1519443900}, {u'count': 7, u'vol': 74258.328734, u'high': 8.25, u'amount': 9001.516, u'low': 8.24, u'close': 8.25, u'open': 8.24, u'id': 1519443840}, {u'count': 31, u'vol': 23339.12505558, u'high': 8.24, u'amount': 2832.4543756771845, u'low': 8.23, u'close': 8.24, u'open': 8.24, u'id': 1519443780}, {u'count': 25, u'vol': 25761.57180742, u'high': 8.25, u'amount': 3124.8350243228156, u'low': 8.24, u'close': 8.24, u'open': 8.25, u'id': 1519443720}, {u'count': 21, u'vol': 23126.964526, u'high': 8.25, u'amount': 2804.3106, u'low': 8.24, u'close': 8.24, u'open': 8.25, u'id': 1519443660}, {u'count': 18, u'vol': 7920.34475, u'high': 8.25, u'amount': 960.4609, u'low': 8.24, u'close': 8.25, u'open': 8.25, u'id': 1519443600}, {u'count': 41, u'vol': 38813.594931, u'high': 8.28, u'amount': 4702.0414157384985, u'low': 8.24, u'close': 8.25, u'open': 8.26, u'id': 1519443540}, {u'count': 32, u'vol': 14918.563148, u'high': 8.3, u'amount': 1800.3302, u'low': 8.26, u'close': 8.28, u'open': 8.29, u'id': 1519443480}, {u'count': 65, u'vol': 86065.33510771, u'high': 8.3, u'amount': 10389.109612736145, u'low': 8.28, u'close': 8.29, u'open': 8.29, u'id': 1519443420}, {u'count': 74, u'vol': 58679.623971, u'high': 8.29, u'amount': 7088.7423, u'low': 8.27, u'close': 8.28, u'open': 8.27, u'id': 1519443360}, {u'count': 18, u'vol': 14128.399861305963, u'high': 8.26, u'amount': 1710.7776450733613, u'low': 8.25, u'close': 8.25, u'open': 8.26, u'id': 1519443300}, {u'count': 103, u'vol': 86035.87593422, u'high': 8.31, u'amount': 10414.004454285907, u'low': 8.22, u'close': 8.26, u'open': 8.23, u'id': 1519443240}, {u'count': 35, u'vol': 55331.40520779, u'high': 8.22, u'amount': 6744.698376495134, u'low': 8.19, u'close': 8.22, u'open': 8.2, u'id': 1519443180}, {u'count': 18, u'vol': 21904.651883, u'high': 8.2, u'amount': 2671.7086341463414, u'low': 8.19, u'close': 8.2, u'open': 8.2, u'id': 1519443120}, {u'count': 10, u'vol': 34204.709345, u'high': 8.2, u'amount': 4171.3554, u'low': 8.19, u'close': 8.2, u'open': 8.2, u'id': 1519443060}, {u'count': 19, u'vol': 24037.653347, u'high': 8.2, u'amount': 2934.229643902439, u'low': 8.19, u'close': 8.2, u'open': 8.2, u'id': 1519443000}, {u'count': 10, u'vol': 4549.75176, u'high': 8.2, u'amount': 555.1953, u'low': 8.19, u'close': 8.2, u'open': 8.19, u'id': 1519442940}, {u'count': 194, u'vol': 142171.9037988547, u'high': 8.2, u'amount': 17397.5802366896, u'low': 8.15, u'close': 8.19, u'open': 8.2, u'id': 1519442880}, {u'count': 46, u'vol': 52918.51012, u'high': 8.2, u'amount': 6453.476843902439, u'low': 8.2, u'close': 8.2, u'open': 8.2, u'id': 1519442820}, {u'count': 173, u'vol': 96410.861819, u'high': 8.23, u'amount': 11753.146587273106, u'low': 8.18, u'close': 8.2, u'open': 8.22, u'id': 1519442760}, {u'count': 68, u'vol': 64502.597503, u'high': 8.25, u'amount': 7834.688810904667, u'low': 8.22, u'close': 8.22, u'open': 8.25, u'id': 1519442700}, {u'count': 36, u'vol': 14329.287226, u'high': 8.25, u'amount': 1737.471, u'low': 8.24, u'close': 8.24, u'open': 8.25, u'id': 1519442640}, {u'count': 59, u'vol': 76211.286241, u'high': 8.25, u'amount': 9239.5561, u'low': 8.23, u'close': 8.25, u'open': 8.25, u'id': 1519442580}, {u'count': 65, u'vol': 35153.716193, u'high': 8.25, u'amount': 4265.868602787878, u'low': 8.23, u'close': 8.25, u'open': 8.25, u'id': 1519442520}, {u'count': 96, u'vol': 95439.831912, u'high': 8.26, u'amount': 11576.1081, u'low': 8.23, u'close': 8.25, u'open': 8.26, u'id': 1519442460}, {u'count': 56, u'vol': 45495.595257, u'high': 8.28, u'amount': 5505.427389371981, u'low': 8.26, u'close': 8.26, u'open': 8.27, u'id': 1519442400}, {u'count': 22, u'vol': 4855.847323, u'high': 8.28, u'amount': 586.5229, u'low': 8.26, u'close': 8.27, u'open': 8.28, u'id': 1519442340}, {u'count': 40, u'vol': 16698.423769, u'high': 8.28, u'amount': 2017.5521, u'low': 8.27, u'close': 8.28, u'open': 8.28, u'id': 1519442280}, {u'count': 32, u'vol': 25110.627619, u'high': 8.29, u'amount': 3032.5685, u'low': 8.27, u'close': 8.28, u'open': 8.29, u'id': 1519442220}, {u'count': 16, u'vol': 12261.57365, u'high': 8.3, u'amount': 1479.3682, u'low': 8.28, u'close': 8.29, u'open': 8.3, u'id': 1519442160}, {u'count': 20, u'vol': 35615.170484, u'high': 8.3, u'amount': 4293.3937, u'low': 8.28, u'close': 8.29, u'open': 8.3, u'id': 1519442100}, {u'count': 42, u'vol': 22331.309801196356, u'high': 8.3, u'amount': 2694.1540531561877, u'low': 8.28, u'close': 8.3, u'open': 8.29, u'id': 1519442040}, {u'count': 51, u'vol': 45047.783383, u'high': 8.31, u'amount': 5427.062479783393, u'low': 8.29, u'close': 8.29, u'open': 8.29, u'id': 1519441980}, {u'count': 58, u'vol': 28215.000965, u'high': 8.29, u'amount': 3407.6405, u'low': 8.27, u'close': 8.29, u'open': 8.28, u'id': 1519441920}, {u'count': 43, u'vol': 65593.18308077, u'high': 8.28, u'amount': 7923.484285479469, u'low': 8.26, u'close': 8.28, u'open': 8.28, u'id': 1519441860}, {u'count': 33, u'vol': 38948.712905, u'high': 8.28, u'amount': 4709.8268, u'low': 8.25, u'close': 8.28, u'open': 8.25, u'id': 1519441800}, {u'count': 42, u'vol': 66702.415028, u'high': 8.27, u'amount': 8077.4126, u'low': 8.24, u'close': 8.27, u'open': 8.27, u'id': 1519441740}, {u'count': 19, u'vol': 18248.197304968562, u'high': 8.28, u'amount': 2204.5384, u'low': 8.27, u'close': 8.27, u'open': 8.27, u'id': 1519441680}, {u'count': 119, u'vol': 80124.749053, u'high': 8.28, u'amount': 9697.683941233374, u'low': 8.25, u'close': 8.27, u'open': 8.26, u'id': 1519441620}, {u'count': 101, u'vol': 77589.243879, u'high': 8.31, u'amount': 9360.7342, u'low': 8.26, u'close': 8.28, u'open': 8.31, u'id': 1519441560}, {u'count': 22, u'vol': 20963.029435, u'high': 8.34, u'amount': 2517.7839, u'low': 8.31, u'close': 8.32, u'open': 8.34, u'id': 1519441500}, {u'count': 21, u'vol': 13173.421252, u'high': 8.34, u'amount': 1581.7074, u'low': 8.31, u'close': 8.34, u'open': 8.33, u'id': 1519441440}, {u'count': 43, u'vol': 27154.800068, u'high': 8.34, u'amount': 3263.9674, u'low': 8.31, u'close': 8.33, u'open': 8.32, u'id': 1519441380}, {u'count': 44, u'vol': 23615.959395, u'high': 8.35, u'amount': 2836.5714, u'low': 8.32, u'close': 8.32, u'open': 8.35, u'id': 1519441320}, {u'count': 78, u'vol': 78087.18364874, u'high': 8.37, u'amount': 9358.781559467145, u'low': 8.33, u'close': 8.35, u'open': 8.37, u'id': 1519441260}, {u'count': 24, u'vol': 22068.695609, u'high': 8.39, u'amount': 2637.0647, u'low': 8.36, u'close': 8.37, u'open': 8.36, u'id': 1519441200}, {u'count': 12, u'vol': 20715.696644, u'high': 8.39, u'amount': 2474.1778, u'low': 8.37, u'close': 8.37, u'open': 8.38, u'id': 1519441140}, {u'count': 11, u'vol': 25983.97214, u'high': 8.39, u'amount': 3101.5366, u'low': 8.37, u'close': 8.37, u'open': 8.39, u'id': 1519441080}, {u'count': 11, u'vol': 6235.442901, u'high': 8.4, u'amount': 743.0575, u'low': 8.39, u'close': 8.39, u'open': 8.4, u'id': 1519441020}, {u'count': 15, u'vol': 12845.05017463, u'high': 8.39, u'amount': 1532.588232375447, u'low': 8.38, u'close': 8.39, u'open': 8.39, u'id': 1519440960}, {u'count': 15, u'vol': 36511.343441, u'high': 8.39, u'amount': 4352.329235041716, u'low': 8.38, u'close': 8.39, u'open': 8.39, u'id': 1519440900}, {u'count': 35, u'vol': 26197.487316, u'high': 8.4, u'amount': 3122.7313, u'low': 8.38, u'close': 8.39, u'open': 8.38, u'id': 1519440840}, {u'count': 15, u'vol': 14422.667788, u'high': 8.4, u'amount': 1718.81, u'low': 8.39, u'close': 8.39, u'open': 8.39, u'id': 1519440780}, {u'count': 10, u'vol': 23919.628371, u'high': 8.39, u'amount': 2856.6819, u'low': 8.37, u'close': 8.39, u'open': 8.38, u'id': 1519440720}, {u'count': 10, u'vol': 12533.42348, u'high': 8.38, u'amount': 1496.9775353221958, u'low': 8.37, u'close': 8.38, u'open': 8.38, u'id': 1519440660}, {u'count': 19, u'vol': 13503.1330547, u'high': 8.38, u'amount': 1611.7742996062052, u'low': 8.37, u'close': 8.38, u'open': 8.38, u'id': 1519440600}, {u'count': 8, u'vol': 530.347119, u'high': 8.39, u'amount': 63.2568, u'low': 8.38, u'close': 8.38, u'open': 8.38, u'id': 1519440540}, {u'count': 13, u'vol': 10446.52376, u'high': 8.39, u'amount': 1246.6035, u'low': 8.37, u'close': 8.39, u'open': 8.37, u'id': 1519440480}, {u'count': 48, u'vol': 113340.050816, u'high': 8.38, u'amount': 13541.062951135005, u'low': 8.37, u'close': 8.38, u'open': 8.37, u'id': 1519440420}, {u'count': 17, u'vol': 53378.432342, u'high': 8.37, u'amount': 6377.781579330944, u'low': 8.36, u'close': 8.37, u'open': 8.36, u'id': 1519440360}, {u'count': 7, u'vol': 17055.493488, u'high': 8.36, u'amount': 2040.1308, u'low': 8.36, u'close': 8.36, u'open': 8.36, u'id': 1519440300}, {u'count': 22, u'vol': 32327.110526, u'high': 8.37, u'amount': 3866.58936953405, u'low': 8.36, u'close': 8.36, u'open': 8.36, u'id': 1519440240}, {u'count': 25, u'vol': 19308.006154, u'high': 8.37, u'amount': 2307.9063, u'low': 8.36, u'close': 8.36, u'open': 8.37, u'id': 1519440180}, {u'count': 22, u'vol': 11394.84423, u'high': 8.38, u'amount': 1360.8754, u'low': 8.37, u'close': 8.37, u'open': 8.37, u'id': 1519440120}, {u'count': 5, u'vol': 2610.931566, u'high': 8.39, u'amount': 311.5543, u'low': 8.38, u'close': 8.38, u'open': 8.39, u'id': 1519440060}, {u'count': 18, u'vol': 13130.42707, u'high': 8.39, u'amount': 1568.4724, u'low': 8.37, u'close': 8.38, u'open': 8.38, u'id': 1519440000}, {u'count': 8, u'vol': 7608.579513, u'high': 8.39, u'amount': 907.4769, u'low': 8.38, u'close': 8.38, u'open': 8.39, u'id': 1519439940}, {u'count': 53, u'vol': 60356.47035978853, u'high': 8.4, u'amount': 7206.321259617682, u'low': 8.36, u'close': 8.39, u'open': 8.38, u'id': 1519439880}, {u'count': 10, u'vol': 2503.370793, u'high': 8.38, u'amount': 298.9127, u'low': 8.37, u'close': 8.38, u'open': 8.38, u'id': 1519439820}, {u'count': 12, u'vol': 5201.011104, u'high': 8.4, u'amount': 620.3361, u'low': 8.38, u'close': 8.38, u'open': 8.4, u'id': 1519439760}, {u'count': 7, u'vol': 3640.44156, u'high': 8.4, u'amount': 433.3859, u'low': 8.4, u'close': 8.4, u'open': 8.4, u'id': 1519439700}, {u'count': 10, u'vol': 16560.891616, u'high': 8.41, u'amount': 1971.4898, u'low': 8.39, u'close': 8.39, u'open': 8.41, u'id': 1519439640}, {u'count': 32, u'vol': 19941.505769378953, u'high': 8.42, u'amount': 2372.3417049881236, u'low': 8.39, u'close': 8.41, u'open': 8.41, u'id': 1519439580}, {u'count': 21, u'vol': 35533.3840453, u'high': 8.42, u'amount': 4221.917579890612, u'low': 8.41, u'close': 8.41, u'open': 8.42, u'id': 1519439520}, {u'count': 15, u'vol': 25308.01155, u'high': 8.44, u'amount': 3001.6238, u'low': 8.43, u'close': 8.44, u'open': 8.43, u'id': 1519439460}, {u'count': 9, u'vol': 9668.615517, u'high': 8.44, u'amount': 1146.173, u'low': 8.43, u'close': 8.43, u'open': 8.44, u'id': 1519439400}, {u'count': 15, u'vol': 11664.837008, u'high': 8.45, u'amount': 1381.7194, u'low': 8.44, u'close': 8.44, u'open': 8.45, u'id': 1519439340}, {u'count': 17, u'vol': 8578.628953, u'high': 8.45, u'amount': 1016.569, u'low': 8.42, u'close': 8.45, u'open': 8.43, u'id': 1519439280}, {u'count': 58, u'vol': 59989.98614279241, u'high': 8.44, u'amount': 7122.903420759193, u'low': 8.41, u'close': 8.44, u'open': 8.43, u'id': 1519439220}, {u'count': 16, u'vol': 9310.689194, u'high': 8.44, u'amount': 1104.2158, u'low': 8.42, u'close': 8.43, u'open': 8.43, u'id': 1519439160}, {u'count': 18, u'vol': 12552.55043, u'high': 8.43, u'amount': 1489.847, u'low': 8.42, u'close': 8.43, u'open': 8.43, u'id': 1519439100}, {u'count': 14, u'vol': 17288.633048, u'high': 8.43, u'amount': 2052.7890792408066, u'low': 8.42, u'close': 8.42, u'open': 8.43, u'id': 1519439040}, {u'count': 8, u'vol': 15522.978012, u'high': 8.44, u'amount': 1841.22849478673, u'low': 8.43, u'close': 8.43, u'open': 8.43, u'id': 1519438980}, {u'count': 21, u'vol': 11182.574016, u'high': 8.44, u'amount': 1326.3812, u'low': 8.42, u'close': 8.43, u'open': 8.43, u'id': 1519438920}, {u'count': 23, u'vol': 55370.408925, u'high': 8.45, u'amount': 6561.4216, u'low': 8.42, u'close': 8.43, u'open': 8.45, u'id': 1519438860}, {u'count': 26, u'vol': 8362.170185, u'high': 8.45, u'amount': 991.1071, u'low': 8.43, u'close': 8.44, u'open': 8.45, u'id': 1519438800}, {u'count': 18, u'vol': 7586.670824, u'high': 8.45, u'amount': 899.8899, u'low': 8.42, u'close': 8.45, u'open': 8.42, u'id': 1519438740}], u'ts': 1519444708272L}
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
#     ax2.plot(KDJ[5][0], KDJ[5][1], color='green')
    ax2.xaxis.set_major_locator(xmajorLocator)
   
    print balance
   
    ax1.grid(linestyle='--')
    ax2.grid(linestyle='--')
    plt.show()
    
     
    
    
    