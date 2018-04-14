# -*- coding: utf-8 -*-
import HuobiService as huobi
import TacticsKDJ as tac
import TacticsAVG as tacAvg
import TacticsRSI as tacRsi  
import TacticsAmount as tacAmount
import TacticsBoll as tacBoll
import globalUtil as constant
import time
import MyHuobiService as myHuo

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
    global lastBuy
    global packageBuy
    global buynum
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
        if constant.juideGap():
            lastBuy = i['close']
            
            #挂单
            
            constant.buyPackage.append(lastBuy)
            print ('购买',i['close'],"index=",index)
    
    elif avgFlag and buy == 0 and amountFlag:
        if kdjFlag and rsiflag :
            lastBuy = i['close']
            constant.buyPackage.append(lastBuy)
            
            #挂单
            
            print ('购买',i['close'] )
        elif lowest  and tacAmount.judgeRisk(index)   and tacBoll.judgeBoll(i['close']):
            constant.nextBuy = 1
        
    if check_sell(K, D, J, lastK, lastD, lastJ,  buy):
        
        listPrice = constant.canSell(i['close'])
        
        if len(listPrice) > 0:
            constant.sell(listPrice)
        
            buy = 0
            sendx.append(index)
            sendy.append(i['close'])
            
            
            buynum = 0
            
            #挂单
            print ('卖出',listPrice,'单价：',i['close']  ,'\n')
    
    lastK = K
    lastD = D
    lastJ = J
    


def check_sell(K,D,J,lastK,lastD,lastJ,buy):
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
   
    
#     while True:
#         
#         lastId = 0
#         count = 0
#         
#         try:
#             test = huobi.get_kline('eosusdt','1min',1)
#             test['data'].reverse()
#             print(test['data'])
#             
#             if lastId != test['data'][0]['id']:
#                 get_KDJ(test['data'][0],count)
#                 count += 1
#             
#             time.sleep(1)
#         except:
#             print('connect ws error,retry...')
#             time.sleep(5)
    
#     print(huobi.get_balance())
#     print(huobi.send_order(1, "api", "xrpusdt", "buy-limit", "0.4820"))
    orders = myHuo.getAllOrder("eosusdt")
    for order in orders:
        order.printTransaction()

    
    
    