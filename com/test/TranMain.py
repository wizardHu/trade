import HuobiService as huobi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def zscore(series):
    return (series - series.mean()) / np.std(series)

if __name__ == '__main__':
    firstLine = huobi.get_kline('xlmusdt', '1min', 110)
    secondLine = huobi.get_kline('omgusdt', '1min', 110)

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

    for index in range(min(len(firstLine['data']), len(secondLine['data']))):

        firstClose = firstLine['data'][index]['close']
        secondClose = secondLine['data'][index]['close']

        firstData.append(firstClose)
        secondData.append(secondClose)

        if len(firstData) < 100:
            continue

        X = pd.Series(firstData, name='X')
        Y = pd.Series(secondData, name='Y')

        # ratios = X / Y

        ratios = Y - 24.3042*X

        score = zscore(ratios)
        scoreList = score.tolist()

        s = scoreList[-1]

        if s > 1 and c == 0:

            buyCount = 24.3042;
            firstCount = firstCount + buyCount*0.998;
            balance = balance - firstClose*buyCount;

            sellCount = 1;

            if secondCount < sellCount:
                sellCount = secondCount

            secondCount = secondCount - sellCount
            balance = balance + sellCount*secondClose*0.998

            print("index=",index," s=",s," 买入first:",buyCount," firstClose=",firstClose," firstCount=",firstCount," 卖出second:",sellCount," secondClose=",secondClose," secondCount=",secondCount," balance=",balance)

            c = 1
            b = 0;

        if s < -1 and b == 0:
            buyCount = 1;
            secondCount = secondCount + buyCount * 0.998;
            balance = balance - secondClose;

            sellCount = 24.3042;

            if firstCount < sellCount:
                sellCount = firstCount

            firstCount = firstCount - sellCount
            balance = balance + sellCount * firstClose * 0.998
            b = 1
            c = 0

            print("index=",index," s=",s,"买入second:", buyCount, " secondClose=", secondClose, " secondCount=", secondCount, " 卖出first:",
                  sellCount," firstCount=",firstCount, " firstClose=", firstClose, " balance=", balance)

    balance = balance+firstCount*firstClose*0.998+secondCount*secondClose*0.998
    print("balance=",balance," firstCount=",firstCount," secondCount=",secondCount)
