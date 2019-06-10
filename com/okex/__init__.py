# -*- coding: utf-8 -*-
import HuobiService as huobi
import spot_api as spot
import time
import logging

# 1.初始化日志默认配置
logging.basicConfig(filename='./my.log',                                                 # 日志输出文件
                    level=logging.INFO,                                                 # 日志写入级别
                    datefmt='%Y-%m-%d %H:%M:%S',                                         # 时间格式
                    format='%(asctime)s Line:%(lineno)s==>%(message)s')    # 日志写入格式


def write(msg,fileName):
    f = open(fileName,'a',encoding='utf-8')
    f.write("{0}\n".format(msg))
    f.flush()
    f.close()

if __name__ == '__main__':
    api_key = 'fe31ff24-fcf3-4160-81e9-69f1d0509dc3'


    spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)
    amount = 10.0

    symbol = "btmusdt"
    symbol2 = "BTM-USDT"

    while True:
        try:
            okexResult = spotAPI.get_specific_ticker(symbol2)
            huobiResult = huobi.get_ticker(symbol)

            okClose = float(okexResult['last'])
            huoBiClose = float(huobiResult['tick']['close'])

            okCharge = okClose*amount*0.0015
            huoBiCharge = huoBiClose * amount * 0.002
            charge = okCharge + huoBiCharge

            logging.info(('okClose={} huoBiClose={} charge={}').format(okClose, huoBiClose, charge))

            if (okClose - huoBiClose) > charge:#OK卖出 火币买入
                result = spotAPI.take_order('limit', 'sell', symbol2,amount, price=str(okClose))
                if result['result']:
                    huobi.send_order(amount, "api", symbol, 'buy-limit', huoBiClose)
                    write(('sellok {} buyhuobi {} charge {} profit {}').format(okClose, huoBiClose, charge,okClose - huoBiClose-charge),symbol)

            if (huoBiClose - okClose ) > charge:#OK买入 火币卖出
                result = huobi.send_order(amount, "api", symbol, 'sell-limit', huoBiClose)
                if result['status'] == 'ok':
                    spotAPI.take_order('limit', 'buy', symbol2, amount, price=str(okClose))
                    write(('sellhuobi {} buyok {} charge {} profit {}').format(huoBiClose, okClose, charge,huoBiClose - okClose - charge),symbol)

        except Exception as err:
            logging.info('connect https error,retry...',err)
            time.sleep(1)