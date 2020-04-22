from BuyModel import BuyModel
import fileOperUtil as fileOperUtil
import time
import HuobiService as huobi
import logUtil
import modelUtil as modelUtil
from JumpQueueModel import JumpQueueModel
from StopLossModel import StopLossModel
import random
import commonUtil as commonUtil
from TransactionModel import TransactionModel

# 只是加入了跳跃队列
def buy(buyPrice,amount,symbol,index):
    try:
        orderId = random.randint(0,1999999999)

        decimalLength = commonUtil.calDecimal(buyPrice)

        buyModel = BuyModel(buyPrice,buyPrice,index,amount,orderId,2,buyPrice)
        newJumpModel = JumpQueueModel(1, orderId, round(buyPrice*1.005,decimalLength), round(buyPrice*1.008,decimalLength), round(buyPrice*0.99,decimalLength), 0,
                                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(index)),buyPrice)

        fileOperUtil.write(newJumpModel,"queue/"+symbol+"-queue")
        fileOperUtil.write(buyModel,"buy/"+symbol+"buy")

        return True
    except Exception as err:
        logUtil.info("BiTradeUtil--buy"+err)
    return False

# 这里才是真正实现买操作
def jumpBuy(env,buyPrice,jumpQueueModel,transactionModel,index):
    try:
        symbol = transactionModel.symbol
        orderId = jumpQueueModel.orderId
        buyModel = modelUtil.getBuyModelByOrderId(symbol,orderId)
        newAmount = round(float(transactionModel.everyExpense) / buyPrice, int(transactionModel.precision))
        if "pro" == env:
            result = huobi.send_order(newAmount, "api", symbol, "buy-limit", buyPrice)
            logUtil.info("buy result",result,symbol,newAmount,buyPrice)
            if result['status'] == 'ok':
                orderId = result['data']
            else:
                return False
        else:
            huobi.send_order_dev(newAmount, 1, buyPrice)

        newBuyModel = BuyModel(buyPrice,buyModel.price,index,newAmount,orderId,transactionModel.minIncome,buyPrice)
        modelUtil.modBuyModel(buyModel, newBuyModel, symbol)
        fileOperUtil.delMsgFromFile(jumpQueueModel,"queue/"+symbol+"-queue")

        jumpProfit = (float(jumpQueueModel.oriPrice) - buyPrice )* float(newAmount)
        huobi.jumpProfit = huobi.jumpProfit + jumpProfit
        fileOperUtil.write(jumpQueueModel.getValue(), "queue/" + symbol + "-queuerecord")

        fileOperUtil.write(('1,{},{},{},{},{},{}').format(int(time.time()),index,buyPrice,newAmount,orderId,
                                                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))),"record/"+symbol + "-record")

        return True
    except Exception as err:
        logUtil.info("BiTradeUtil--jumpBuy"+err)
    return False

# 正常卖
def sell(env,sellPrice,sellIndex,buyModel,symbol):
    try:

        decimalLength = commonUtil.calDecimal(sellPrice)

        newBuyModel = BuyModel(buyModel.price, buyModel.oriPrice, buyModel.index, buyModel.amount, buyModel.orderId, 3, buyModel.lastPrice)
        # newJumpModel = JumpQueueModel(2, buyModel.orderId, round(sellPrice * 0.992, decimalLength),
        #                               round(sellPrice * 0.995, decimalLength), round(sellPrice * 1.01, decimalLength), 0,
        #                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sellIndex)),sellPrice)

        #统计发现，因为提高了最低收入值，因此不大可能会再次触发跳跃
        newJumpModel = JumpQueueModel(2, buyModel.orderId, sellPrice,sellPrice , round(sellPrice * 1.01, decimalLength), 0,
                                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sellIndex)), sellPrice)

        fileOperUtil.write(newJumpModel, "queue/" + symbol + "-queue")
        modelUtil.modBuyModel(buyModel,newBuyModel,symbol)

    except Exception as err:
        logUtil.info("BiTradeUtil--sell"+err)

# 这里才是真正实现卖操作
def jumpSell(env,sellPrice,jumpQueueModel,transactionModel,index):
    try:

        symbol = transactionModel.symbol
        orderId = jumpQueueModel.orderId
        buyModel = modelUtil.getBuyModelByOrderId(symbol, orderId)
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

        fileOperUtil.delMsgFromFile(jumpQueueModel, "queue/" + symbol + "-queue")
        fileOperUtil.delMsgFromFile(buyModel,"buy/"+symbol+"buy")
        fileOperUtil.write(jumpQueueModel.getValue(), "queue/" + symbol + "-queuerecord")

        fileOperUtil.write(('0,{},{},{},{},{},{},{}').format(int(time.time()),index,buyModel.price, buyModel.amount,buyModel.orderId,sellPrice,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))),"record/"+symbol+"-record")

    except Exception as err:
        logUtil.info("BiTradeUtil--jumpSell"+err)

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
        #在{什么时候} 以 {什么价格} 卖出 {原价是什么} 的 {多少个} {原来的orderId} {这次的orderId} {状态}
        fileOperUtil.write(
            ('{},{},{},{},{},{},{}').format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),sellPrice, buyModel.price, buyModel.amount, buyModel.orderId,orderId,0)
            ,"stopLossSell/" + symbol + "-sell")

        #记录日志
        # 在{什么时候} 以 {什么价格} 卖出 {原价是什么} 的 {多少个} {原来的orderId} {这次的orderId}
        fileOperUtil.write(
            ('0,{},{},{},{},{},{}').format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                         sellPrice, buyModel.price, buyModel.amount, buyModel.orderId, orderId)
            , "stopLossSellRecoed/" + symbol + "-sellRecord")


    except Exception as err:
        logUtil.info("BiTradeUtil--stopLossSell"+err)


#买入因止损卖出的
def stopLossBuy(env,price,stopLossModel,symbol,index):
    try:

        decimalLength = commonUtil.calDecimal(price)
        newStopLossModel = StopLossModel(stopLossModel.time, stopLossModel.sellPrice, stopLossModel.oriPrice, stopLossModel.oriAmount,stopLossModel.oriOrderId,stopLossModel.orderId,1)

        newJumpModel = JumpQueueModel(3, stopLossModel.orderId, round(price * 1.005, decimalLength),
                                      round(price * 1.008, decimalLength), round(price * 0.99, decimalLength), 0,
                                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),price)

        fileOperUtil.write(newJumpModel, "queue/" + symbol + "-queue")
        modelUtil.modStopLossModel(stopLossModel,newStopLossModel,symbol)


    except Exception as err:
        logUtil.info("BiTradeUtil--stopLossBuy"+err)


#买入因止损卖出的  真正执行卖逻辑
def stopLossJumpBuy(env,buyPrice,jumpQueueModel,transactionModel,index):
    try:
        symbol = transactionModel.symbol
        orderId = jumpQueueModel.orderId
        stopLossModel = modelUtil.getStopLossModelByOrderId(symbol,orderId)
        if stopLossModel is None:
            logUtil.info("jumpQueueModel=",jumpQueueModel," is none")
            return

        buyModel = modelUtil.getBuyModelByOrderId(symbol, stopLossModel.oriOrderId)
        if "pro" == env:
            result = huobi.send_order(float(buyModel.amount), "api", symbol, "buy-limit", buyPrice)
            logUtil.info("buy result", result, symbol, buyModel.amount, buyPrice)
            if result['status'] == 'ok':
                orderId = result['data']
            else:
                return False
        else:
            huobi.send_order_dev(buyModel.amount, 1, buyPrice)

        # 计算新的价格
        length = commonUtil.calDecimal(buyPrice)
        newPrice = round(float(buyModel.price) - (float(stopLossModel.sellPrice)-float(buyPrice)), length)

        newBuyModel = BuyModel(newPrice,buyModel.oriPrice, buyModel.index, buyModel.amount, buyModel.orderId, transactionModel.minIncome,buyPrice)
        modelUtil.modBuyModel(buyModel, newBuyModel, symbol)
        fileOperUtil.delMsgFromFile(stopLossModel, "stopLossSell/"+symbol+"-sell")
        fileOperUtil.delMsgFromFile(jumpQueueModel, "queue/" + symbol + "-queue")

        jumpProfit = (float(jumpQueueModel.oriPrice) - buyPrice) * float(buyModel.amount)
        huobi.jumpProfit = huobi.jumpProfit + jumpProfit
        fileOperUtil.write(jumpQueueModel.getValue(), "queue/" + symbol + "-queuerecord")

        #记录日志
        # 在{什么时候} 以 {什么价格} 买入 {原价是什么} 的 {多少个} {原来的orderId} {这次的orderId}
        fileOperUtil.write(
            ('1,{},{},{},{},{},{}').format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                         buyPrice, stopLossModel.oriPrice, stopLossModel.oriAmount, stopLossModel.oriOrderId, orderId)
            , "stopLossSellRecoed/" + symbol + "-sellRecord")


    except Exception as err:
        logUtil.info("BiTradeUtil--stopLossJumpBuy"+err)

if __name__ == '__main__':
    transactionModel = TransactionModel("eosusdt", 10, 0.02, 0.025, "1min", 2, 0.1)

    #验证买
    # buy(2.823, 3.52, "eosusdt", int(time.time()));

    # 验证jumpBuy买
    # jumpQueueModel = JumpQueueModel(1,610219755,2.837,2.846,2.795,0,"2020-04-17 17:56:01")
    # jumpBuy("dev", 2.837, jumpQueueModel, transactionModel)

    # 验证卖
    # buyModel = BuyModel(2.54,2.823,1587117361,3.52,610219755,0.025,2.203)
    # sell("dev",2.854,int(time.time()),buyModel,"eosusdt")

    # 验证jump卖
    jumpQueueModel = JumpQueueModel(2,610219755,2.831,2.84,2.883,0,"2020-04-17 18:05:44")
    jumpSell("dev", 2.903, jumpQueueModel, transactionModel)

    #验证止损卖
    # buyModel = BuyModel(2.837,2.823,1587117361,3.52,610219755,0.025,2.837)
    # stopLossSell("dev",2.5,buyModel,"eosusdt")

    # 验证止损买
    # stopLossModel = StopLossModel("2020-04-17 17:57:40",2.5,2.837,3.52,610219755,298050635,0)
    # stopLossBuy("dev",2.302,stopLossModel,"eosusdt")

    # 验证jump止损买
    # jumpQueueModel = JumpQueueModel(3,298050635,2.314,2.32,2.279,0,"2020-04-17 18:02:33")
    #     # stopLossJumpBuy("dev", 2.203, jumpQueueModel, transactionModel)

