import numpy as np
import HuobiService as huobi

if __name__ == '__main__':
    symbols = huobi.get_symbols();
    datas = symbols['data']

    symbolsList = []

    for data in datas:
        quote_currency = data['quote-currency']
        if quote_currency == 'usdt':
            symbolsList.append(data['symbol'])

    print(symbolsList)