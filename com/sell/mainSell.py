import HuobiService as huobi
import KDJ as KDJ
import priceUtil as priceUtil
import Boll as Boll
import Amount as Amount
import TradeUtil as TradeUtil
import time
import logging

# 1.初始化日志默认配置
logging.basicConfig(filename='./my.log',                                                 # 日志输出文件
                    level=logging.INFO,                                                 # 日志写入级别
                    datefmt='%Y-%m-%d %H:%M:%S',                                         # 时间格式
                    format='%(asctime)s Line:%(lineno)s==>%(message)s')    # 日志写入格式


if __name__ == '__main__':
    symbols = 'eosusdt'
    bi = 'eos'
    env = "pro"
    test = huobi.get_kline(symbols, '1min', 1000)
    test['data'].reverse()

    # a = test['data'][:1000]
    # b = test['data'][1000:]

    for data in test['data']:
        index = test['data'].index(data)
        close = data['close']

        priceUtil.add(data, index)
        KDJ.calKDJ(data, index)

    # for data in a:
    #     index = a.index(data)
    #     close = data['close']
    #
    #     priceUtil.add(data, index)
    #     KDJ.calKDJ(data, index)

    lastId = 0
    count = 0
    lastDate = huobi.get_kline(symbols, '1min', 1)

    while True:
    # for data in b:
        try:
            test = huobi.get_kline(symbols, '1min', 1)
            test['data'].reverse()
            logging.info(test['data'])

            data = test['data'][0]

            if lastId != data['id']:

                close = data['close']
                bollFlag = True
                kdjFlag = True
                amountFlag = True
                priceUtil.add(data, count)
                # kdjFlag = KDJ.judgeSell(index)
                bollFlag = Boll.judgeBoll(data, count)
                amountFlag = Amount.judgeAmount(data, count)
                sellFlag = TradeUtil.canSell(symbols, close,bi,env)
                logging.info(('bollFlag={} amountFlag={} sellFlag={} \n').format(bollFlag,amountFlag,sellFlag))
                if kdjFlag and bollFlag and amountFlag and sellFlag:
                    TradeUtil.sell(env,symbols,close)

                canBuyLists = TradeUtil.getBuyModel(symbols, close, env)

                for buyRecord in canBuyLists:
                    #买入
                    TradeUtil.sendBuy(env,buyRecord)

                count += 1

            lastId = data['id']
            time.sleep(1)
        except Exception as err:
            logging.info('connect https error,retry...', err)
            time.sleep(1)


