import modelUtil as modelUtil

def juideAllGap(price,symbol):
    buyPackage = modelUtil.getBuyModel(symbol)  # 查询购买历史 #查询购买历史

    for model in buyPackage:

        buyPrice = float(model.price)

        gap = abs(buyPrice - price)
        times = gap / buyPrice
        if times < 0.015:
            return False

    return True

print(juideAllGap(7,"eosusdt"))