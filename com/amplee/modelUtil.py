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
            symbol = pair['symbol']
            everyExpense = pair['every_expense']
            tradeGap = pair['trade_gap']
            minIncome = pair['min_income']
            period = pair['period']
            precision = pair['precision']
            stopLoss = pair['stopLoss']
            status = pair['status']
            id = pair['id']
            pricePrecision = pair['price_precision']

            if status == 1:
                tradeModel = TransactionModel(id,symbol, everyExpense, tradeGap, minIncome, period,precision,stopLoss,pricePrecision)
                pairs.append(tradeModel)

    return pairs

######################BUYMODEL##############################

def insertBuyModel(buyModel):
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    myCache.buyModelCache.clear()
    myCache.buyModelIsNone = False
    mysql = MySqlConn()
    sql = "insert into tb_buy_record(symbol,price,ori_price,buy_index,amount,order_id,min_income,last_price," \
          "status,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    result = mysql.insertOne(sql, (buyModel.symbol, buyModel.price, buyModel.oriPrice, buyModel.index, buyModel.amount,
                                   buyModel.orderId, buyModel.minIncome, buyModel.lastPrice, buyModel.status,dt))

    mysql.dispose()
    if result:
        return result

    return False

def getBuyModel(symbol,env):
    models = []

    if "dev" == env:
        if myCache.buyModelIsNone:
            return models

        if myCache.buyModelCache.get(symbol,None):
            return myCache.buyModelCache.get(symbol,None)

    mysql = MySqlConn()
    sql = "select * from tb_buy_record where symbol=%s"
    results = mysql.getAll(sql, (symbol))
    mysql.dispose()
    if results:
        for row in results:
            buyModel = BuyModel(row['id'], row['symbol'], row['price'], row['ori_price'], row['buy_index']
                                ,row['amount'], row['order_id'],row['min_income'],row['last_price'],row['status'])
            models.append(buyModel)

        myCache.buyModelIsNone = False
        myCache.buyModelCache[symbol] = models
    else:
        myCache.buyModelIsNone = True
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

def getBuyModelByOrderId(orderId):
    sql = "select * from tb_buy_record where order_id=%s "
    mysql = MySqlConn()
    result = mysql.getOne(sql, (orderId))
    mysql.dispose()
    if result:
        buyModel = BuyModel(result['id'], result['symbol'], result['price'], result['ori_price'], result['buy_index']
                            ,result['amount'], result['order_id'],result['min_income'],result['last_price'],result['status'])
        return buyModel

    return None

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

def getBuyModelBySymbolAndStatus(symbol,status):
    sql = "select * from tb_buy_record where symbol=%s and status=%s"
    mysql = MySqlConn()
    result = mysql.getOne(sql, (symbol,status))
    mysql.dispose()
    if result:
        buyModel = BuyModel(result['id'], result['symbol'], result['price'], result['ori_price'], result['buy_index']
                            ,result['amount'], result['order_id'],result['min_income'],result['last_price'],result['status'])
        return buyModel

    return None

######################JUMP##############################

def modJumpModel(jumpQueueModel):
    myCache.jumpQueueModelCache.clear()
    mysql = MySqlConn()
    sql = "update tb_jump_queue_record set low_price=%s,high_price=%s,jump_price=%s,jump_count=%s where id=%s"
    result = mysql.update(sql, (jumpQueueModel.lowPrice,jumpQueueModel.highPrice,jumpQueueModel.jumpPrice,jumpQueueModel.jumpCount,
                                jumpQueueModel.id))
    mysql.dispose()
    if result:
        return True

    return False

def delJumpModelById(id):
    myCache.jumpQueueModelCache.clear()

    mysql = MySqlConn()
    sql = "delete from tb_jump_queue_record  where id=%s"
    result = mysql.delete(sql, (id))
    mysql.dispose()
    if result:
        return True
    return False


def getJumpModel(symbol,env):
    models = []

    if "dev" == env:
        if myCache.jumpQueueModelIsNone:
            return models

        if myCache.jumpQueueModelCache.get(symbol, None):
            return myCache.jumpQueueModelCache.get(symbol, None)

    mysql = MySqlConn()
    sql = "select * from tb_jump_queue_record where symbol=%s"

    results = mysql.getAll(sql, (symbol))
    mysql.dispose()
    if results:
        for row in results:
            jumpQueueModel = JumpQueueModel(row['id'], row['symbol'], row['type'],
                                          row['order_id'], row['low_price'],
                                          row['high_price'],row['jump_price']
                                          , row['jump_count'], row['ori_price'])

            models.append(jumpQueueModel)
        myCache.jumpQueueModelCache[symbol] = models
        myCache.jumpQueueModelIsNone = False
    else:
        myCache.jumpQueueModelIsNone = True

    return models

def insertJumpQueueModel(jumpQueueModel):
    myCache.jumpQueueModelCache.clear()
    myCache.jumpQueueModelIsNone = False
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mysql = MySqlConn()
    sql = "insert into tb_jump_queue_record(symbol,type,order_id,low_price,high_price,jump_price,jump_count" \
          ",create_time,ori_price) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    result = mysql.insertOne(sql, (jumpQueueModel.symbol,jumpQueueModel.type,jumpQueueModel.orderId,jumpQueueModel.lowPrice,
                                   jumpQueueModel.highPrice,jumpQueueModel.jumpPrice,jumpQueueModel.jumpCount,dt,jumpQueueModel.oriPrice))

    mysql.dispose()
    if result:
        return result

    return False

def insertHistoryJumpQueueModel(jumpQueueModel,oper_price,amount):
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mysql = MySqlConn()
    sql = "insert into tb_jump_queue_history_record(symbol,type,order_id,low_price,high_price,jump_price,jump_count" \
          ",create_time,ori_price,oper_price,amount) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    result = mysql.insertOne(sql, (jumpQueueModel.symbol,jumpQueueModel.type,jumpQueueModel.orderId,jumpQueueModel.lowPrice
                                   ,jumpQueueModel.highPrice,jumpQueueModel.jumpPrice,jumpQueueModel.jumpCount,dt,
                                   jumpQueueModel.oriPrice,oper_price,amount))

    mysql.dispose()
    if result:
        return result

    return False

######################StopLoss##############################

def modStopLossModel(stopLossModel):
    myCache.stopLossListCache.clear()
    myCache.stopLossCache.clear()
    mysql = MySqlConn()
    sql = "update tb_stop_loss_record set sell_price=%s,ori_price=%s,ori_amount=%s,ori_order_id=%s" \
          ",order_id=%s,status=%s where id=%s"
    result = mysql.update(sql, (stopLossModel.sellPrice, stopLossModel.oriPrice,stopLossModel.oriAmount,
                                stopLossModel.oriOrderId,  stopLossModel.orderId,
                                stopLossModel.status, stopLossModel.id))
    mysql.dispose()
    if result:
        return True

    return False

def getStopLossModel(symbol,env):
    models = []

    if "dev" == env:
        if myCache.stopLossIsNone:
            return models

        if myCache.stopLossListCache.get(symbol,None):
            return myCache.stopLossListCache.get(symbol,None)

    mysql = MySqlConn()
    sql = "select * from tb_stop_loss_record where symbol=%s"

    results = mysql.getAll(sql, (symbol))
    mysql.dispose()
    if results:
        for row in results:
            stopLossModel = StopLossModel(row['id'], row['symbol'], row['sell_price'],
                                          row['ori_price'], row['ori_amount'],
                                          row['ori_order_id']
                                          , row['order_id'], row['status'])

            models.append(stopLossModel)
        myCache.stopLossListCache[symbol] = models
        myCache.stopLossIsNone = False
    else:
        myCache.stopLossIsNone = True

    return models

def getStopLossModelByOrderId(selectOrderId):

    if myCache.stopLossCache.get(selectOrderId,None):
        return myCache.stopLossCache.get(selectOrderId,None)

    mysql = MySqlConn()
    sql = "select * from tb_stop_loss_record where order_id=%s"

    result = mysql.getOne(sql, (selectOrderId))
    mysql.dispose()
    if result:
        stopLossModel = StopLossModel(result['id'], result['symbol'],result['sell_price'], result['ori_price'], result['ori_amount'],
                            result['ori_order_id']
                            , result['order_id'], result['status'])
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

def insertStopLossReocrd(symbol,sell_price,ori_price,ori_amount,ori_order_id,order_id,status):
    myCache.stopLossCache.clear()
    myCache.stopLossListCache.clear()
    myCache.stopLossIsNone = False
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

######################SellOrderModel##############################

def getSellOrderModels(symbol,env):
    models = []

    if "dev" == env:
        if myCache.sellOrderIsNone:
            return models

        if myCache.sellOrderCache.get(symbol, None):
            return myCache.sellOrderCache.get(symbol, None)

    mysql = MySqlConn()
    sql = "select * from tb_sell_order_record where symbol=%s"

    results = mysql.getAll(sql, (symbol))
    mysql.dispose()
    if results:
        for row in results:
            sellOrderModel = SellOrderModel(row["id"], row["symbol"], row["buy_price"],
                                            row["sell_price"], row["buy_index"], row["sell_index"], row["buy_orderId"],
                                            row["sell_orderId"],row["amount"])
            models.append(sellOrderModel)

        myCache.sellOrderCache[symbol] = models
        myCache.sellOrderIsNone = False
    else:
        myCache.sellOrderIsNone = True

    return models

def insertSellOrderReocrd(sellOrderModel):
    myCache.sellOrderIsNone = False
    myCache.sellOrderCache.clear()

    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mysql = MySqlConn()
    sql = "insert into tb_sell_order_record(symbol,buy_price,sell_price,buy_index,sell_index,buy_orderId,sell_orderId" \
          ",amount,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    result = mysql.insertOne(sql, (sellOrderModel.symbol,sellOrderModel.buyPrice,sellOrderModel.sellPrice,sellOrderModel.buyIndex
                                   ,sellOrderModel.sellIndex,sellOrderModel.buyOrderId,sellOrderModel.sellOrderId
                                   ,sellOrderModel.amount,dt))

    mysql.dispose()
    if result:
        return result

    return False

def delSellOrderById(id):
    myCache.sellOrderCache.clear()

    mysql = MySqlConn()
    sql = "delete from tb_sell_order_record where id=%s"
    result = mysql.delete(sql, (id))
    mysql.dispose()
    if result:
        return True

    return False


######################OTHER##############################

# 得到每次买需要的平均花费
def getAllPairAvgBuyExpense():
    pairsModel = getAllPair()

    count = 0

    for model in pairsModel:
        expense = model.everyExpense
        count += float(expense)

    return float(count/len(pairsModel))


def insertKLineReocrd(data,symbol):

    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00")
    mysql = MySqlConn()
    sql = "insert into tb_kline_record(symbol,open,close,high,low,amount,count" \
          ",vol,line_index,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    result = mysql.insertOne(sql, (symbol,data['open'],data['close'],data['high'],data['low']
                                   ,data['amount'],data['count'],data['vol']
                                   ,data['id'],dt))

    mysql.dispose()
    if result:
        return result

    return False

if __name__ == '__main__':

    # data = {"data": [{"open": 0.19629, "id": 1587721980, "count": 29, "amount": 36697.23, "close": 0.1963, "vol": 7200.5755178, "high": 0.1963, "low": 0.19613}]}
    #
    # print(insertKLineReocrd(data['data'][0],"eosusdt"))
    if getBuyModelBySymbolAndStatus("eowsusdt",0) is None:
        print(True)
    else:
        print(False)