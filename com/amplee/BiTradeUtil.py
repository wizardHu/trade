from BuyModel import BuyModel
import fileOperUtil as fileOperUtil
import time

def buy(env,buyPrice,amount,symbol,index):
    try:
        orderId = "0000"
        if "pro" == env:
            print("buy")
            orderId = "1111"

        buyModel = BuyModel(buyPrice,index,amount,orderId)
        fileOperUtil.write(buyModel,symbol+"buy")
        fileOperUtil.write(('1,{},{},{},{}').format(buyPrice, amount, index,
                                                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(index))),symbol + "-record")

    except Exception as err:
        print("BiTradeUtil--buy"+err)

def sell(env,sellPrice,sellIndex,buyModel,symbol):
    try:
        if "pro" == env:
            print("sell")

        fileOperUtil.delMsgFromFile(buyModel,symbol+"buy")
        fileOperUtil.write(('0,{},{},{},{},{}').format(buyModel.price, buyModel.amount,sellPrice,sellIndex,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sellIndex))),symbol+"-record")

    except Exception as err:
        print("BiTradeUtil--sell"+err)

