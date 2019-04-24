# -*- coding: utf-8 -*-
import HuobiService as huobi
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator
import KDJ as KDJ
from matplotlib.ticker import  FormatStrFormatter
import globalUtil as constant
import Client as client
import time

if __name__ == '__main__':

    fig = plt.figure()
    symbols = 'eosusdt'
    test = huobi.get_kline(symbols, '1min', 1000)

    test['data'].reverse()

    dataList = []
    dataListX = []

#用于画图
    K = []
    D = []
    J = []
    sellX = []
    sellY = []

    for data in test['data']:
        index = test['data'].index(data)
        dataList.append(data['close'])
        dataListX.append(index)

        KDJ.calKDJ(data,index)
        K.append(KDJ.getLastK())
        D.append(KDJ.getLastD())
        J.append(KDJ.getLastJ())

        flag = KDJ.judgeSell(index);
        if flag:
            sellX.append(index)
            sellY.append(data['close'])



    xmajorLocator = MultipleLocator(50);

    #三行一列 获取第 1 行 第 0 列的图表，占一列，两行
    ax1 = plt.subplot2grid((3, 1), (0, 0), colspan = 1, rowspan = 2)

    # 三行一列 获取第 3 行 第 0 列的图表，占一列，一行
    ax2 = plt.subplot2grid((3, 1), (2, 0), colspan = 1, rowspan = 1)
    # ax3 = fig.add_subplot(313)

    ax1.plot(dataListX,dataList)
    ax1.scatter(sellX, sellY, label='1', color='red')
    ax1.xaxis.set_major_locator(xmajorLocator)
    ax1.grid(linestyle='--')

    ax2.plot(dataListX,K, color="red")
    ax2.plot(dataListX,D, color='blue')
    # ax2.plot(dataListX,J, color='green')
    ax2.xaxis.set_major_locator(xmajorLocator)
    ax2.grid(linestyle='--')

    # ax3.plot(dataListX, dataList, label=symbols)
    # ax3.xaxis.set_major_locator(xmajorLocator)
    # ax3.grid(linestyle='--')

    plt.show()