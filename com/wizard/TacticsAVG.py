# -*- coding: utf-8 -*-

import globalUtil as constant


def avgJudgeBuy(data,index):
    
    Cn = data['close']
    
    ma10 = constant.getMa(10)
    ma30 = constant.getMa(30)
    ma60 = constant.getMa(60)
     
    if ma30 <= ma10 or ma30 == 0 or ma10 == 0:
        return False
     
    if Cn >= ma10 or Cn >= ma30 or Cn >= ma60:
        return False
    
    return True




if __name__ == '__main__':
    price = constant.prices
    price.append(1)
    price.append(2)
    price.append(3)
    price.append(4)
    price.append(5)
    print (constant.getMa(20))
    
    