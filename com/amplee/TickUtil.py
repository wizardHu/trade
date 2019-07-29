import logUtil

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
    if data and "ok" == data['status']:
        for tick in data['tick']['data']:
            lastId = lastTickId.get(symbol,0)
            nowId = tick['id']

            if lastId != nowId:
                lastTickId[symbol] = nowId
                print(tick['amount'],tick['price'],tick['direction'],symbol)