import modelUtil as modelUtil
import klineUtil as klineUtil

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

    if len(lastPrice) < 800:
        return False

    high = max(lastPrice)
    # 比最大值少两个点还要大就不要买了 风险高
    if price >= high * 0.98:
        return False

    return True

if __name__ == '__main__':
    print(juideHighest(7,"eosusdt"))