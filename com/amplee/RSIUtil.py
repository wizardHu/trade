import klineUtil as klineUtil

rsiDice={}

def rsiJudgeBuy(symbol,pre):
    rsiList = rsiDice.get(symbol + str(pre), [50])

    rsi = rsiList[-1]

    if rsi < 40:
        return True

    return False

def add(symbol,pre):
    global rsiDice
    lastPrice = klineUtil.prices.get(symbol, [])
    rsiList = rsiDice.get(symbol + str(pre), [])

    down = 0.0
    up = 0.0
    rsi = 50

    if len(lastPrice) > pre:
        listPrice = lastPrice[-(pre + 1):]
        for i in range(len(listPrice) - 1):

            if listPrice[i] >= listPrice[i + 1]:  # 前面的比后面的大 跌
                down += (listPrice[i] - listPrice[i + 1])

            if listPrice[i] < listPrice[i + 1]:
                up += (listPrice[i + 1] - listPrice[i])

        avgDown = down / pre
        avgUp = up / pre

        if avgUp != 0 or avgDown != 0:
            rsi = 100 * avgUp / (avgUp + avgDown)

    rsiList.append(rsi)
    if len(rsiList) > 10:
        rsiList = rsiList[1:]

    rsiDice[symbol + str(pre)]=rsiList
