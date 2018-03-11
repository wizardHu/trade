# -*- coding: utf-8 -*-

import pandas as pd

amounts = []

def calAmount(datas):
    global amounts
    
    for data in datas:
        amount = data['amount']
        
        amount = int(amount)
        amount = amount / 1000;
        
        if amount == 0:
            amount = 1
        
        amount *= 1000
        
        amounts.append(amount)
        
    amounts.sort()
    
    num = []
    index = []
    
    for a in amounts:
        
        if num.count(a) == 0:
            num.append(a)
            index.append(amounts.count(a))
    
    
    count = 0
    for i in index:
        count += i
    
    
    print len(num),len(index),count
    print num,"\n",index
    




