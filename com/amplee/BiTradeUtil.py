from BuyModel import BuyModel
from UrgentSellModel import UrgentSellModel
import fileOperUtil as fileOperUtil
import time
import HuobiService as huobi
import logUtil
import sys
import modelUtil as modelUtil

def buy(env,buyPrice,amount,symbol,index,minIncome):
    try:
        orderId = "0000"
        if "pro" == env:
            result = huobi.send_order(amount, "api", symbol, "buy-limit", buyPrice)
            logUtil.info("buy result",result,symbol,amount,buyPrice)
            if result['status'] == 'ok':
                orderId = result['data']
            else:
                return

        buyModel = BuyModel(buyPrice,index,amount,orderId,minIncome)
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
            else:
                return

        fileOperUtil.delMsgFromFile(buyModel,"buy/"+symbol+"buy")
        fileOperUtil.write(('0,{},{},{},{},{},{}').format(int(time.time()),buyModel.price, buyModel.amount,sellPrice,sellIndex,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sellIndex))),"record/"+symbol+"-record")

    except Exception as err:
        logUtil.info("BiTradeUtil--sell"+err)

def urgentSell(env,sellPrice,sellIndex,buyModel,symbol,minIncome):
    try:
        orderId = "0000"
        if "pro" == env:
            result = huobi.send_order(buyModel.amount, "api", symbol, 'sell-limit', sellPrice)
            logUtil.info("urgentSell result", result, symbol, buyModel.amount, sellPrice)
            if result['status'] == 'ok':
                orderId = result['data']
            else:
                return

        newBuyModel = BuyModel(buyModel.price,buyModel.index,buyModel.amount,buyModel.orderId,1)
        urgentSellModel = UrgentSellModel(buyModel,sellIndex,orderId,sellPrice,minIncome)
        fileOperUtil.write(urgentSellModel, "sell/" + symbol + "sell")
        fileOperUtil.write(('0,{},{},{},{},{},{}').format(int(time.time()),buyModel.price, buyModel.amount,sellPrice,sellIndex,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sellIndex))),"urgentRecord/"+symbol+"-recordLog")
        modelUtil.modBuyModel(buyModel,newBuyModel,symbol)

    except Exception as err:
        logUtil.info("BiTradeUtil--urgentSell"+err)

if __name__ == '__main__':
    data = huobi.get_kline(sys.argv[1], sys.argv[2], sys.argv[3])
    print(data)

