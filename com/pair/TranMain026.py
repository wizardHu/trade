import HuobiService as huobi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from arch.unitroot import ADF
import statsmodels.api as sm

def zscore(series):
    return (series - series.mean()) / np.std(series)

def TradeSig(prcLevel):
    n=len(prcLevel)
    signal=np.zeros(n)
    for i in range(1,n):
        if prcLevel[i-1]==1 and prcLevel[i]==2:
            signal[i]=-2
        elif prcLevel[i-1]==1 and prcLevel[i]==0:
            signal[i]=2
        elif prcLevel[i-1]==2 and prcLevel[i]==3:
            signal[i]=3
        elif prcLevel[i-1]==-1 and prcLevel[i]==-2:
            signal[i]=1
        elif prcLevel[i-1]==-1 and prcLevel[i]==0:
            signal[i]=-1
        elif prcLevel[i-1]==-2 and prcLevel[i]==-3:
            signal[i]=-3
    return(signal)

def TradeSim(priceX,priceY,position):
    n=len(position)
    size=10
    shareY=size*position
    shareX=[(-beta)*shareY[0]*priceY[0]/priceX[0]]
    cash=[200]
    for i in range(1,n):
        shareX.append(shareX[i-1])
        cash.append(cash[i-1])
        if position[i-1]==0 and position[i]==1:
            shareX[i]=(-beta)*shareY[i]*priceY[i]/priceX[i]
            cash[i]=cash[i-1]-(shareY[i]*priceY[i]+shareX[i]*priceX[i])
        elif position[i-1]==0 and position[i]==-1:
            shareX[i]=(-beta)*shareY[i]*priceY[i]/priceX[i]
            cash[i]=cash[i-1]-(shareY[i]*priceY[i]+shareX[i]*priceX[i])
        elif position[i-1]==1 and position[i]==0:
            shareX[i]=0
            cash[i]=cash[i-1]+(shareY[i-1]*priceY[i]+shareX[i-1]*priceX[i])
        elif position[i-1]==-1 and position[i]==0:
            shareX[i]=0
            cash[i]=cash[i-1]+(shareY[i-1]*priceY[i]+shareX[i-1]*priceX[i])
    cash = pd.Series(cash,index=position.index)
    shareY=pd.Series(shareY,index=position.index)
    shareX=pd.Series(shareX,index=position.index)
    asset=cash+shareY*priceY+shareX*priceX
    account=pd.DataFrame({'Position':position,'ShareY':shareY,'ShareX':shareX,'Cash':cash,'Asset':asset})
    return(account)

if __name__ == '__main__':
    firstLine = huobi.get_kline('xlmusdt', '1min', 100)
    secondLine = huobi.get_kline('omgusdt', '1min', 100)

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

    PAf = pd.Series(firstData, name='X')
    PBf = pd.Series(secondData, name='Y')

    ############################

    log_PAf = np.log(PAf)
    log_PBf = np.log(PBf)

    # 协整关系检验
    model = sm.OLS(log_PBf, sm.add_constant(log_PAf)).fit()
    model.summary()

    alpha = model.params[0]
    beta = model.params[1]

    spreadf = log_PBf - beta * log_PAf - alpha

    adfSpread = ADF(spreadf)

    CoSpreadT = np.log(PBf) - beta * np.log(PAf) - alpha

    mu = np.mean(spreadf)
    sd = np.std(spreadf)

    print(mu,sd)

    level = (float('-inf'), mu - 2.5 * sd, mu - 1.5 * sd, mu - 0.2 * sd, mu + 0.2 * sd, mu + 1.5 * sd, mu + 2.5 * sd,
             float('inf'))

    prcLevel = pd.cut(CoSpreadT, level, labels=False)-3

    signal = TradeSig(prcLevel)

    position = [signal[0]]
    ns = len(signal)

    for i in range(1, ns):
        position.append(position[-1])
        if signal[i] == 1:
            position[i] = 1
        elif signal[i] == -2:
            position[i] = -1
        elif signal[i] == -1 and position[i - 1] == 1:
            position[i] = 0
        elif signal[i] == 2 and position[i - 1] == -1:
            position[i] = 0
        elif signal[i] == 3:
            position[i] = 0
        elif signal[i] == -3:
            position[i] = 0

    position = pd.Series(position, index=CoSpreadT.index)

    account1 = TradeSim(PAf, PBf, position)
    print(account1)


    ############################

    # ratios = Y - 24.3042*X
    #
    # score = zscore(ratios)
    # scoreList = score.tolist()
    #
    # s = scoreList[-1]
    #
    # if s > 1 and c == 0:
    #
    #     buyCount = 24.3042;
    #     firstCount = firstCount + buyCount*0.998;
    #     balance = balance - firstClose*buyCount;
    #
    #     sellCount = 1;
    #
    #     if secondCount < sellCount:
    #         sellCount = secondCount
    #
    #     secondCount = secondCount - sellCount
    #     balance = balance + sellCount*secondClose*0.998
    #
    #     print("index=",index," s=",s," 买入first:",buyCount," firstClose=",firstClose," firstCount=",firstCount," 卖出second:",sellCount," secondClose=",secondClose," secondCount=",secondCount," balance=",balance)
    #
    #     c = 1
    #     b = 0;
    #
    # if s < -1 and b == 0:
    #     buyCount = 1;
    #     secondCount = secondCount + buyCount * 0.998;
    #     balance = balance - secondClose;
    #
    #     sellCount = 24.3042;
    #
    #     if firstCount < sellCount:
    #         sellCount = firstCount
    #
    #     firstCount = firstCount - sellCount
    #     balance = balance + sellCount * firstClose * 0.998
    #     b = 1
    #     c = 0
    #
    #     print("index=",index," s=",s,"买入second:", buyCount, " secondClose=", secondClose, " secondCount=", secondCount, " 卖出first:",
    #           sellCount," firstCount=",firstCount, " firstClose=", firstClose, " balance=", balance)
    #
    # balance = balance+firstCount*firstClose*0.998+secondCount*secondClose*0.998
    # print("balance=",balance," firstCount=",firstCount," secondCount=",secondCount)
