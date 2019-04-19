import numpy as np
import pandas as pd
from TranPairs import TranPairs

from statsmodels.tsa.stattools import coint
import HuobiService as huobi

def writeSymbolRecord(msg):
    f = open('pairTxt','a',encoding='utf-8')
    f.write("{0}\n".format(msg))
    f.flush()
    f.close()

def takeKey(tranPairs):
    return tranPairs.pvalue

if __name__ == '__main__':
    symbols = huobi.get_symbols();
    datas = symbols['data']

    symbolsList = []

    for data in datas:
        quote_currency = data['quote-currency']
        if quote_currency == 'usdt':
            symbolsList.append(data['symbol'])

    print(symbolsList)
    print(len(symbolsList))

    pairList = []
    for index in range(len(symbolsList)):
        for index2 in range(index+1,len(symbolsList)):
            pairs = [symbolsList[index],symbolsList[index2]]
            pairList.append(pairs)

    tranPairsList = []
    count = 0;
    for symbolPair in pairList:

        try:

            first = symbolPair[0]
            second = symbolPair[1]

            # if count == 5:
            #     break
            # count = count + 1
            #1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
            firstLine = huobi.get_kline(first, '15min', 2000)
            secondLine = huobi.get_kline(second, '15min', 2000)

            # print(firstLine,first)
            # print(secondLine,second)

            if firstLine is None or secondLine is None:
                continue

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
                corrXY = X.corr(Y)
                print(pvalue, corrXY,first,second)  # X.corr(Y) 是相关性 [-1,1]越大越好 0.7以上就行

                tranPairs = TranPairs(first,second,pvalue,corrXY)
                tranPairsList.append(tranPairs)
        except Exception as err:
            print(err)


    tranPairsList.sort(key=takeKey)
    print(len(tranPairsList),"------------------------------------")
    for tranPair in tranPairsList:
        print(tranPair.getValue()+"sss")
        writeSymbolRecord(tranPair.getValue())