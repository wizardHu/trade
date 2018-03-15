# -*- coding: utf-8 -*-

prices = []

def add(data,index):
    global prices
    
    Cn = data['close']
    prices.append(Cn)
    
    if len(prices) >300:
        prices = prices[1:]
    
    