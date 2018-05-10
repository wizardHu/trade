# -*- coding: utf-8 -*-

import time

import MyHuobiService as myHuo
from Transaction import Transaction


prices = []
amount = []

buyPackage = []
wait = 0
nextBuy = 0
ma10 = []
closeGap = []

def add(data,index):
    global prices
    global amount
    global ma10
    global closeGap
    
    Cn = data['close']
    prices.append(Cn)
    
    deal = data['amount']
    amount.append(deal)
    
    if len(prices)>1:
        gap = prices[-1] - prices[-2]
        closeGap.append(gap)
    
    count = 0.0
    if len(prices) > 10:
        lists = prices[(-10):]
        for p in lists:
            count += p
    
        ma = round(count/10,2)
        ma10.append(ma)
    
    if len(prices) >720:
        prices = prices[1:]
        amount = amount[1:]
        ma10 = ma10[1:]
        closeGap = closeGap[1:]
        
#获取买入记录
def getBuyPackage(symbol):
    
    return myHuo.getOrderFromFile()
    
#获取订单状态
def getOrderStatus(evn,orderId):
    
    if evn == 'pro':
        return myHuo.getOrderStatus(orderId)
    else:
        return 'filled'


#判断是否可卖
def canSell(evn,price):
    global wait
    global ma10
    global closeGap
    
    buyPackage = getBuyPackage('eosusdt')#查询购买历史
    
    listPrice = []
    
    for transaction in buyPackage:
        
        state = getOrderStatus(evn,transaction.orderId) #先判断订单的状态
         
        if state != 'filled':
            continue
        
        buyPrice = float(transaction.price)
        
        if buyPrice*1.007 <= price:
            ma = ma10[-2:]
            if len(ma) > 1:
                if ma[0] >= ma[1]:# 十日均线向下
                    listPrice.append(transaction) 
                elif wait==0:# 向上 再等一期才卖
                    wait+=1
                    print (price ,"wait")
                elif wait == 1:
                    wait = 0
                    listPrice.append(transaction) 
    
    flag = True
    for gap in closeGap[-50:]:#最新50期中，这一期是不是最大
        if closeGap[-1] < gap:
            flag = False
    
    if flag:
        listPrice.clear()
        wait = 1
    
    return listPrice

#挂卖单
def sell(evn,transactions):
    
    for transaction in transactions:
        
        if evn == 'pro':
            myHuo.sendOrder(2, transaction.price, 'eosusdt', 'sell-limit')
        
        delMsgFromFile(transaction.getValue())
        
def getMa(period):
    global prices
    
    count = 0.0
    
    if len(prices) >= period:
        lists = prices[(-1*period):]
        for p in lists:
            count += p
    
    return round(count/period,2)   

#两期差距不到0.2%就可以买
def juideGap():
    global prices
    
    if len(prices)<2:
        return False
    
    curPrice = prices[-1]
    lastPrice = prices[-2]
    
    if curPrice <= lastPrice:
        return True
    else:
        gap = curPrice - lastPrice
        times = gap/lastPrice
        if times < 0.002:
            return True
    
    return False

#拿当前价格和以往买过的对比，差距在0.2%内的不买
def juideAllGap(price,evn):
    buyPackage = getBuyPackage( 'eosusdt')#查询购买历史 #查询购买历史
    
    for transaction in buyPackage:
        
        buyPrice = float(transaction.price)
        
        gap = abs(buyPrice-price)
        times = gap/buyPrice
        if times < 0.002:
            return False
    
    return True

#买入
def sendBuy(evn,amount,price,symbol):
    
    orderId = 0
    
    if evn == 'pro':
        orderId = myHuo.sendOrder(amount, price, symbol, 'buy-limit')
         
    index = int(round(time.time() * 1000))
    transaction = Transaction(price,index,amount,orderId,0)
    write(transaction.getValue())

#判断是否比最近12小时的最大值要大
def isLagerBigger(price):
    global prices
    
    high = max(prices)
     
    if price >= high*0.93:
        return False
    
    return True

def write(msg):
    f = open('buy','a',encoding='utf-8')
    f.write("{0}\n".format(msg))
    f.flush()
    f.close()
    

def delAll():
    f = open('buy','w',encoding='utf-8')
    f.close()

def readAll():
    lines = []
    f = open('buy',encoding='utf-8')
    for line in f.readlines() :
        if line != '\n' and line!='':
            lines.append(line.replace('\n',''))
    
    f.close()
    return lines

def delMsgFromFile(msg):
    
    msg = "{0}\n".format(msg)
    lines = []
    f = open('buy',encoding='utf-8')
    for line in f:
        if line != msg:
            lines.append(line.replace('\n',''))
    
    delAll()
    f.close()
    
    for line in lines:
        write(line)


if __name__ == '__main__':
    
#     write("qw1,er1,121")
#     write("qw2,er2,122")
#         
#     delMsgFromFile('qw1,er1,121')
#     write("qw3,er4,125")
#     
#     lines = readAll()
#     for line in lines:
#         print(line)
    print(getAllOrder("eosusdt"))
    