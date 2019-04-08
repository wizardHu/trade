# -*- coding: utf-8 -*-
import HuobiService as huobi
import aaa as aa


if __name__ == '__main__':
   
    test = huobi.get_kline('eosusdt','1min',500)
    print(test)
#     test = aa.test0
    
    test['data'].reverse()
    
    initPrice = test['data'][1]['close'];
    initCount = 200;
    initInput = initPrice*initCount;
    
    calInput = initPrice*initCount;
    
    balance = 0;
    nowCount = initCount;
    
    print("initPrice=",initPrice," initInput=",initInput)
    
    test['data'] = test['data'][1:]
   
    for i in test['data']:
        close = i['close'];
        
        nowBalance = nowCount * close;
        
        gap = calInput - nowBalance;
        
        if abs(gap)/calInput < 0.01:
            continue;
        
        if gap > 0:
            buy = gap/close;
            nowCount = nowCount + buy*0.998
            balance = balance - buy*close;
#             calInput = calInput + buy*close
            print("buy=",buy," nowCount=",nowCount," balance=",balance," avg=",(initInput-balance)/nowCount," close=",close," calInput=",calInput)
        
        if gap < 0:
            sell = abs(gap)/close;
            nowCount = nowCount - sell
            balance = balance + sell*close*0.998
#             calInput = calInput - sell*close*0.998
            print("sell=",sell," nowCount=",nowCount," balance=",balance," avg=",(initInput-balance)/nowCount," close=",close," calInput=",calInput)
    
    print("nowCount=",nowCount," balance=",balance," nowB=",nowCount*test['data'][-1]['close']," initInput=",initInput," avg=",(initInput-balance)/nowCount)    
   
    
     
    
    
    