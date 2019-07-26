import modelUtil as modelUtil
import klineUtil as klineUtil
import KDJUtil as kDJUtil
import RSIUtil as rSIUtil
import MAUtil as mAUtil
import AmountUtil as amountUtil
import logUtil

nextBuy = False
lastIdDict = {}
lastDataDict = {}

def juideAllGap(price,symbol,tradeGap):
    buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史 #查询购买历史

    for model in buyPackage:

        buyPrice = float(model.price)

        gap = abs(buyPrice - price)
        times = gap / buyPrice
        if times < float(tradeGap):
            return False

    return True

#判断能不能买
def juideHighest(price,symbol):
    lastPrice = klineUtil.prices.get(symbol, [])

    high = max(lastPrice)
    # 比最大值少两个点还要大就不要买了 风险高
    if price >= high * 0.98:
        return False

    return True

def juideLowest(price,symbol):
    lastPrice = klineUtil.prices.get(symbol, [])

    low = min(lastPrice)

    if price <= low:
        return True

    return False

def canSell(price,symbol,minIncome,env):

    sellPackage = []

    try:
        buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史 #查询购买历史

        for buyModel in buyPackage:

            buyModelPrice = buyModel.price;

            gap = price - float(buyModelPrice)
            gap = gap / float(buyModelPrice)

            if gap >= float(minIncome) and gap >= float(buyModel.minIncome):
                sellPackage.append(buyModel)

    except Exception as err:
        logUtil.info("commonUtil--canSell"+err)

    return sellPackage

def addSymbol(data,transactionModel):
    logUtil.info(data, "new data-----",transactionModel.symbol)

    klineUtil.add(data, transactionModel.symbol)
    kDJUtil.add(data, transactionModel.symbol)
    rSIUtil.add(transactionModel.symbol, 12)
    mAUtil.add(transactionModel.symbol, 10)
    mAUtil.add(transactionModel.symbol, 30)
    mAUtil.add(transactionModel.symbol, 60)
    amountUtil.add(data,transactionModel.symbol)

def delSymbol(transactionModel):
    klineUtil.delSymbol(transactionModel.symbol)
    kDJUtil.delSymbol(transactionModel.symbol)
    rSIUtil.delSymbol(transactionModel.symbol, 12)
    mAUtil.delSymbol(transactionModel.symbol, 10)
    mAUtil.delSymbol(transactionModel.symbol, 30)
    mAUtil.delSymbol(transactionModel.symbol, 60)
    amountUtil.delSymbol(transactionModel.symbol)
    lastDataDict[transactionModel.symbol] = []
    lastIdDict[transactionModel.symbol] = 0

#判断是否最大
def isHighest(price,symbol):
    lastPrice = klineUtil.prices.get(symbol, [])

    if len(lastPrice) < 360:
        return False

    high = max(lastPrice[-360:])
    if price >= high :
        return True

    return False

#找到已购买的最大的那个去卖  至少堆积了5个，并且最大的那个与现在相差10%
def findHighToSell(price,symbol):
    try:
        buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史 #查询购买历史

        buyList = []
        for model in buyPackage:
            if float(model.minIncome) != 1:
                buyList.append(model)

        if len(buyList) < 5:
            return None

        buyList.sort(key=lambda buyModel:float(buyModel.price), reverse=True)
        buyModel = buyList[0]

        buyModelPrice = buyModel.price;

        gap = float(buyModelPrice) - price
        gap = gap / float(buyModelPrice)

        if gap >= 0.1:
            return buyModel

    except Exception as err:
        logUtil.info("commonUtil--findHighToSell" + err)

    return None

def canUrgentBuy(price,symbol,env):
    canBuyPackage = []

    try:
        sellPackage = modelUtil.getUrgentSellModel(symbol)  # 查询卖出历史

        for sellModel in sellPackage:

            sellModelPrice = sellModel.sellPrice;

            gap = float(sellModelPrice) - price
            gap = gap / float(sellModelPrice)

            if gap >= float(sellModel.minIncome):
                canBuyPackage.append(sellModel)

    except Exception as err:
        logUtil.info("commonUtil--canUrgentBuy" + err)

    return canBuyPackage

if __name__ == '__main__':
    print(canUrgentBuy(0.87,"htusdt","dev"))