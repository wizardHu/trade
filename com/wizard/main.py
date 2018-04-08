# -*- coding: utf-8 -*-
import HuobiService as huobi
import TacticsKDJ as tac
import TacticsAVG as tacAvg
import TacticsRSI as tacRsi  
import TacticsAmount as tacAmount
import TacticsBoll as tacBoll
import globalUtil as constant
import Client as client
import aaa as aa
import time

balance = 0
lastBuy = 0
packageBuy = []
buynum = 0;
buyx = []
buyy = []
sendx = []
sendy = []

lastK = 50
lastD = 50
lastJ = 50

buy = 0


def get_KDJ(i,index):
    global balance
    global lastBuy
    global packageBuy
    global buynum
    global buyx
    global buyy
    global sendx 
    global sendy
    global lastK
    global lastD
    global lastJ
    global buy
   
        
    Cn = i['close']
    Ln = i['low']
    Hn = i['high']
    
    constant.add(i, index)#
    
    K = 50
    D = 50
    J = 50
    
    if Hn!=Ln:
       
        RSV = (Cn-Ln)/(Hn-Ln)*100 
        
        K = 2.0/3*lastK+1.0/3*RSV
        D = 2.0/3*lastD+1.0/3*K
        J = 3*K-2*D        
     
    avgFlag = tacAvg.avgJudgeBuy(i,index) 
    amountFlag = tacAmount.amountJudgeBuy(i,index)
    kdjFlag = tac.judgeBuy(i,index)
    lowest = tacAmount.isLowest(i['close']);
    rsiflag = tacRsi.rsiJudgeBuy(i, index, 12)
    
    if constant.nextBuy == 1:
        constant.nextBuy = 0
        if constant.canBuy():
            buyx.append(index)
            buyy.append(i['close'])
            balance -= i['close']
            lastBuy = i['close']
                  
            constant.buyPackage.append(lastBuy)
            print ('购买',i['close'],'余额',balance,"index=",index)
    
    elif avgFlag and buy == 0 and amountFlag:
        if kdjFlag and rsiflag :
            buyx.append(index)
            buyy.append(i['close'])
            balance -= i['close']
            lastBuy = i['close']
            constant.buyPackage.append(lastBuy)

            print ('购买',i['close'],'余额',balance)
        elif lowest  and tacAmount.judgeRisk(index)   and tacBoll.judgeBoll(i['close']):
            constant.nextBuy = 1
        
    if check_sell(K, D, J, lastK, lastD, lastJ, i['close'], buy):
        
        listPrice = constant.canSell(i['close'])
        
        if len(listPrice) > 0:
            constant.sell(listPrice)
        
            buy = 0
            sendx.append(index)
            sendy.append(i['close'])
            
            balance += (len(listPrice)*i['close']*0.998)
            buynum = 0
            print ('卖出',listPrice,'单价：',i['close'],'余额',balance,'\n')
    
    lastK = K
    lastD = D
    lastJ = J
    


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
   
    
    while True:
        
        try:
            test = huobi.get_kline('eosusdt','1min',1)
            test['data'].reverse()
#             test = client.getKline(1,"eos_usdt")
            print(test['data'])
#             time.sleep(5)
        except:
            print('connect ws error,retry...')
            time.sleep(5)
  
    count = 0
    for i in test['data']:
        get_KDJ(i,count)
        count += 1
  
     
    balance += (len(constant.buyPackage)*constant.prices[-1]*0.998)
    print ('卖出',constant.buyPackage,'单价：',constant.prices[-1],'余额',balance,'\n')
    constant.buyPackage = []
      
    print (balance)
    print (constant.buyPackage)
    
    
    
     
    
    
    