
def cal(fileName):

    amount = 0;
    cost = 0

    f = open(fileName, encoding='utf-8')
    for line in f.readlines():
        if line != '\n' and line != '':
            params = line.split(' ')
            flag = params[0]
            if "1" == flag:
                buyAmount = float(params[2])
                buyPrice = float(params[1])
                amount = amount + buyAmount
                cost = cost - buyPrice*buyAmount
            else:
                sellAmount = float(params[2])
                sellPrice = float(params[3])
                amount = amount - sellAmount
                cost = cost + sellPrice*sellAmount

    print(cost,amount)

    f.close()

if __name__ == '__main__':
    cal("tradeRecord")