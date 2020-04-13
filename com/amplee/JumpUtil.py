# -*- coding: utf-8 -*-
import modelUtil as modelUtil
import logUtil
import commonUtil as commonUtil


# 执行操作
from JumpQueueModel import JumpQueueModel
from TransactionModel import TransactionModel


def doOper(price, transactionModel, jumpModel):
    pass


# 交割模块
def doTrade(price, transactionModel):
    try:
        jumpModelList = modelUtil.getJumpModel(transactionModel.symbol)

        if len(jumpModelList) > 0:
            for jumpModel in jumpModelList:
                lowPrice = float(jumpModel.lowPrice)
                highPrice = float(jumpModel.highPrice)
                jumpPrice = float(jumpModel.jumpPrice)
                jumpCount = int(jumpModel.jumpCount)
                type = int(jumpModel.type)

                # 达到需要操作的价格区间
                if (price >= lowPrice and price <= highPrice) or jumpCount >= 10:
                    doOper(price, transactionModel, jumpModel)
                    continue

                highGap = 0.008
                lowGap = 0.005
                # 为单数即为买,到达跳跃点，需要不断下调jumpPrice价格
                if type % 2 == 1 and jumpPrice >= price:
                    length = commonUtil.calDecimal(price)
                    if jumpCount > 2:
                        highGap = 0.015
                        lowGap = 0.01
                    lowPrice = round(price + price * lowGap,length)#重新计算可操作区间
                    highPrice = round(price + price * highGap, length)
                    jumpCount = jumpCount + 1
                    jumpPrice = round(price - price * 0.01, length)#下调jumpPrice价格
                    newJumpModel = JumpQueueModel(jumpModel.type,jumpModel.orderId,lowPrice,highPrice,jumpPrice,jumpCount,jumpModel.time)
                    modelUtil.modJumpModel(jumpModel,newJumpModel,transactionModel.symbol)

                # 为双数即为卖,到达跳跃点，需要不断上调jumpPrice价格
                if type % 2 == 0 and jumpPrice <= price:
                    length = commonUtil.calDecimal(price)
                    if jumpCount > 2:
                        highGap = 0.015
                        lowGap = 0.01
                    lowPrice = round(price - price * highGap,length)#重新计算可操作区间
                    highPrice = round(price - price * lowGap, length)
                    jumpCount = jumpCount + 1
                    jumpPrice = round(price + price * 0.01, length)#上调jumpPrice价格
                    newJumpModel = JumpQueueModel(jumpModel.type,jumpModel.orderId,lowPrice,highPrice,jumpPrice,jumpCount,jumpModel.time)
                    modelUtil.modJumpModel(jumpModel,newJumpModel,transactionModel.symbol)

    except Exception as err:
        logUtil.info("JumpUtil--doTrade" + err)


if __name__ == '__main__':
    tradeModel = TransactionModel("eosusdt", 10, 0.02, 0.03, "1min",2,0.1)
    doTrade(3.1801,tradeModel)
    print(1)
