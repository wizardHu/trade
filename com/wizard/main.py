# -*- coding: utf-8 -*-
import HuobiService as huobi
import TacticsKDJ as tac
import TacticsAVG as tacAvg
import TacticsRSI as tacRsi  
import TacticsAmount as tacAmount
import TacticsBoll as tacBoll
import globalUtil as constant
import time
import logging

# 1.初始化日志默认配置
logging.basicConfig(filename='./my.log',                                                 # 日志输出文件
                    level=logging.INFO,                                                 # 日志写入级别
                    datefmt='%Y-%m-%d %H:%M:%S',                                         # 时间格式
                    format='%(asctime)s Line:%(lineno)s==>%(message)s')    # 日志写入格式

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


def get_KDJ(i,index,evn):
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
    allGap = constant.juideAllGap(i['close'],'pro')
    risk = tacAmount.judgeRisk(index)
    gap = constant.juideGap()
    boll = tacBoll.judgeBoll(i['close'])
    
    if evn == 'init':
        return
    
    logging.info("avgFlag={} amountFlag={} allGap={} kdjFlag={} rsiflag={}  lowest={}  risk={}  boll={} gap={} nextBuy={} \n"
          .format(avgFlag,amountFlag,allGap, kdjFlag,rsiflag,lowest,risk,boll,gap,constant.nextBuy))
    
    if constant.nextBuy == 1:
        constant.nextBuy = 0
        if gap:
            lastBuy = i['close']
            
            constant.sendBuy('pro', 1, i['close'], 'eosusdt')
            logging.info('购买',i['close'],"index=",index)
    
    elif avgFlag and buy == 0 and amountFlag and allGap:
        if kdjFlag and rsiflag :
            lastBuy = i['close']
            constant.sendBuy('pro', 1, i['close'], 'eosusdt')
            
            logging.info('购买',i['close'] )
        elif lowest  and risk   and boll and allGap:
            constant.nextBuy = 1
    
    ckeckSell = check_sell(K, D, J, lastK, lastD, lastJ,  buy)
    logging.info("ckeckSell={} K={}, D={}, J={}, lastK={}, lastD={}, lastJ={},  buy={}".format(ckeckSell,K, D, J, lastK, lastD, lastJ,  buy))
    
    if ckeckSell:
        
        transactions = constant.canSell('pro',i['close'])
        logging.info("transactions={}".format(transactions))
        
        if len(transactions) > 0:
            constant.sell('pro',transactions)
        
            buy = 0
            sendx.append(index)
            sendy.append(i['close'])
            
            buynum = 0
            
            logging.info('卖出',transactions,'单价：',i['close']  ,'\n')
    
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
   
    test = huobi.get_kline('eosusdt','1min',1200)
    test['data'].reverse()
    for i in test['data']:  
        get_KDJ(i,test['data'].index(i),'init')
    
    lastId = 0
    count = 0
    lastDate = huobi.get_kline('eosusdt','1min',1)
    
    while True:
         
        try:
            test = huobi.get_kline('eosusdt','1min',1)
            test['data'].reverse()
            logging.info(test['data'])
            
            if lastId != test['data'][0]['id'] : 
                
                logging.info(lastDate['data'])
                get_KDJ(lastDate['data'][0],count,'pro')
                count += 1
                 
                lastId = test['data'][0]['id']
                
            lastDate = test
            time.sleep(1)
        except:
            logging.info('connect https error,retry...')
            time.sleep(5)
     
    
    
    