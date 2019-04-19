import HuobiService as huobi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from arch.unitroot import ADF

def zscore(series):
    return (series - series.mean()) / np.std(series)

if __name__ == '__main__':
    firstLine = huobi.get_kline('ctxcusdt', '15min', 2000)
    secondLine = huobi.get_kline('hcusdt', '15min', 2000)

    firstLine['data'].reverse()
    secondLine['data'].reverse()
    firstData = []
    secondData = []

    firstCount = 0
    secondCount = 0
    balance = 0
    score = []
    firstClose = 0
    secondClose = 0
    ratioList = []
    b = 0
    c = 0

    mu = 0
    sd = 0
    gap1 = 0
    gap2 = 0
    gap3 = 0
    gap4 = 0
    gap5 = 0
    gap6 = 0

    beat = 3.5170
    times = 100

    for index in range(min(len(firstLine['data']), len(secondLine['data']))):

        firstClose = firstLine['data'][index]['close']
        secondClose = secondLine['data'][index]['close']

        firstData.append(firstClose)
        secondData.append(secondClose)

        if len(firstData) < 1000:
            continue

        X = pd.Series(firstData, name='X')
        Y = pd.Series(secondData, name='Y')

        spreadf = Y - beat * X
        # spreadf = np.log(Y) - beat*np.log(X)
        if len(firstData) == 1000:
            adfSpread = ADF(spreadf)
            mu = np.mean(spreadf)
            sd = np.std(spreadf)
            gap1 = mu - 2.5 * sd
            gap2 = mu - 1.5 * sd
            gap3 = mu - 0.2 * sd
            gap4 = mu + 0.2 * sd
            gap5 = mu + 1.5 * sd
            gap6 = mu + 2.5 * sd
            print(mu,sd)
        # ratios = X / Y

        concurent = spreadf[len(spreadf)-1]
        last = spreadf[len(spreadf)-2]

        if last < gap5 and concurent > gap5:#上穿gap5 mu + 1.5 * sd
            print("卖出Y，买入X", index, concurent)
            buyCount = times*beat*secondClose/firstClose;
            firstCount = firstCount + buyCount * 0.998;
            balance = balance - times*beat*secondClose;

            sellCount = times;

            if secondCount < sellCount:
                sellCount = secondCount

            secondCount = secondCount - sellCount
            balance = balance + sellCount * secondClose * 0.998

            print("index=", index, "买入first:", buyCount, " firstClose=", firstClose, " firstCount=",
                  firstCount, " 卖出second:",
                  sellCount, " secondCount=", secondCount, " secondClose=", secondClose, " balance=", balance)


        elif last > gap2 and concurent < gap2:#g下穿gap2 mu - 1.5 * sd
            print("卖出X，买入Y",index)
            buyCount = times;
            secondCount = secondCount + buyCount * 0.998;
            balance = balance - times * secondClose;

            sellCount = times*beat*secondClose/firstClose;

            if firstCount < sellCount:
                sellCount = firstCount

            firstCount = firstCount - sellCount
            balance = balance + sellCount * firstCount * 0.998

            print("index=", index, "买入second:", buyCount, " secondClose=", secondClose, " secondCount=",
                  secondCount, " 卖出first:",
                  sellCount, " firstCount=", firstCount, " firstClose=", firstClose, " balance=", balance)

        elif last < gap3 and concurent > gap3:#上穿gap3 mu - 0.2 * sd
            print("卖出Y",index)
            sellCount = secondCount;

            secondCount = secondCount - sellCount
            balance = balance + sellCount * secondClose * 0.998

            print("index=", index, " 卖出second:",
                  sellCount, " secondCount=", secondCount, " secondClose=", secondClose, " balance=", balance)


        elif last > gap4 and concurent <gap4 :#下穿gap4 mu + 0.2 * sd
            print("卖出X",index)
            sellCount = firstCount;

            firstCount = firstCount - sellCount
            balance = balance + sellCount * firstClose * 0.998

            print("index=", index, " 卖出first:",
                  sellCount, " firstCount=", firstCount, " firstClose=", firstClose, " balance=", balance)

        elif (last > gap1 and gap1 > concurent) or (last < gap6 and concurent >gap6): #上穿gap6 下穿gap1
            print("全部卖出", index)
            # firstCount = 0
            # secondCount = 0
            # balance = balance + firstCount * firstClose * 0.998 + secondCount * secondClose * 0.998
            # print("index=", index, " 卖出first:",
            #       sellCount, " firstCount=", firstCount, " firstClose=", firstClose, " 卖出second:",
            #       sellCount, " secondCount=", secondCount, " secondClose=", secondClose," balance=", balance)

    balance = balance+firstCount*firstClose*0.998+secondCount*secondClose*0.998
    print("balance=",balance," firstCount=",firstCount," secondCount=",secondCount)
