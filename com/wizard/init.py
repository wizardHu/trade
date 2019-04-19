# -*- coding: utf-8 -*-
import HuobiService as huobi
import TacticsKDJ as tac
import TacticsAVG as tacAvg
import TacticsRSI as tacRsi  
import TacticsAmount as tacAmount
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator
from matplotlib.ticker import  FormatStrFormatter
from audioop import avg
import TacticsBoll as tacBoll
import CalAmount as calAmounts
import globalUtil as constant
import aaa as aa
import Client as client
import time

balance = 0
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


def get_KDJ(data,symbols):
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
    BOLLUPXY = []
    BOLLDOWNXY = []
    
    buyx = []
    buyy = []
    sendx = []
    sendy = []
    
    bollx = []
    bolldowny = []
    bollupy = []
    
    lastK = 50
    lastD = 50
    lastJ = 50
    
    buy = 0
    send = 0
    
    for i in data:
        
        
        Cn = i['close']
        Ln = i['low']
        Hn = i['high']
        
        constant.add(i, data.index(i))
        tacRsi.getrsi(i, data.index(i), 12)
        bollxy = tacBoll.getBoll(20, 2)
        if len(bollxy)>1:
            bollx.append(data.index(i))
            bollupy.append(bollxy[0])
            bolldowny.append(bollxy[1])
        
        K = 50
        D = 50
        J = 50
        
        if Hn!=Ln:
           
            RSV = (Cn-Ln)/(Hn-Ln)*100 
            
            K = 2.0/3*lastK+1.0/3*RSV
            D = 2.0/3*lastD+1.0/3*K
            J = 3*K-2*D        
         
        x.append(data.index(i))
        ky.append(K)
        dy.append(D)
        jy.append(J)
        
        avgFlag = tacAvg.avgJudgeBuy(i,data.index(i)) 
        amountFlag = tacAmount.amountJudgeBuy(i,data.index(i))
        kdjFlag = tac.judgeBuy(i,data.index(i))
        lowest = tacAmount.isLowest(i['close']);
        isfastLowAmount = tacAmount.isfastLowAmount( i['amount']);
        rsiflag = tacRsi.rsiJudgeBuy(i, data.index(i), 12)
        allGap = constant.juideAllGap(i['close'],'dev',symbols)
        isHighPrice = constant.isLagerBigger(i['close'])

        # print("index=",data.index(i)," avgFlag=",avgFlag," kdjFlag=",kdjFlag," rsi=",rsiflag," allGap=",allGap," isHighPrice=",isHighPrice)

        if constant.nextBuy == 1:
            constant.nextBuy = 0
            if constant.juideGap():
                buyx.append(data.index(i))
                buyy.append(i['close'])
#                 constant.buyPackage.append
                shouldBuy = constant.getShouldByAmount(i['close'],symbols)
                if shouldBuy>0:
                    constant.sendBuy('dev', shouldBuy, i['close'], symbols)
                    balance -= (i['close'] * shouldBuy)
                    lastBuy = i['close']
                    constant.writeTradeRecord(('1 {} {} {}').format(i['close'], shouldBuy,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())));
                    print ('购买', i['close'],' 个数=',shouldBuy, '余额', balance," 平均价=",constant.getBuyPriceAVG(symbols), "index=", data.index(i))

        elif avgFlag and buy == 0  and allGap and isHighPrice:
            if kdjFlag and rsiflag :
                buyx.append(data.index(i))
                buyy.append(i['close'])

#                 constant.buyPackage.append(lastBuy)
                shouldBuy = constant.getShouldByAmount(i['close'],symbols)
                if shouldBuy > 0:
                    constant.sendBuy('dev', shouldBuy, i['close'], symbols)
                    balance -= (i['close'] * shouldBuy)
                    lastBuy = i['close']
                    constant.writeTradeRecord(('1 {} {} {}').format(i['close'], shouldBuy,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())));
                    print ('购买', i['close'], ' 个数=', shouldBuy, '余额', balance," 平均价=",constant.getBuyPriceAVG(symbols), "index=", data.index(i))


            elif lowest  and tacAmount.judgeRisk(data.index(i)) and tacBoll.judgeBoll(i['close']) and allGap:
                constant.nextBuy = 1#下一期买

        if check_sell(K, D, J, lastK, lastD, lastJ, i['close'], buy):
            
            transactions = constant.canSellv2('dev',i['close'],symbols)
            
            if len(transactions) > 0:
                constant.sell('dev',transactions,symbols)
            
                buy = 0
                sendx.append(data.index(i))
                sendy.append(i['close'])

                sellCount = 0;

                for transaction in transactions:
                    sellCount = sellCount + float(transaction.amount);

                balance += (sellCount*i['close']*0.998)
                buynum = 0
                
                print ('卖出',transactions," 总数=",sellCount,'单价：',i['close'],'余额',balance,'\n')
        
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
    
    BOLLUPXY.append(bollx)
    BOLLUPXY.append(bollupy)
    
    BOLLDOWNXY.append(bollx)
    BOLLDOWNXY.append(bolldowny)
    
    KDJ.append(KXY)
    KDJ.append(DXY)
    KDJ.append(JXY)
    KDJ.append(BUYXY)
    KDJ.append(SENDXY)
    KDJ.append(RSIXY)
    KDJ.append(BOLLUPXY)
    KDJ.append(BOLLDOWNXY)
    
    
    return KDJ



def check_sell(K,D,J,lastK,lastD,lastJ,close,buy):
    global lastBuy
    global buynum
    isSend = False
    if buy== 0:
        
        if (D<K and lastK<lastD  or J>100 ) :
            isSend = True
        
        if J < lastJ and J>50 and J>K:
            isSend = True
        
    return isSend

if __name__ == '__main__':
   
    fig = plt.figure()
    symbols = 'htusdt'
    test = huobi.get_kline(symbols,'15min',1000)
    # test = aa.test0
    
    test['data'].reverse()
#     test = client.getKline(1200,"eos_usdt")
    
    xmajorLocator = MultipleLocator(10);
  
    klineXY = get_kline_xy(test['data'])
    klinex = klineXY[0]
    kliney = klineXY[1]
    
    MA60XY = get_MA(test['data'],60)
    MA30XY = get_MA(test['data'],30)
    MA10XY = get_MA(test['data'],5)

    ax1 = fig.add_subplot(111)
#     ax2 = fig.add_subplot(112)
#     ax3 = fig.add_subplot(313)
    KDJ = get_KDJ(test['data'],symbols)

    ax1.plot(klinex, kliney, label=symbols)
    # ax1.plot(MA60XY[0], MA60XY[1], label='ma60')
    # ax1.plot(MA30XY[0], MA30XY[1], label='ma30')
    # ax1.plot(MA10XY[0], MA10XY[1], label='ma10')

#     ax1.plot(KDJ[6][0], KDJ[6][1], color='green',label='bollup')
#     ax1.plot(KDJ[7][0], KDJ[7][1], color='red',label='bolldown')
    
    ax1.scatter(KDJ[3][0], KDJ[3][1],marker = 'x', color = 'm', label='1' )
    ax1.scatter(KDJ[4][0], KDJ[4][1], label='1' , color = 'red')
    ax1.xaxis.set_major_locator(xmajorLocator)
    
#     ax2.plot(KDJ[0][0], KDJ[0][1], color="red")
#     ax2.plot(KDJ[1][0], KDJ[1][1], color='blue')
#     ax2.plot(KDJ[2][0], KDJ[2][1], color='green')
#     ax2.plot(KDJ[5][0], KDJ[5][1], color='green')
#     ax2.xaxis.set_major_locator(xmajorLocator)
#     ax3.xaxis.set_major_locator(xmajorLocator)

    buyPackage = constant.getBuyPackage(symbols)
    count = 0
    for tran in buyPackage:
        count = count + float(tran.amount)

    balance += (count*constant.prices[-1]*0.998)
    print ('卖出',constant.getBuyPackage(symbols),'单价：',constant.prices[-1],'余额',balance,'\n')
    constant.buyPackage = []
    constant.delAll()
    
    print (balance)
    print (constant.buyPackage)
   
    ax1.grid(linestyle='--')
#     ax2.grid(linestyle='--')
#     ax3.grid(linestyle='--')

#     calAmounts.calAmount(test['data'])
    
    plt.show()
    
     
    
    
    