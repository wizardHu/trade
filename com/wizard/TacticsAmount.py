# -*- coding: utf-8 -*-

import numpy as np
import globalUtil as constant

uplow = []

def amountJudgeBuy(data,index):
    global uplow
    
    volsma5 = 0
    volsma10 = 0
    
    deal = data['amount']
    price = data['close']
    
    close = data['close']
    open = data['open']
    up = 1
    
    if close <= open :
        up = 0
    
    
#     print deal,"======",index,"==",up
    
    uplow.append(up)
    
    if len(uplow) > 100:
        uplow = uplow[1:]
        
    amount = constant.amount
    
    if len(amount) >= 5:
        list5 = amount[-5:]
        volsma5 = np.mean(list5)
    
    if len(amount) >= 10:
        list10 = amount[-10:]
        volsma10 = np.mean(list10)
    
    avg = (volsma5 + volsma10)/2
    
    if avg > deal:
        return False
    
    return True

def isLowest(price):
    prices = constant.prices[-100:]
    
    if len(prices)<90:
        return False
    
    for i in prices:
        if i < price:
            return False
    
    return True

def isfastLowAmount(exchangeamount):
    amount = constant.amount
   
    if len(amount)<2 or exchangeamount==0:
        return False
        
    lastAmount = amount[-2]
    multiple = lastAmount/exchangeamount
    
    if multiple >= 5:
        return True
    
    return False

def isHighPer(per,exchangeamount):
    amount = constant.amount[-101:]
    amount = amount[0:len(amount)-1]#排除自己
    
    amount.sort()
    
    count = len(amount)-(len(amount)*per/100)
    
    amount = amount[(-1*count):]
    
    
    if exchangeamount < (amount[0]*0.9):
        return False
    
    return True

def judgeRisk():
    amounts = constant.amount
    prices = constant.prices
    global uplow
    
    risk = 0
    
    amount10 = amounts[-13:len(amounts)-1]#取最后13 并排除最后一个
    prices10 = prices[-11:len(prices)-1]
    uplow10 = uplow[-11:len(uplow)-1]
    
    if len(amount10) == 12:
        for index in range(len(prices10)):
            amount = amount10[index+2]#与 index位置的price 对应的成交额度
             
            if risk==0  and isHighPer(85,amount):#这个成交量大于最近100期的85% 需要进行成交额判断
                last2 = amount10[index]
                last1 = amount10[index+1]
                
                if last2 == 0:
                    last2=1
                
                if last1 == 0:
                    last1=1
                
                if amount/last1 >= 5 or amount/last2 >= 6:#成交量异常 需要进行风险判断
                    risk += 2
                    continue
            
            if risk != 0:
                if uplow10[index]==1:
                    risk -= 1
                else:
                    risk += 1
#                     if risk >5:
#                         risk = 0
                    
    else:
        return False
    
    if risk == 0 or risk > 5:
        return True
    
    return False
            
    
    
if __name__ == '__main__':
    constant.amount.append(1)
    constant.amount.append(4)
    constant.amount.append(5)
    constant.amount.append(3)
    constant.amount.append(2)
    
    flag =  isHighPer(70,4)
    
    print not flag


