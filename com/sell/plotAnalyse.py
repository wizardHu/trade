# -*- coding: utf-8 -*-
import HuobiService as huobi
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator
import KDJ as KDJ
import priceUtil as priceUtil
import MA as MA
import Boll as Boll
import Amount as Amount
from TradeModel import TradeModel
import fileUtil as fileUtil
import  TradeUtil as TradeUtil

if __name__ == '__main__':

    fig = plt.figure()
    symbols = 'eosusdt'
    test = huobi.get_kline(symbols, '1min', 2000)

    test['data'].reverse()

    dataList = []
    dataListX = []

#用于画图
    K = []
    D = []
    J = []
    sellX = []
    sellY = []

    buyX = []
    buyY = []

    ma10x = []
    ma10y = []

    ma60x = []
    ma60y = []

    amounts = []

    for data in test['data']:
        index = test['data'].index(data)
        close = data['close']

        dataList.append(close)
        dataListX.append(index)
        amounts.append(data['amount'])

        priceUtil.add(data,index)

        KDJ.calKDJ(data,index)
        K.append(KDJ.getLastK())
        D.append(KDJ.getLastD())
        J.append(KDJ.getLastJ())

        bollFlag = True
        kdjFlag = True
        amountFlag = True
        # kdjFlag = KDJ.judgeSell(index)
        bollFlag = Boll.judgeBoll(data,index)
        amountFlag = Amount.judgeAmount(data,index)
        sellFlag = TradeUtil.canSell(symbols,close)
        if kdjFlag and bollFlag and amountFlag and sellFlag:
            sellX.append(index)
            sellY.append(close)
            tradeModel = TradeModel(close,10,0,index,symbols)
            fileUtil.write(tradeModel.getValue(),"sell"+symbols)

        canBuyLists = TradeUtil.getBuyModel(symbols,close,"dev")

        for buyRecord in canBuyLists:
            buyX.append(index)
            buyY.append(close)


        m10 = MA.getMa(10)
        if m10 != 0:
            ma10x.append(index)
            ma10y.append(m10)

        m60 = MA.getMa(60)
        if m60 != 0:
            ma60x.append(index)
            ma60y.append(m60)

    xmajorLocator = MultipleLocator(50);

    #三行一列 获取第 1 行 第 0 列的图表，占一列，两行
    ax1 = plt.subplot2grid((3, 1), (0, 0), colspan = 1, rowspan = 3)

    # 三行一列 获取第 3 行 第 0 列的图表，占一列，一行
    # ax2 = plt.subplot2grid((3, 1), (2, 0), colspan = 1, rowspan = 1)
    # ax3 = fig.add_subplot(313)

    ax1.plot(dataListX,dataList)
    # ax1.plot(ma10x, ma10y)
    # ax1.plot(ma60x, ma60y)
    ax1.scatter(sellX, sellY, label='1', color='red')
    ax1.scatter(buyX, buyY, label='1', marker = 'x', color = 'm')
    ax1.xaxis.set_major_locator(xmajorLocator)
    ax1.grid(linestyle='--')

    # ax2.bar(dataListX, amounts, 1, label="rainfall", color="#87CEFA")

    # ax2.plot(dataListX,K, color="red")
    # ax2.plot(dataListX,D, color='blue')
    # ax2.plot(dataListX,J, color='green')
    # ax2.xaxis.set_major_locator(xmajorLocator)
    # ax2.grid(linestyle='--')

    # ax3.plot(dataListX, dataList, label=symbols)
    # ax3.xaxis.set_major_locator(xmajorLocator)
    # ax3.grid(linestyle='--')

    plt.show()