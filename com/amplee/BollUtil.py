# -*- coding: utf-8 -*-

import numpy as np
import klineUtil as klineUtil


def getBoll(period, times,symbol):
    prices = klineUtil.prices.get(symbol, [])
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


def judgeBoll(price,symbol):
    boll = getBoll(20, 2,symbol)
    if len(boll) < 2:
        return False

    bollDown = boll[1]

    if bollDown > price:
        return True

    return False
