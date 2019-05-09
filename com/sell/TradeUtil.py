from TradeModel import TradeModel
import fileUtil as fileUtil
import MyHuobiService as myHuo
import time
import HuobiService as huobi

def canSell(symbol,close,bi,env):
    tradeModels = fileUtil.getOrderFromFile("sell"+symbol)

    for tradeModel in tradeModels:

        price = float(tradeModel.price)

        if price >= close:#比卖过的还低  不能卖
            return False

        gap = close - price
        times = gap/price

        if times < 0.015:
            return False

    if 'pro' == env:
        balance = float(getBalance(bi))

        if balance < 50:
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

        if times >= 0.01:
            tradeModel.buyPrice = close;
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


# 买入
def sendBuy(evn, tradeModel):
    orderId = 0

    if evn == 'pro':
        orderId = myHuo.sendOrder(tradeModel.amount, tradeModel.buyPrice, tradeModel.symbol, 'buy-limit')

    fileUtil.delMsgFromFile(tradeModel.getValue(), "sell" + tradeModel.symbol)
    fileUtil.write(('1 {} {} {} {}').format(tradeModel.price, tradeModel.buyPrice, tradeModel.amount,
                                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                   "record" + tradeModel.symbol)


# 挂卖单
def sell(evn, symbols,price):

    orderId = 0
    if evn == 'pro':
        orderId = myHuo.sendOrder(10, price, symbols, 'sell-limit')

    index = int(round(time.time() * 1000))
    tradeModel = TradeModel(price, index, 10, orderId, symbols)
    fileUtil.write(tradeModel.getValue(), "sell" + symbols)
    fileUtil.write(
        ('0 {} {} {}').format(price, 10, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
        "record" + symbols)

def getBalance(bi):
    balance = huobi.get_balance()
    data = balance['data']
    list = data['list']
    for account in list:
        currency = account['currency']
        accountBalance = account['balance']
        type = account['type']
        if currency == bi and type == 'trade':
            return accountBalance

if __name__ == '__main__':
    print(getOrderStatus("pro",12))