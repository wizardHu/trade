import logUtil
import time
from TickModel import TickModel

tickDict = {}
lastTickId = {}

# {'status': 'ok', 'ch': 'market.eosusdt.trade.detail', 'ts': 1564407471709,
# 'tick': {'id': 101645400148, 'ts': 1564407470567,
# 'data': [
# {'amount': 11.3896, 'ts': 1564407470567, 'id': 10164540014842590792840, 'price': 4.2257, 'direction': 'buy'},
# {'amount': 5.9466, 'ts': 1564407470567, 'id': 10164540014842590792829, 'price': 4.2257, 'direction': 'buy'},
# {'amount': 41.6557, 'ts': 1564407470567, 'id': 10164540014842590788489, 'price': 4.2258, 'direction': 'buy'}
# ]}}
def add(data,symbol):
    global tickDict
    global lastTickId

    if data and "ok" == data['status']:
        for tick in data['tick']['data']:
            lastIds = lastTickId.get(symbol,[0])

            nowId = tick['id']
            ts = tick['ts']

            if len(lastIds) == 0 or nowId not in lastIds:#该交易id未处理过
                lastIds.append(nowId)

                curTs = str(int(ts / 1000))

                ticks = tickDict.get(symbol, {})#得到该交易对的所有交易数据
                tickModel = ticks.get(curTs, TickModel(0,0))#根据秒时间戳得到对应的交易量

                if tick['direction'] == 'buy':
                    tickModel.buySum = tickModel.buySum + float(tick['amount'])
                elif tick['direction'] == 'sell':
                    tickModel.sellSum = tickModel.sellSum + float(tick['amount'])

                ticks[curTs] = tickModel

                #过滤掉2天前的数据
                p2 = dict((key, value) for key, value in ticks.items() if int(key)-int(time.time()) > 60*60*48)

                tickDict[symbol] = p2

                #交易id每个交易对只保留最近20个
                if len(lastIds) > 20:
                    lastIds = lastIds[1:]

                lastTickId[symbol] = lastIds

                print(tickDict)