import Point as point

lastK = [50]
lastD = [50]
lastJ = [50]

def calKDJ(data,index):
    global lastK
    global lastD
    global lastJ

    Cn = data['close']
    Ln = data['low']
    Hn = data['high']

    if Ln == Hn:
        lastK.append(lastK[-1])
        lastD.append(lastD[-1])
        lastJ.append(lastJ[-1])
        return

    RSV = (Cn - Ln) / (Hn - Ln) * 100
    K = 2.0 / 3 * lastK[-1] + 1.0 / 3 * RSV
    D = 2.0 / 3 * lastD[-1] + 1.0 / 3 * K
    J = 3 * K - 2 * D

    lastK.append(K)
    lastD.append(D)
    lastJ.append(J)

    if len(lastK)>10:
        lastK = lastK[1:]
        lastD = lastD[1:]
        lastJ = lastJ[1:]

def getLastK():
    global lastK
    return lastK[-1]

def getLastD():
    global lastD
    return lastD[-1]

def getLastJ():
    global lastJ
    return lastJ[-1]

def judgeSell(index):
    global lastK
    global lastD
    global lastJ

    #当前的K值
    ck = lastK[-1]
    cd = lastD[-1]
    cj = lastJ[-1]

    #上一个的K值
    lk = lastK[-2]
    ld = lastD[-2]
    lj = lastJ[-2]

    if cd > ck and ld < lk :#下穿
        p1 = point.Point(1, lk)
        p2 = point.Point(2, ck)
        line1 = point.Line(p1, p2)

        p3 = point.Point(1, ld)
        p4 = point.Point(2, cd)
        line2 = point.Line(p3, p4)

        pointXY = point.GetCrossPoint(line1, line2)
        if pointXY.y > 70:
            return True

    # if ck > 80 and cd >70:
    #     return True

    # if len(lastJ)>3 and cj > 100 and lj >100 and lastJ[-3]>100:
    #     return True

    return False