from BuyModel import BuyModel
import fileOperUtil as fileOperUtil

def buy(env,price,amount,symbol,index):

    orderId = "0000"
    if "pro" == env:
        print("buy")
        orderId = "1111"

    buyModel = BuyModel(price,index,amount,orderId)
    fileOperUtil.write(buyModel,symbol+"buy")
