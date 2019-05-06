from TradeModel import TradeModel
import fileUtil as fileUtil
import MyHuobiService as myHuo

def canSell(symbol,close):
    tradeModels = fileUtil.getOrderFromFile("sell"+symbol)

    for tradeModel in tradeModels:

        price = float(tradeModel.price)

        if price >= close:#比卖过的还低  不能卖
            return False

        gap = close - price
        times = gap/price

        if times < 0.015:
            return False

    return True

def getBuyModel(symbol,close,env):
    sellPackage = fileUtil.getOrderFromFile("sell"+symbol)

    listPrice = []

    for tradeModel in sellPackage:

        state = getOrderStatus(env, tradeModel.orderId)  # 先判断订单的状态

        if state != 'filled':
            continue

        price = tradeModel.price;

        gap = float(price) - close
        times = gap / float(price)

        if times >= 0.015:
            tradeModel.buyPrice = price;
            listPrice.append(tradeModel)

    return listPrice


# 获取订单状态
def getOrderStatus(evn, orderId):
    if evn == 'pro':
        if orderId == 0:
            return 'error'
        return myHuo.getOrderStatus(orderId)
    else:
        return 'filled'