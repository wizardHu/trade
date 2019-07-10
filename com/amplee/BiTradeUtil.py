from BuyModel import BuyModel
import fileOperUtil as fileOperUtil
import time
import HuobiService as huobi
import logUtil

def buy(env,buyPrice,amount,symbol,index):
    try:
        orderId = "0000"
        if "pro" == env:
            result = huobi.send_order(amount, "api", symbol, "buy-limit", buyPrice)
            if result['status'] == 'ok':
                orderId = result['data']

        buyModel = BuyModel(buyPrice,index,amount,orderId)
        fileOperUtil.write(buyModel,"buy/"+symbol+"buy")
        fileOperUtil.write(('1,{},{},{},{},{}').format(int(time.time()),buyPrice, amount, index,
                                                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(index))),"record/"+symbol + "-record")

    except Exception as err:
        logUtil.info("BiTradeUtil--buy"+err)

def sell(env,sellPrice,sellIndex,buyModel,symbol):
    try:
        if "pro" == env:
            result = huobi.order_info(buyModel.orderId)
            data = result['data']
            state = data['state']
            if state == 'filled':
                result = huobi.send_order(buyModel.amount, "api", symbol, 'sell-limit', sellPrice)

        fileOperUtil.delMsgFromFile(buyModel,"buy/"+symbol+"buy")
        fileOperUtil.write(('0,{},{},{},{},{},{}').format(int(time.time()),buyModel.price, buyModel.amount,sellPrice,sellIndex,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sellIndex))),"record/"+symbol+"-record")

    except Exception as err:
        logUtil.info("BiTradeUtil--sell"+err)

