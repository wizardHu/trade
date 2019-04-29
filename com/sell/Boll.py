import numpy as np
import priceUtil as priceUtil

def calBoll(period,times):
    prices = priceUtil.prices

    boll = []

    if len(prices) >= period:
        lists = prices[(-1 * period):]

        midBBand = np.nanmean(lists)
        sigma = np.nanstd(lists)

        upBBand = midBBand + times * sigma
        downBBand = midBBand - times * sigma

        boll.append(upBBand)
        boll.append(downBBand)

    return boll


def judgeBoll(data,index):
    price = data['close']
    low = data['low']

    boll = calBoll(20, 2)
    if len(boll) < 2:
        return False

    upBBand = boll[0]

    if upBBand < low:
        return True

    return False