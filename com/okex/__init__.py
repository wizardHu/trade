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

if __name__ == '__main__':
    api_key = 'fe31ff24-fcf3-4160-81e9-69f1d0509dc3'


    spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)
    amount = 1.0
    count = 0

    while True:
        try:
            okexResult = spotAPI.get_ticker()

            for data in okexResult:
                symbol = data['instrument_id']
                index = symbol.find('-USDT')
                if index >= 0:

                    huoBiSymbol = symbol[0:index].lower()+'usdt'

                    huobiResult = huobi.get_ticker(huoBiSymbol)

                    if huobiResult and huobiResult['status'] == 'ok':

                        okClose = float(data['last'])
                        huoBiClose = float(huobiResult['tick']['close'])

                        okCharge = okClose*amount*0.0015
                        huoBiCharge = huoBiClose * amount * 0.002
                        charge = okCharge + huoBiCharge

                        print(okClose, huoBiClose,charge)

                        if (okClose - huoBiClose) > charge:#OK卖出 火币买入
                            print('sell ok=',okClose,' buy huobi ',huoBiClose,' symbol=',huoBiSymbol)
                            count += okClose - huoBiClose-charge

                        if (huoBiClose - okClose ) > charge:#OK买入 火币卖出
                            print('sell huobi=',huoBiClose,' buy ok ',okClose,' symbol=',huoBiSymbol)
                            count += huoBiClose - okClose - charge

                    print(count)

        except Exception as err:
            logging.info('connect https error,retry...',err)
            time.sleep(1)