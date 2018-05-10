# -*- coding: utf-8 -*-

import time

import globalUtil as constant
import MyHuobiService as myHuo
from Transaction import Transaction


if __name__ == '__main__':
    buys = constant.readAll()
    
    for order in buys:
        
        if order != '' and order != '\n':
            params = order.split(',')
            price = params[0]
            amount = params[1]
            orderId = params[2]
            index = params[3]
            isSpecial = params[4]
            
            transaction = Transaction(price,index,amount,orderId,isSpecial)
            
            state = myHuo.getOrderStatus(orderId)
            
            print(state)
            
            if state != 'filled':
                constant.delMsgFromFile(transaction.getValue())
        
        
        
        
        
        
        
        
        