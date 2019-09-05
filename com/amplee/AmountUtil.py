import klineUtil as klineUtil
import numpy as np

uplowDict = {}

def add(data,symbol):
    global uplowDict

    uplow = uplowDict.get(symbol,[])

    close = data['close']
    open = data['open']
    up = 1

    if close <= open:
        up = 0

    uplow.append(up)

    if len(uplow) > 50:
        uplow = uplow[1:]

    uplowDict[symbol] = uplow

def delSymbol(symbol):
    global uplowDict
    uplowDict[symbol] = []


def isHighPer(per, exchangeamount,symbol):
    amount = klineUtil.amounts.get(symbol, [])[-101:]
    amount = amount[0:len(amount) - 1]  # 排除自己

    amount.sort()

    count = len(amount) - (len(amount) * per / 100)

    amount = amount[int((-1 * count)):]

    if exchangeamount < (amount[0] * 0.9):
        return False

    return True

def judgeRisk(symbol):
    prices = klineUtil.prices.get(symbol, [])
    amounts = klineUtil.amounts.get(symbol, [])

    global uplowDict

    uplow = uplowDict.get(symbol, [])

    risk = 0

    amount10 = amounts[-13:len(amounts)]  # 取最后13
    prices10 = prices[-11:len(prices)]
    uplow10 = uplow[-11:len(uplow)]

    if len(amount10) == 13:
        for index in range(len(prices10)):
            amount = amount10[index + 2]  # 与 index位置的price 对应的成交额度

            if risk == 0 and isHighPer(85, amount,symbol):  # 这个成交量大于最近100期的85% 需要进行成交额判断
                last2 = amount10[index]
                last1 = amount10[index + 1]

                if last2 == 0:
                    last2 = 1

                if last1 == 0:
                    last1 = 1

                if amount / last1 >= 4 or amount / last2 >= 5:  # 成交量异常 需要进行风险判断
                    risk += 2
                    continue

            if risk != 0:
                if uplow10[index] == 1:
                    risk -= 1
                else:
                    risk += 1
                    if risk > 5:
                        risk = 0

    else:
        return False

    if risk == 0 or risk > 5:
        return True

    return False

def judgeUrgentSell(symbol):
    amounts = klineUtil.amounts.get(symbol, [])
    if len(amounts) < 5:
        return False

    list = [amounts[-1], amounts[-2], amounts[-3], amounts[-4],
            amounts[-5]]

    mean = np.mean(list)
    std = np.std(list)

    if std > mean:
        return True

    return False