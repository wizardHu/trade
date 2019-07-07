from KDJModel import KDJModel
import Point as point

kdjDict={}

def add(data,symbol):
    global kdjDict

    Cn = data['close']
    Ln = data['low']
    Hn = data['high']

    KDJModelList = kdjDict.get(symbol,[KDJModel(50,50,50)])
    lastModel = KDJModelList[-1]

    if Ln == Hn:
        kDJModel = KDJModel(lastModel.K,lastModel.D,lastModel.J)
        KDJModelList.append(kDJModel)

        kdjDict[symbol] = KDJModelList
        return

    RSV = (Cn - Ln) / (Hn - Ln) * 100
    K = 2.0 / 3 * lastModel.K + 1.0 / 3 * RSV
    D = 2.0 / 3 * lastModel.D + 1.0 / 3 * K
    J = 3 * K - 2 * D

    kDJModel = KDJModel(K,D,J)
    KDJModelList.append(kDJModel)

    if len(KDJModelList)>10:
        KDJModelList = KDJModelList[1:]

    kdjDict[symbol] = KDJModelList

def judgeSell(symbol):
    global kdjDict

    KDJModelList = kdjDict.get(symbol, [KDJModel(50, 50, 50)])
    if len(KDJModelList) < 2:
        return False

    thisModel = KDJModelList[-1]
    lastModel = KDJModelList[-2]

    K = thisModel.K
    D = thisModel.D
    J = thisModel.J

    lastK = lastModel.K
    lastD = lastModel.D
    lastJ = lastModel.J

    if (D < K and lastK < lastD or J > 100):
        return True

    if J < lastJ and J > 50 and J > K:
        return True

    return False

def judgeBuy(symbol):
    global kdjDict

    KDJModelList = kdjDict.get(symbol, [KDJModel(50, 50, 50)])

    if len(KDJModelList) < 3:
        return False

    thisModel = KDJModelList[-1]
    lastModel = KDJModelList[-2]

    K = thisModel.K
    D = thisModel.D
    J = thisModel.J

    lastK = lastModel.K
    lastD = lastModel.D
    lastJ = lastModel.J
    isBuy = False

    if K < D and lastK > lastD and D - K > 1 and lastK - lastD > 1:  # 普通下穿
        p1 = point.Point(1, lastK)
        p2 = point.Point(2, K)
        line1 = point.Line(p1, p2)

        p3 = point.Point(1, lastD)
        p4 = point.Point(2, D)
        line2 = point.Line(p3, p4)

        pointXY = point.GetCrossPoint(line1, line2)
        if pointXY.y < 60:
            isBuy = True

    if KDJModelList[-3].J < 0 and lastJ < 0 and J < 0:
            isBuy = True

    if K>55 and D>55 or abs(J-lastJ)<30:
        isBuy = False

    return isBuy
