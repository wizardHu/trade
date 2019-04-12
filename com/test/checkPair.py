import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import coint
import HuobiService as huobi
#输出两个交易对的相关信息
if __name__ == '__main__':

    firstLine = huobi.get_kline('xlmusdt', '1min', 2000)
    secondLine = huobi.get_kline('omgusdt', '1min', 2000)

    # print(firstLine,first)
    # print(secondLine,second)

    if  firstLine['status'] == 'ok' and secondLine['status'] == 'ok' and firstLine['data'] and secondLine['data']:

        firstLine['data'].reverse()
        secondLine['data'].reverse()

        firstData = []
        secondData = []
        for index in range(min(len(firstLine['data']),len(secondLine['data']))):
            firstData.append(firstLine['data'][index]['close'])
            secondData.append(secondLine['data'][index]['close'])

        X = pd.Series(firstData, name='X')
        Y = pd.Series(secondData, name='Y')
        score, pvalue, _ = coint(X, Y)  # pvalue 就是协整值  越小越好
        print(pvalue, X.corr(Y))  # X.corr(Y) 是相关性 [-1,1]越大越好 0.7以上就行

        Xsm = sm.add_constant(X)
        result = (sm.OLS(Y, Xsm)).fit()
        print(result.summary())

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(X, Y, 'o', label="data")
        ax.plot(X, result.fittedvalues, 'r', label="OLS")
        ax.legend(loc='best')
        plt.show()