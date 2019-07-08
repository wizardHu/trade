# -*- coding: utf-8 -*-
import modelUtil as modelUtil
import HuobiService as huobi
import klineUtil as klineUtil
import KDJUtil as kDJUtil
import RSIUtil as rSIUtil
import MAUtil as mAUtil
import time
import logUtil

lastRefreshTime = 0
pairs = []

def delSymbol(needDel):
    logUtil.info("needDel={}".format(needDel))
    for model in needDel:
        logUtil.info("begin del={}".format(model))
        klineUtil.delSymbol(model.symbol)
        kDJUtil.delSymbol(model.symbol)
        rSIUtil.delSymbol(model.symbol,12)
        mAUtil.delSymbol(model.symbol,10)
        mAUtil.delSymbol(model.symbol,30)
        mAUtil.delSymbol(model.symbol,60)
        logUtil.info("end del={}".format(model))

def addSymbol(needAdd):
    logUtil.info("needAdd={}".format(needAdd))

def contains(pairsModel,symbol):
    for model in pairsModel:
        if model.symbol == symbol:
            return True
    return False

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
            if not contains(pairs,newModel.symbol):
                needAdd.append(newModel)

        for oldModel in pairs:
            if not contains(pairsModel, oldModel.symbol):
                needDel.append(oldModel)

        delSymbol(needDel)
        addSymbol(needAdd)

        pairs = pairsModel

    return pairs



if __name__ == '__main__':
    print(getAllPairAndRefresh())
    time.sleep(6)
    print(getAllPairAndRefresh())
    time.sleep(6)
    print(getAllPairAndRefresh())