import modelUtil as modelUtil
import klineUtil as klineUtil

nextBuy = False

def juideAllGap(price,symbol,tradeGap):
    buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史 #查询购买历史

    for model in buyPackage:

        buyPrice = float(model.price)

        gap = abs(buyPrice - price)
        times = gap / buyPrice
        if times < float(tradeGap):
            return False

    return True

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
        print(price)
        return True

    return False

def canSell(price,symbol,minIncome,env):

    sellPackage = []

    try:
        buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史 #查询购买历史

        for buyModel in buyPackage:
            state = 'filled'

            if "pro" == env:
                print(state)

            if state == 'filled':
                buyModelPrice = buyModel.price;

                gap = price - float(buyModelPrice)
                gap = gap / float(buyModelPrice)

                if gap >= float(minIncome):
                    sellPackage.append(buyModel)

    except Exception as err:
        print("commonUtil--canSell"+err)

    return sellPackage

if __name__ == '__main__':
    print(juideHighest(7,"eosusdt"))