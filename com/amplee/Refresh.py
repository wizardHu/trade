# -*- coding: utf-8 -*-
import modelUtil as modelUtil
from TransactionModel import TransactionModel
import time

lastRefreshTime = 0
pairs = []

def contains(pairsModel,symbol):
    for o in list:

def getAllPairAndRefresh():
    global lastRefreshTime
    global pairs

    t = int(time.time())

    gap = t - lastRefreshTime

    if gap > 5:#5秒同步一次
        pairsModel = modelUtil.getAllPair()
        lastRefreshTime = t

        needAdd = []
        needDel = []

        for newModel in pairsModel:
            for oldModel in pairs:
                if oldModel.symbol == newModel.symbol:
                    continue
            needAdd.append(newModel)

        for oldModel in pairs:
            for newModel in pairsModel:
                if oldModel.symbol == newModel.symbol:
                    continue
            needDel.append(newModel)

        print("needAdd",needAdd)
        print("needDel",needDel)
        pairs = pairsModel

    return pairs

if __name__ == '__main__':
    print(getAllPairAndRefresh())
    time.sleep(6)
    print(getAllPairAndRefresh())
    time.sleep(6)
    print(getAllPairAndRefresh())