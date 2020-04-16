from BuyModel import BuyModel
import fileOperUtil as fileOperUtil
import time
import HuobiService as huobi
import logUtil
import modelUtil as modelUtil
from StopLossModel import StopLossModel
import random
import commonUtil as commonUtil

# 只是加入了跳跃队列
def buy(env,buyPrice,amount,symbol,index,minIncome):
    try:
        orderId = random.randint(0,1999999999)
        if "pro" == env:
            result = huobi.send_order(amount, "api", symbol, "buy-limit", buyPrice)
            logUtil.info("buy result",result,symbol,amount,buyPrice)
            if result['status'] == 'ok':
                orderId = result['data']
            else:
                return False
        else:
            huobi.send_order_dev(amount, 1, buyPrice)

        buyModel = BuyModel(buyPrice,buyPrice,index,amount,orderId,minIncome,buyPrice)
        fileOperUtil.write(buyModel,"buy/"+symbol+"buy")
        fileOperUtil.write(('1,{},{},{},{},{}').format(int(time.time()),buyPrice, amount, index,
                                                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(index))),"record/"+symbol + "-record")

        return True
    except Exception as err:
        logUtil.info("BiTradeUtil--buy"+err)
    return False

# 这里才是真正实现买操作
def jumpBuy(env,buyPrice,amount,symbol,index,minIncome):
    try:
        orderId = random.randint(0,1999999999)
        if "pro" == env:
            result = huobi.send_order(amount, "api", symbol, "buy-limit", buyPrice)
            logUtil.info("buy result",result,symbol,amount,buyPrice)
            if result['status'] == 'ok':
                orderId = result['data']
            else:
                return False
        else:
            huobi.send_order_dev(amount, 1, buyPrice)

        buyModel = BuyModel(buyPrice,buyPrice,index,amount,orderId,minIncome,buyPrice)
        fileOperUtil.write(buyModel,"buy/"+symbol+"buy")
        fileOperUtil.write(('1,{},{},{},{},{}').format(int(time.time()),buyPrice, amount, index,
                                                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(index))),"record/"+symbol + "-record")

        return True
    except Exception as err:
        logUtil.info("BiTradeUtil--buy"+err)
    return False

def sell(env,sellPrice,sellIndex,buyModel,symbol):
    try:
        if "pro" == env:
            result = huobi.order_info(buyModel.orderId)
            data = result['data']
            state = data['state']
            logUtil.info("sell result", result, symbol)
            if state == 'filled':
                result = huobi.send_order(buyModel.amount, "api", symbol, 'sell-limit', sellPrice)
                if result['status'] != 'ok':
                    return
            else:
                return
        else:
            huobi.send_order_dev(buyModel.amount, 0, sellPrice)

        fileOperUtil.delMsgFromFile(buyModel,"buy/"+symbol+"buy")
        fileOperUtil.write(('0,{},{},{},{},{},{}').format(int(time.time()),buyModel.price, buyModel.amount,sellPrice,sellIndex,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sellIndex))),"record/"+symbol+"-record")

    except Exception as err:
        logUtil.info("BiTradeUtil--sell"+err)

#达到止损点就要卖出
def stopLossSell(env,sellPrice,buyModel,symbol):
    try:
        orderId = random.randint(0,1999999999)
        if "pro" == env:
            result = huobi.order_info(buyModel.orderId)
            data = result['data']
            state = data['state']
            logUtil.info("stopLossSell result", result, symbol)
            if state == 'filled':
                result = huobi.send_order(buyModel.amount, "api", symbol, 'sell-limit', sellPrice)
                if result['status'] == 'ok':
                    orderId = result['data']
                else:
                    return
            else:
                return
        else:
            huobi.send_order_dev(buyModel.amount, 0, sellPrice)

        newBuyModel = BuyModel(buyModel.price,buyModel.oriPrice, buyModel.index, buyModel.amount, buyModel.orderId, 1,buyModel.lastPrice)
        modelUtil.modBuyModel(buyModel, newBuyModel, symbol)
        #在{什么时候} 以 {什么价格} 卖出 {原价是什么} 的 {多少个} {原来的orderId} {这次的orderId}
        fileOperUtil.write(
            ('{},{},{},{},{},{}').format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),sellPrice, buyModel.price, buyModel.amount, buyModel.orderId,orderId)
            ,"stopLossSell/" + symbol + "-sell")

        #记录日志
        # 在{什么时候} 以 {什么价格} 卖出 {原价是什么} 的 {多少个} {原来的orderId} {这次的orderId}
        fileOperUtil.write(
            ('0,{},{},{},{},{},{}').format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                                         sellPrice, buyModel.price, buyModel.amount, buyModel.orderId, orderId)
            , "stopLossSellRecoed/" + symbol + "-sellRecord")


    except Exception as err:
        logUtil.info("BiTradeUtil--stopLossSell"+err)


#买入因止损卖出的
def stopLossBuy(env,price,stopLossModel,symbol,minInCome):
    try:
        orderId = random.randint(0,1999999999)
        if "pro" == env:
            result = huobi.send_order(stopLossModel.oriAmount, "api", symbol, "buy-limit", price)
            logUtil.info("buy result", result, symbol, stopLossModel.oriAmount, price)
            if result['status'] == 'ok':
                orderId = result['data']
            else:
                return False
        else:
            huobi.send_order_dev(stopLossModel.oriAmount, 1, price)

        oldBuyModel = modelUtil.getBuyModelByOrderId(symbol,stopLossModel.oriOrderId)

        # 计算新的价格
        length = commonUtil.calDecimal(price)
        newPrice = round(float(oldBuyModel.price) - (float(stopLossModel.sellPrice)-float(price)), length)

        newBuyModel = BuyModel(newPrice,oldBuyModel.oriPrice, oldBuyModel.index, oldBuyModel.amount, oldBuyModel.orderId, minInCome,price)
        modelUtil.modBuyModel(oldBuyModel, newBuyModel, symbol)
        fileOperUtil.delMsgFromFile(stopLossModel, "stopLossSell/"+symbol+"-sell")

        #记录日志
        # 在{什么时候} 以 {什么价格} 买入 {原价是什么} 的 {多少个} {原来的orderId} {这次的orderId}
        fileOperUtil.write(
            ('1,{},{},{},{},{},{}').format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
                                         price, stopLossModel.oriPrice, stopLossModel.oriAmount, stopLossModel.oriOrderId, orderId)
            , "stopLossSellRecoed/" + symbol + "-sellRecord")


    except Exception as err:
        logUtil.info("BiTradeUtil--stopLossSell"+err)

if __name__ == '__main__':

    #验证买
    buy("dev", 6500, 0.002, "btcusdt", 123, 0.015);

    # 验证卖
    # buyModel = BuyModel(6500,6500,123,0.002,"0000",0.015)
    # sell("dev",6600,123456,buyModel,"btcusdt")

    #验证止损卖
    # buyModel = BuyModel(6500,6500,123,0.002,"0000",0.015)
    # stopLossSell("dev",6000,buyModel,"btcusdt")

    # 验证止损买
    # stopLossModel = StopLossModel("2020-04-04 20:03:08",6000,6500,0.002,"0000","0000")
    # stopLossBuy("dev", 5800, stopLossModel, "btcusdt", 0.015)

