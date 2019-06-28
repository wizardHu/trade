import HuobiService as huobi

if __name__ == '__main__':
    # A EOS B HT C USDT
    firstLine = huobi.get_kline('htusdt', '1min', 2000)
    secondLine = huobi.get_kline('eosusdt', '1min', 2000)
    threeLine = huobi.get_kline('eosht', '1min', 2000)

    firstData = firstLine['data']
    secondData = secondLine['data']
    threeData = threeLine['data']

    firstData.reverse()
    secondData.reverse()
    threeData.reverse()

    usdt = 0
    ht = 5
    eos = 5
    balance = 0
    buyAmount = 50
    fei = 0

    for i in range(0,2000):
        p1 = float(firstData[i]['close'])
        p2 = float(secondData[i]['close'])
        p3 = float(threeData[i]['close'])

        if ( p2/p1 - p3) > (p3*0.003):

            eos += buyAmount # 买入 EOS
            buyC3Cost = buyAmount*p3 # 消耗了 buyC3Cost 个 HT
            ht -= buyC3Cost

            fei += buyAmount*p2*0.002

            eos -= buyAmount # 卖出 EOS
            sellC2Cost = buyAmount*p2 # 获得了 sellC2Cost 个 USDT

            fei += buyAmount * p2 * 0.002

            ht += buyC3Cost # 买入 HT
            buyC1Cost = buyC3Cost*p1 # 消耗了 buyC1Cost 个 USDT

            fei += buyC1Cost * 0.002

            usdt += (sellC2Cost-buyC1Cost)

            print(i,p1, p2, p3, p2 / p1,sellC2Cost-buyC1Cost)

    print(ht,eos,usdt,fei)