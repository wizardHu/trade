import asyncio
import websockets
import json
import zlib

def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated

async def subscribe_without_login(url, channels):
    async with websockets.connect(url) as websocket:
        sub_param = {"op": "subscribe", "args": channels}
        sub_str = json.dumps(sub_param)
        await  websocket.send(sub_str)
        print(f"send: {sub_str}")

        print("receive:")
        res = await websocket.recv()
        res = inflate(res)
        print(f"{res}")

        res = await websocket.recv()
        res = inflate(res)
        print(f"{res}")

count =1
url = 'wss://real.okex.com:10442/ws/v3'
channels = ["spot/ticker:BTM-USDT"]
while True:
    try:
        asyncio.get_event_loop().run_until_complete(subscribe_without_login(url, channels))
        # asyncio.get_event_loop().run_until_complete(unsubscribe_without_login(url, channels))
        count += 1
        print(count)
    except Exception as err:
        print(err)