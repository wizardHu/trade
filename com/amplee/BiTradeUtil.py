from BuyModel import BuyModel
import fileOperUtil as fileOperUtil
import time
import HuobiService as huobi
import logUtil
import modelUtil as modelUtil
from JumpQueueModel import JumpQueueModel
from StopLossModel import StopLossModel
import commonUtil as commonUtil
from TransactionModel import TransactionModel
from SellOrderModel import SellOrderModel

# 只是加入了跳跃队列
def buy(buyPrice,amount,symbol,index,minIncome):
    try:
        orderId = commonUtil.getRandomOrderId()

        decimalLength = commonUtil.calDecimal(buyPrice)

        buyModel = BuyModel(0,symbol,buyPrice,buyPrice,index,amount,orderId,minIncome,buyPrice,2)
        newJumpModel = JumpQueueModel(1, orderId, round(buyPrice*1.005,decimalLength), round(buyPrice*1.008,decimalLength), round(buyPrice*0.99,decimalLength), 0,
                                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(index)),buyPrice)

        if modelUtil.insertBuyModel(buyModel):
            fileOperUtil.write(newJumpModel, "queue/" + symbol + "-queue")
        else:
            logUtil.error("BiTradeUtil--buy insert 0")

        return True
    except Exception as err:
        logUtil.error("BiTradeUtil--buy"+err)
    return False

# 这里才是真正实现买操作
def jumpBuy(env,buyPrice,jumpQueueModel,transactionModel,index):
    try:
        symbol = transactionModel.symbol
        orderId = jumpQueueModel.orderId
        buyModel = modelUtil.getBuyModelByOrderId(orderId)

        if buyModel is None:
            logUtil.info("orderId is null",orderId)
            return

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

        newBuyModel = BuyModel(buyModel.id,buyModel.symbol,buyPrice,buyModel.oriPrice,index,newAmount,orderId,transactionModel.minIncome,buyPrice,0)
        if modelUtil.modBuyModel(newBuyModel):
            fileOperUtil.delMsgFromFile(jumpQueueModel,"queue/"+symbol+"-queue")

            jumpProfit = (float(jumpQueueModel.oriPrice) - buyPrice) * float(newAmount)
            huobi.jumpProfit = huobi.jumpProfit + jumpProfit
            fileOperUtil.write(jumpQueueModel.getValue(), "queue/" + symbol + "-queuerecord")

            modelUtil.insertBuySellReocrd(buyModel.symbol,1,buyPrice,0,orderId,0,newAmount,index)
        else:
            logUtil.error("BiTradeUtil--jumpBuy modBuyModel 0 orderId=",orderId)

        return True
    except Exception as err:
        logUtil.error("BiTradeUtil--jumpBuy"+err)
    return False

# 正常卖
def sell(env,sellPrice,sellIndex,buyModel,symbol):
    try:

        if "pro" == env:
            sellPrice = float(buyModel.price)*(1+float(buyModel.minIncome))

        decimalLength = commonUtil.calDecimal(sellPrice)

        newBuyModel = BuyModel(buyModel.id,buyModel.symbol,buyModel.price, buyModel.oriPrice, buyModel.index,
                               buyModel.amount, buyModel.orderId, buyModel.minIncome, buyModel.lastPrice,3)
        # newJumpModel = JumpQueueModel(2, buyModel.orderId, round(sellPrice * 0.992, decimalLength),
        #                               round(sellPrice * 0.995, decimalLength), round(sellPrice * 1.01, decimalLength), 0,
        #                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sellIndex)),sellPrice)

        #统计发现，因为提高了最低收入值，因此不大可能会再次触发跳跃
        newJumpModel = JumpQueueModel(2, buyModel.orderId, sellPrice,sellPrice , round(sellPrice * 1.01, decimalLength), 0,
                                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sellIndex)), sellPrice)

        if modelUtil.modBuyModel(newBuyModel):
            fileOperUtil.write(newJumpModel, "queue/" + symbol + "-queue")
        else:
            logUtil.error("BiTradeUtil--sell modBuyModel 0 orderId=", buyModel.orderId)


    except Exception as err:
        logUtil.error("BiTradeUtil--sell"+err)

# 这里才是真正实现卖操作
def jumpSell(env,sellPrice,jumpQueueModel,transactionModel,index):
    try:

        sellOrderId = commonUtil.getRandomOrderId()
        symbol = transactionModel.symbol
        orderId = jumpQueueModel.orderId
        buyModel = modelUtil.getBuyModelByOrderId(orderId)
        if "pro" == env:
            #{'status': 'ok', 'data': {'symbol': 'xrpusdt', 'source': 'api', 'field-cash-amount': '0.0', 'price': '0.1972',
            # 'canceled-at': 0, 'field-amount': '0.0', 'type': 'sell-limit', 'state': 'submitted', 'client-order-id': '', 'field-fees': '0.0',
            # 'created-at': 1587721600720, 'account-id': account-id, 'id': 82495000363, 'amount': '26.0000', 'finished-at': 0}}
            result = huobi.order_info(buyModel.orderId)
            data = result['data']
            state = data['state']
            logUtil.info("sell result", result, symbol)
            if state == 'filled':
                #{'status': 'ok', 'data': 'orderId'}
                result = huobi.send_order(buyModel.amount, "api", symbol, 'sell-limit', sellPrice)
                if result['status'] != 'ok':
                    return
                sellOrderId = result['data']

            else:
                return
        else:
            huobi.send_order_dev(buyModel.amount, 0, sellPrice)

        sellOrderModel = SellOrderModel(buyModel.price,sellPrice,buyModel.index,index,buyModel.orderId,sellOrderId,buyModel.amount,
                                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        newBuyModel = BuyModel(buyModel.id,buyModel.symbol,buyModel.price, buyModel.oriPrice, buyModel.index, buyModel.amount, buyModel.orderId, buyModel.minIncome,
                               buyModel.lastPrice,4)
        if modelUtil.modBuyModel(newBuyModel):
            fileOperUtil.delMsgFromFile(jumpQueueModel, "queue/" + symbol + "-queue")
            fileOperUtil.write(jumpQueueModel.getValue(), "queue/" + symbol + "-queuerecord")
            fileOperUtil.write(sellOrderModel, "sellOrder/" + symbol + "-sellorder")
        else:
            logUtil.error("BiTradeUtil--sell jumpSell 0 orderId=", buyModel.orderId)

    except Exception as err:
        logUtil.error("BiTradeUtil--jumpSell"+err)

#达到止损点就要卖出
def stopLossSell(env,sellPrice,buyModel,symbol):
    try:
        orderId = commonUtil.getRandomOrderId()
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

        newBuyModel = BuyModel(buyModel.id,buyModel.symbol,buyModel.price,buyModel.oriPrice, buyModel.index,
                               buyModel.amount, buyModel.orderId, buyModel.minIncome,buyModel.lastPrice,1)

        if modelUtil.modBuyModel(newBuyModel):
            #在{什么时候} 以 {什么价格} 卖出 {原价是什么} 的 {多少个} {原来的orderId} {这次的orderId} {状态}
            insertResult = modelUtil.insertStopLossReocrd(symbol,sellPrice,buyModel.price,buyModel.amount,buyModel.orderId,orderId,0)
            if insertResult is False:
                logUtil.error("insertResult is false", buyModel.orderId)

            #记录日志
            modelUtil.insertStopLossHistoryReocrd(symbol,0,sellPrice, buyModel.price,buyModel.amount, buyModel.orderId, orderId)

        else:
            logUtil.error("BiTradeUtil--sell stopLossSell 0 orderId=", buyModel.orderId," id=",buyModel.id)


    except Exception as err:
        logUtil.error("BiTradeUtil--stopLossSell"+err)


#买入因止损卖出的
def stopLossBuy(env,price,stopLossModel,symbol,index):
    try:

        decimalLength = commonUtil.calDecimal(price)
        newStopLossModel = StopLossModel(stopLossModel.id,stopLossModel.symbol,
                                         stopLossModel.sellPrice, stopLossModel.oriPrice, stopLossModel.oriAmount,
                                         stopLossModel.oriOrderId,stopLossModel.orderId,1)

        newJumpModel = JumpQueueModel(3, stopLossModel.orderId, round(price * 1.005, decimalLength),
                                      round(price * 1.008, decimalLength), round(price * 0.99, decimalLength), 0,
                                      time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),price)

        fileOperUtil.write(newJumpModel, "queue/" + symbol + "-queue")
        modelUtil.modStopLossModel(newStopLossModel)


    except Exception as err:
        logUtil.error("BiTradeUtil--stopLossBuy"+err)


#买入因止损卖出的  真正执行卖逻辑
def stopLossJumpBuy(env,buyPrice,jumpQueueModel,transactionModel,index):
    try:
        symbol = transactionModel.symbol
        orderId = jumpQueueModel.orderId
        stopLossModel = modelUtil.getStopLossModelByOrderId(orderId)
        if stopLossModel is None:
            logUtil.error("jumpQueueModel=",jumpQueueModel," is none")
            return

        buyModel = modelUtil.getBuyModelByOrderId(stopLossModel.oriOrderId)
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

        newBuyModel = BuyModel(buyModel.id,buyModel.symbol,newPrice,buyModel.oriPrice, buyModel.index, buyModel.amount,
                               buyModel.orderId, transactionModel.minIncome,buyPrice,0)

        if modelUtil.modBuyModel(newBuyModel):
            modelUtil.delStopLossModelById(stopLossModel.id)
            fileOperUtil.delMsgFromFile(jumpQueueModel, "queue/" + symbol + "-queue")

            jumpProfit = (float(jumpQueueModel.oriPrice) - buyPrice) * float(buyModel.amount)
            huobi.jumpProfit = huobi.jumpProfit + jumpProfit
            fileOperUtil.write(jumpQueueModel.getValue(), "queue/" + symbol + "-queuerecord")

            # 记录止损买日志
            modelUtil.insertStopLossHistoryReocrd(symbol, 1, buyPrice, stopLossModel.oriPrice, stopLossModel.oriAmount,
                                                  stopLossModel.oriOrderId, orderId)

        else:
            logUtil.error("BiTradeUtil--sell stopLossJumpBuy 0 orderId=", buyModel.orderId)


    except Exception as err:
        logUtil.error("BiTradeUtil--stopLossJumpBuy"+err)

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

