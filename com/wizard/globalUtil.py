# -*- coding: utf-8 -*-

import time

import MyHuobiService as myHuo
from Transaction import Transaction
import HuobiService as huobi


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
        if orderId == 0:
            return 'error'
        return myHuo.getOrderStatus(orderId)
    else:
        return 'filled'


#判断是否可卖
def canSell(evn,price,symbols):
    global wait
    global ma10
    global closeGap
    
    buyPackage = getBuyPackage(symbols)#查询购买历史
    
    listPrice = []
    
    for transaction in buyPackage:
        
        state = getOrderStatus(evn,transaction.orderId) #先判断订单的状态
         
        if state != 'filled':
            continue
        
        buyPrice = float(transaction.price)
        
        if buyPrice*1.01 <= price:
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

def canSellv2(evn,price,symbols):
    buyPackage = getBuyPackage(symbols)  # 查询购买历史

    listPrice = []
    avgPrice = getBuyPriceAVG(symbols);

    if avgPrice > 0:
        avgGap = price - avgPrice;
        avgGap = avgGap/avgPrice

        if avgGap >= 0.015:
            for transaction in buyPackage:
                transaction.sellPrice = price;
                listPrice.append(transaction)

            return  listPrice

    for transaction in buyPackage:

        state = getOrderStatus(evn, transaction.orderId)  # 先判断订单的状态

        if state != 'filled':
            continue

        transactionPrice = transaction.price;

        gap = price - float(transactionPrice)
        gap = gap/float(transactionPrice)

        if gap >= 0.015:
            transaction.sellPrice = price;
            listPrice.append(transaction)

    return  listPrice


#挂卖单
def sell(evn,transactions,symbols):
    
    for transaction in transactions:
        
        if evn == 'pro':
            myHuo.sendOrder(transaction.amount, transaction.sellPrice, symbols, 'sell-limit')
        
        delMsgFromFile(transaction.getValue())
        writeTradeRecord(('0 {} {} {} {}').format(transaction.price, transaction.amount,transaction.sellPrice,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())));
        
def getMa(period):
    global prices
    
    count = 0.0
    
    if len(prices) >= period:
        lists = prices[(-1*period):]
        for p in lists:
            count += p
    
    return round(count/period,3)

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

#拿当前价格和以往买过的对比，差距在1.5%内的不买
def juideAllGap(price,evn,symbols):
    buyPackage = getBuyPackage( symbols)#查询购买历史 #查询购买历史
    
    for transaction in buyPackage:
        
        buyPrice = float(transaction.price)
        
        gap = abs(buyPrice-price)
        times = gap/buyPrice
        if times < 0.015:
            return False
    
    return True

#得到所有购买的平均值
def getBuyPriceAVG(symbols):
    buyPackage = getBuyPackage(symbols)  # 查询购买历史 #查询购买历史

    price = 0.0;
    count = 0.0;

    for transaction in buyPackage:
        amount = float(transaction.amount)
        count = count + amount;

        buyPrice = float(transaction.price)
        price = price + buyPrice*amount;

    if count == 0:
        return 0;

    return price/count;

#根据收盘价和历史购买的平均值，确定这一期要买几个
def getShouldByAmount(close,symbols):
    avgPrice = getBuyPriceAVG(symbols);

    if avgPrice == 0:#意味着还没买过
        return 5;

    if avgPrice <= close:
        return 0;

    gap = avgPrice - close;
    rang = gap/avgPrice;

    if rang <= 0.015:
        return 5;
    elif rang <= 0.03:
        return 5;
    else:
        return 5;



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
    #比最大值少两个点还要大就不要买了 风险高
    if price >= high*0.98:
        return False
    
    return True

def write(msg):
    f = open('buy','a',encoding='utf-8')
    f.write("{0}\n".format(msg))
    f.flush()
    f.close()
    
def writeTradeRecord(msg):
    f = open('tradeRecord','a',encoding='utf-8')
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
    print(getOrderStatus('pro',0))

    # myHuo.sendOrder(1,0.5,'xrpusdt','sell-limit')
#     write("qw1,er1,121")
#     write("qw2,er2,122")
#         
#     delMsgFromFile('qw1,er1,121')
#     write("qw3,er4,125")
#     
#     lines = readAll()
#     for line in lines:
#         print(line)