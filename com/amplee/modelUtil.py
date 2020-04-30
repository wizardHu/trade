import datetime

import fileOperUtil as fileOperUtil
from JumpQueueModel import JumpQueueModel
from SellOrderModel import SellOrderModel
from TransactionModel import TransactionModel
from BuyModel import BuyModel
from StopLossModel import  StopLossModel
from MySqlConn import MySqlConn
import MyCache as myCache



def getAllPair():
    pairs = []
    mysql = MySqlConn()
    sql = "select * from tb_transaction_config"
    result = mysql.getAll(sql)
    mysql.dispose()
    if result:
        for pair in result:
            symbol = pair['symbol'].decode('utf-8')
            everyExpense = pair['every_expense']
            tradeGap = pair['trade_gap']
            minIncome = pair['min_income']
            period = pair['period'].decode('utf-8')
            precision = pair['precision']
            stopLoss = pair['stopLoss']
            status = pair['status']
            id = pair['id']

            if status == 1:
                tradeModel = TransactionModel(id,symbol, everyExpense, tradeGap, minIncome, period,precision,stopLoss)
                pairs.append(tradeModel)

    return pairs

def insertBuyModel(buyModel):
    myCache.buyModelCache.clear()
    mysql = MySqlConn()
    sql = "insert into tb_buy_record(symbol,price,ori_price,buy_index,amount,order_id,min_income,last_price," \
          "status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    result = mysql.insertOne(sql, (buyModel.symbol, buyModel.price, buyModel.oriPrice, buyModel.index, buyModel.amount,
                                   buyModel.orderId, buyModel.minIncome, buyModel.lastPrice, buyModel.status))

    mysql.dispose()
    if result:
        return result

    return False

def getBuyModel(symbol):
    models = []

    if myCache.buyModelCache.get(symbol,None):
        return myCache.buyModelCache.get(symbol,None)

    mysql = MySqlConn()
    sql = "select * from tb_buy_record where symbol=%s"
    results = mysql.getAll(sql, (symbol))
    mysql.dispose()
    if results:
        for row in results:
            buyModel = BuyModel(row['id'], row['symbol'].decode('utf-8'), row['price'], row['ori_price'], row['buy_index']
                                ,row['amount'], row['order_id'].decode('utf-8'),row['min_income'],row['last_price'],row['status'])
            models.append(buyModel)

    myCache.buyModelCache[symbol] = models
    return models


def modBuyModel(buyModel):
    myCache.buyModelCache.clear()
    mysql = MySqlConn()
    sql = "update tb_buy_record set price=%s,ori_price=%s,buy_index=%s,amount=%s,order_id=%s,min_income=%s," \
          "last_price=%s,status=%s where id=%s"
    result = mysql.update(sql,(buyModel.price,buyModel.oriPrice,buyModel.index,buyModel.amount,buyModel.orderId,buyModel.minIncome
                               ,buyModel.lastPrice,buyModel.status,buyModel.id))
    mysql.dispose()
    if result:
        return True

    return False

def modJumpModel(oldJumpMode,newJumpMode,symbol):
    fileOperUtil.delMsgFromFile(oldJumpMode, "queue/" + symbol + "-queue")
    fileOperUtil.write(newJumpMode, "queue/" + symbol + "-queue")

def modStopLossModel(stopLossModel):
    myCache.stopLossListCache.clear()
    myCache.stopLossCache.clear()
    mysql = MySqlConn()
    sql = "update tb_stop_loss_record set sell_price=%s,ori_price=%s,ori_amount=%s,ori_order_id=%s" \
          ",order_id=%s,status=%s,where id=%s"
    result = mysql.update(sql, (stopLossModel.sellPrice, stopLossModel.oriPrice,stopLossModel.oriAmount,
                                stopLossModel.oriOrderId, stopLossModel.oriOrderId, stopLossModel.orderId,
                                stopLossModel.status, stopLossModel.id))
    mysql.dispose()
    if result:
        return True

    return False


# 得到每次买需要的平均花费
def getAllPairAvgBuyExpense():
    pairsModel = getAllPair()

    count = 0

    for model in pairsModel:
        expense = model.everyExpense
        count += float(expense)

    return float(count/len(pairsModel))

def getStopLossModel(symbol):
    models = []

    if myCache.stopLossListCache.get(symbol,None):
        return myCache.stopLossListCache.get(symbol,None)

    mysql = MySqlConn()
    sql = "select * from tb_stop_loss_record where symbol=%s"

    results = mysql.getAll(sql, (symbol))
    mysql.dispose()
    if results:
        for row in results:
            stopLossModel = StopLossModel(row['id'], row['symbol'].decode('utf-8'), row['sell_price'],
                                          row['ori_price'], row['ori_amount'],
                                          row['ori_order_id'].decode('utf-8')
                                          , row['order_id'].decode('utf-8'), row['status'])

            models.append(stopLossModel)
        myCache.stopLossListCache[symbol] = models

    return models

def getStopLossModelByOrderId(selectOrderId):

    if myCache.stopLossCache.get(selectOrderId,None):
        return myCache.stopLossCache.get(selectOrderId,None)

    mysql = MySqlConn()
    sql = "select * from tb_stop_loss_record where order_id=%s"

    result = mysql.getOne(sql, (selectOrderId))
    mysql.dispose()
    if result:
        stopLossModel = StopLossModel(result['id'], result['symbol'].decode('utf-8'),result['sell_price'], result['ori_price'], result['ori_amount'],
                            result['ori_order_id'].decode('utf-8')
                            , result['order_id'].decode('utf-8'), result['status'])
        myCache.stopLossCache[selectOrderId] = stopLossModel
        return stopLossModel

    return None

def delStopLossModelById(id):

    myCache.stopLossCache.clear()
    myCache.stopLossListCache.clear()

    mysql = MySqlConn()
    sql = "delete from tb_stop_loss_record where id=%s"
    result = mysql.delete(sql, (id))
    mysql.dispose()
    if result:
        return True
    return False

def getBuyModelByOrderId(orderId):
    sql = "select * from tb_buy_record where order_id=%s "
    mysql = MySqlConn()
    result = mysql.getOne(sql, (orderId))
    mysql.dispose()
    if result:
        buyModel = BuyModel(result['id'], result['symbol'].decode('utf-8'), result['price'], result['ori_price'], result['buy_index']
                            ,result['amount'], result['order_id'].decode('utf-8'),result['min_income'],result['last_price'],result['status'])
        return buyModel

    return None

def getJumpModel(symbol):
    lines = fileOperUtil.readAll("queue/"+symbol+"-queue")
    models = []

    #type,orderId,lowPrice,highPrice,jumpPrice,jumpCount
    for model in lines:

        if model != '' and model != '\n':
            params = model.split(',')
            type = params[0]
            orderId = params[1]
            lowPrice = params[2]
            highPrice = params[3]
            jumpPrice = params[4]
            jumpCount = params[5]
            time = params[6]
            price = params[7]

            jumpQueueModel = JumpQueueModel(type, orderId, lowPrice, highPrice,jumpPrice,jumpCount,time,price)
            models.append(jumpQueueModel)

    return models

def getSellOrderModels(symbol):
    lines = fileOperUtil.readAll("sellOrder/"+symbol+"-sellorder")
    models = []

    for model in lines:

        if model != '' and model != '\n':
            params = model.split(',')
            buyPrice = params[0]
            sellPrice = params[1]
            buyIndex = params[2]
            sellIndex = params[3]
            buyOrderId = params[4]
            sellOrderId = params[5]
            amount = params[6]
            time = params[7]

            sellOrderModel = SellOrderModel(buyPrice, sellPrice, buyIndex, sellIndex,buyOrderId,sellOrderId,amount,time)
            models.append(sellOrderModel)

    return models

def delBuyModel(id):
    mysql = MySqlConn()
    sql = "delete from tb_buy_record where id = %s"
    result = mysql.delete(sql, (id))
    mysql.dispose()
    if result:
        return True

    return False

def insertBuySellReocrd(symbol,type,buy_price,sell_price,buy_order_id,sell_order_id,amount,oper_index):
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mysql = MySqlConn()
    sql = "insert into tb_buy_sell_history_record(symbol,type,buy_price,sell_price,buy_order_id,sell_order_id,amount,oper_index," \
          "create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    result = mysql.insertOne(sql, (symbol,type,buy_price,sell_price,buy_order_id,sell_order_id,amount,oper_index,dt))

    mysql.dispose()
    if result:
        return result

    return False

def insertStopLossReocrd(symbol,sell_price,ori_price,ori_amount,ori_order_id,order_id,status):
    myCache.stopLossCache.clear()
    myCache.stopLossListCache.clear()
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mysql = MySqlConn()
    sql = "insert into tb_stop_loss_record(symbol,create_time,sell_price,ori_price,ori_amount,ori_order_id,order_id," \
          "status) values(%s,%s,%s,%s,%s,%s,%s,%s)"

    result = mysql.insertOne(sql, (symbol,dt,sell_price,ori_price,ori_amount,ori_order_id,order_id,status))

    mysql.dispose()
    if result:
        return result

    return False

def insertStopLossHistoryReocrd(symbol,type,oper_price,last_price,amount,ori_order_id,order_id):
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mysql = MySqlConn()
    sql = "insert into tb_stop_loss_history_record(type,symbol,create_time,oper_price,last_price,amount,ori_order_id" \
          ",order_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"

    result = mysql.insertOne(sql, (type,symbol,dt,oper_price,last_price,amount,ori_order_id,order_id))

    mysql.dispose()
    if result:
        return result

    return False

if __name__ == '__main__':
   print(getAllPair())
