#!/usr/bin/env python
# -*- coding: utf-8 -*-

import HuobiService as huobi
from Transaction import Transaction
import globalUtil as constant
import time


#获得所有的买记录
def getAllOrder(symbol):
    result = huobi.orders_matchresults(symbol, "buy-limit", "2017-04-09")
    
    buyPackage = []
    
    if result['status'] == 'ok':
        datas = result['data']
        for order in datas:
            index = order['created-at']
            price = order['price']
            amount = order['filled-amount']
            orderId = order['order-id']
            
            transaction = Transaction(price,index,amount,orderId)
            buyPackage.append(transaction)
    
    return buyPackage

#将买入记录装换成简单的列表
def getSimpleAllOrder(symbol):
    buyPackage = getAllOrder(symbol)
    
    orders = []
    
    for order in buyPackage:
        orders.append(order.price)

#从文件中读取买入记录
def getOrderFromFile():
    buyPackage = []
    buys = constant.readAll()
    
    for order in buys:
        params = order.split(',')
        price = params[0]
        amount = params[1]
        orderId = params[2]
        index = params[3]
        #int(round(time.time() * 1000))
        
        transaction = Transaction(price,index,amount,orderId)
        buyPackage.append(transaction)
    
    return buyPackage

def getOrderStatus(orderId):
    result = huobi.order_info(orderId)
    data = result['data']
    state = data['state']
    
    return state
        