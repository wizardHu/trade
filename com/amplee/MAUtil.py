import klineUtil as klineUtil

#{'eosusdt10':[1,2,3,4],'eosusdt20':[1,3,4,5],'xrpusdt20':[1,3,4,5],'xrpusdt30':[1,3,4,5]}
maDice={}

def getThisMa(symbol,pre):
    maList = maDice.get(symbol + str(pre), [0])
    return maList[-1:]

def maJudgeBuy(data, symbol):
    Cn = data['close']

    ma10 = getThisMa(10)
    ma30 = getThisMa(30)
    ma60 = getThisMa(60)

    # print ("index=",index," ma10=",ma10," ma30=",ma30," ma60=",ma60)

    if ma30 <= ma10 or ma30 == 0 or ma10 == 0:
        return False

    if Cn >= ma10 or Cn >= ma30 or Cn >= ma60:
        return False

    return True

def add(symbol,pre):
    global maDice
    lastPrice = klineUtil.prices.get(symbol, [])
    maList = maDice.get(symbol + str(pre), [])

    count = 0.0

    if len(lastPrice) >= pre:
        lists = lastPrice[(-1 * pre):]
        for p in lists:
            count += p

    maList.append(round(count/pre,3))
    if len(maList) > 10:
        maList = maList[1:]

    maDice[symbol + str(pre)]=maList


for i in range(20):
    klineUtil.add({'close': i+1, 'amount': 1}, "eosusdt")

add("eosusdt",2)
print(getThisMa("eosusdt",2))

