import matplotlib.pyplot as plt
import HuobiService as huobi
import pandas as pd
import numpy as np

def zscore(series):
    return (series - series.mean()) / np.std(series)


if __name__ == '__main__':
    firstLine = huobi.get_kline('xlmusdt', '1min', 110)
    secondLine = huobi.get_kline('omgusdt', '1min', 110)

    firstLine['data'].reverse()
    secondLine['data'].reverse()
    firstData = []
    secondData = []
    for index in range(min(len(firstLine['data']), len(secondLine['data']))):
        firstData.append(firstLine['data'][index]['close'])
        secondData.append(secondLine['data'][index]['close'])

    X = pd.Series(firstData, name='X')
    Y = pd.Series(secondData, name='Y')

    # pd.concat([Y], axis=1).plot(figsize=(10,7))
    # pd.concat([X], axis=1).plot(figsize=(10,7))
    # (X / Y).plot(figsize=(10, 7))
    # plt.axhline((X / Y).mean(), color='red', linestyle='--')
    # plt.show()

    ratios = Y - 24.3042*X
    zscore(ratios).plot()
    plt.axhline(zscore(ratios).mean())
    plt.axhline(1.0, color='red')
    plt.axhline(-1.0, color='green')
    plt.show()
