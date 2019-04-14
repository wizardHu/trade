import matplotlib.pyplot as plt
import HuobiService as huobi
import pandas as pd
import numpy as np
from arch.unitroot import ADF

def zscore(series):
    return (series - series.mean()) / np.std(series)


if __name__ == '__main__':
    firstLine = huobi.get_kline('eosusdt', '1min', 2000)
    secondLine = huobi.get_kline('iotausdt', '1min', 2000)

    firstLine['data'].reverse()
    secondLine['data'].reverse()
    firstData = []
    secondData = []
    for index in range(min(len(firstLine['data'])-1000, len(secondLine['data'])-1000)):
        firstData.append(firstLine['data'][index]['close'])
        secondData.append(secondLine['data'][index]['close'])

    X = pd.Series(firstData, name='X')
    Y = pd.Series(secondData, name='Y')

    pd.concat([Y], axis=1).plot(figsize=(10,7))
    pd.concat([X], axis=1).plot(figsize=(10,7))
    # (X / Y).plot(figsize=(10, 7))
    # plt.axhline((X / Y).mean(), color='red', linestyle='--')
    # plt.show()

    # ratios = np.log(Y) - 0.0870 * np.log(X)
    ratios = Y - 0.0621 * X

    adfSpread = ADF(ratios)
    print(adfSpread.summary().as_text())

    mu = np.mean(ratios)
    sd = np.std(ratios)
    print(mu, sd)
    # ratios.plot()
    # plt.axhline(ratios.mean())
    # plt.axhline(mu - 2.5 * sd)
    # plt.axhline(mu - 1.5 * sd)
    # plt.axhline(mu - 0.2 * sd)
    # plt.axhline(mu + 1.5 * sd)
    # plt.axhline(mu + 2.5 * sd)
    # plt.axhline(mu + 0.2 * sd)
    plt.show()
