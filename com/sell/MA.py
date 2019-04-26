import numpy as np
import priceUtil as priceUtil

def getMa(period):
    prices = priceUtil.prices

    if len(prices) < period:
        return 0

    maList = prices[-1*period:]

    return np.nanmean(maList)