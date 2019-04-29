import numpy as np
import priceUtil as priceUtil

def judgeAmount(data,index):

    if len(priceUtil.amounts) < 5:
        return False

    list = [priceUtil.amounts[-1],priceUtil.amounts[-2],priceUtil.amounts[-3],priceUtil.amounts[-4],priceUtil.amounts[-5]]

    mean = np.mean(list)
    std = np.std(list)

    if std > mean:
        return True

    return False