# -*- coding: utf-8 -*-
#author: 半熟的韭菜

from websocket import create_connection
import gzip
import time

if __name__ == '__main__':
    
    while(1):
        try:
            ws = create_connection("wss://api.huobipro.com/ws")
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)

    # 订阅 KLine 数据
    tradeStr="""{"sub": "market.eosusdt.kline.1min","id": "id10"}"""

    ws.send(tradeStr)
    while(1):
        compressData=ws.recv()
        result=gzip.decompress(compressData).decode('utf-8')
        if result[:7] == '{"ping"':
            ts=result[8:21]
            pong='{"pong":'+ts+'}'
            ws.send(pong)
            ws.send(tradeStr)
        else:
            if 'ts' in result:
                
                a = result['ts']
#                 timestamp = a/1000
#                 time_local = time.localtime(timestamp)
#                 id = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
                print(id,result)

    
