# -*- coding: utf-8 -*-
import HuobiService as huobi
import spot_api as spot

if __name__ == '__main__':

    api_key = 'fe31ff24-fcf3-4160-81e9-69f1d0509dc3'


    spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)

    test = spotAPI.get_kline('eos-USDT', '', '', 60)
    data = test
    data.reverse()
    print(data)

    test2 = huobi.get_kline('eosusdt', '1min', 200)
    data2 = test2['data']
    data2.reverse()
    print(data2)

    count = 0
    amount = 1

    for i in range(0,200):
        close1 = float(data[i][4])
        close2 = float(data2[i]['close'])

        if close1 > close2:
            fei = close1 * 0.0015 + close2 * 0.002
            gap = close1-close2
            if gap > fei:
                print(close1,close2,gap,fei,gap-fei,"aaaa")
                count += gap-fei

        if close1 < close2:
            fei = close1 * 0.0015 +  close2 * 0.002
            gap = (close2-close1)
            if gap > fei:
                print(close1,close2,gap,fei,gap-fei,"bbbb")
                count += gap-fei

    print(count)

    # while True:
    #
    #     try:
    #         okex = client.getKline(1, "eos_usdt")
    #         huo = huobi.get_kline('eosusdt', '1min', 1)
    #
    #         okexData = okex['data']
    #         huoData = huo['data']
    #
    #         okexclose = okexData[0]['close']
    #         huoclose = huoData[0]['close']
    #
    #         print(okexclose,huoclose)
    #
    #         if okexclose > huoclose:
    #             fei = okexclose * 0.002 + huoclose * 0.002
    #             gap = okexclose - huoclose
    #             if gap > fei:
    #                 print(okexclose, huoclose, gap,"aaaaa")
    #
    #         if okexclose < huoclose:
    #             fei = okexclose * 0.002 + huoclose * 0.002
    #             gap = huoclose - okexclose
    #             if gap > fei:
    #                 print(okexclose, huoclose, gap, gap - fei,"aaaaa")
    #     except Exception as err:
    #         print('connect https error,retry...', err)
