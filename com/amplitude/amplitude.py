import HuobiService as huobi
import numpy as np
from AmplitudeModel import AmplitudeModel

def takeKey(amplitudeModel):
    return amplitudeModel.amplitude

if __name__ == '__main__':
    symbols = huobi.get_symbols();
    datas = symbols['data']

    symbolsList = []

    for data in datas:
        quote_currency = data['quote-currency']
        if quote_currency == 'usdt':
            symbolsList.append(data['symbol'])

    amplitudeModelList = []

    lineLen = 2000
    for symbol in symbolsList:
        lastClose = 0
        kLine = huobi.get_kline(symbol, '15min', lineLen)

        if kLine is None :
            continue

        print(symbol)

        if kLine['status'] == 'ok' and kLine['data'] and len(kLine['data']) >= lineLen:
            kLine['data'].reverse()
        else:
            continue

        amplitudeList = []

        for data in kLine['data'] :

            if lastClose == 0:
                lastClose = data['close']
                continue

            high = data['high']
            low = data['low']
            amplitude = (high-low)/lastClose

            amplitudeList.append(amplitude)

            lastClose = data['close']

        avg = np.mean(amplitudeList)
        std =  np.std(amplitudeList, ddof=1)
        cv = std/avg;

        amplitudeModel = AmplitudeModel(symbol,avg)
        amplitudeModel.std = std
        amplitudeModel.cv = cv*100
        amplitudeModelList.append(amplitudeModel)

    amplitudeModelList.sort(key=takeKey)
    print(len(amplitudeModelList), "------------------------------------")
    for amplitudeModel in amplitudeModelList:
        print(amplitudeModel.getValue())
