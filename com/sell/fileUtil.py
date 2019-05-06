from TradeModel import TradeModel

# 从文件中读取卖出记录
def getOrderFromFile(fileName):
    sellPackage = []
    sells = readAll(fileName)

    for order in sells:

        if order != '' and order != '\n':
            params = order.split(',')
            price = params[0]
            amount = params[1]
            orderId = params[2]
            index = params[3]
            symbol = params[4]

            tradeModel = TradeModel(price, index, amount, orderId, symbol)
            sellPackage.append(tradeModel)

    return sellPackage

def write(msg,fileName):
    f = open(fileName, 'a', encoding='utf-8')
    f.write("{0}\n".format(msg))
    f.flush()
    f.close()


def delAll(fileName):
    f = open(fileName, 'w', encoding='utf-8')
    f.close()

def readAll(fileName):
    lines = []
    f = open(fileName, encoding='utf-8')
    for line in f.readlines():
        if line != '\n' and line != '':
            lines.append(line.replace('\n', ''))

    f.close()
    return lines

def delMsgFromFile(msg,fileName):
    msg = "{0}\n".format(msg)
    lines = []
    f = open('buy', encoding='utf-8')
    for line in f:
        if line != msg:
            lines.append(line.replace('\n', ''))

    delAll(fileName)
    f.close()

    for line in lines:
        write(line)