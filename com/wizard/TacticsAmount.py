# -*- coding: utf-8 -*-

import numpy as np

amount = []

def amountJudgeBuy(data,index):
    global amount
    
    volsma5 = 0
    volsma10 = 0
    
    deal = data['amount']
    
    print deal,"======",index
    
    amount.append(deal)
    
    
    if len(amount) > 20:
        amount = amount[1:]
    
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
    
if __name__ == '__main__':
    amountJudgeBuy(1,2)


