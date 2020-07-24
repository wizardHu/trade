# -*- coding: utf-8 -*-
import modelUtil as modelUtil
import HuobiService as huobi
import time
import logUtil
import commonUtil as commonUtil

lastRefreshTime = 0
pairs = []

def delSymbol(needDel):
    logUtil.info("needDel={}".format(needDel))
    for model in needDel:
        logUtil.info("begin del={}".format(model))
        commonUtil.delSymbol(model)
        logUtil.info("end del={}".format(model))

def addSymbol(needAdd):
    logUtil.info("needAdd={}".format(needAdd))
    for model in needAdd:
        logUtil.info("begin add={}".format(model))
        kline = huobi.get_kline(model.symbol, model.period, 1000)
        datas = kline['data']
        datas.reverse()
        for data in datas:
            commonUtil.addSymbol(data,model,False)
        logUtil.info("end add={}".format(model))

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