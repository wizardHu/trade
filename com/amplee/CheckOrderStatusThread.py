# -*- coding: utf-8 -*-
from threading import Thread
import fileOperUtil as fileOperUtil
import logUtil
import Refresh as refresh
import HuobiService as huobi
import time
import modelUtil as modelUtil
from BuyModel import BuyModel


class CheckOrderStatusThread(Thread):
    env = "dev"

    def __init__(self,env, name="checkOrderStatusThread"):
        super().__init__()
        self.name = name
        self.env = env


    def chechOrder(self,orderId):
        try:
            if "pro" == self.env:

                result = huobi.order_info(orderId)
                data = result['data']
                state = data['state']
                logUtil.info("chechOrder", result)
                if state == 'filled':
                    return True
            else:
                return True

        except Exception as err:
            logUtil.error('chechOrder error', err)

        return False

    def run(self):

        while True:
            try:
                transactionModels = refresh.getAllPairAndRefresh()

                self.doCheck(transactionModels)

            except Exception as err:
                logUtil.error('checkOrderStatusThread error', err.__traceback__)

            time.sleep(5)

    def doCheck(self, transactionModels):
        for transactionModel in transactionModels:
            symbol = transactionModel.symbol
            sellOrderModels = modelUtil.getSellOrderModels(symbol,self.env)

            if len(sellOrderModels) > 0:
                for sellOrderModel in sellOrderModels:
                    orderStatus = self.chechOrder(sellOrderModel.sellOrderId)
                    logUtil.info("orderId=", sellOrderModel.sellOrderId, " status=", orderStatus)
                    if orderStatus:
                        buyModel = modelUtil.getBuyModelByOrderId(sellOrderModel.buyOrderId)
                        modelUtil.delBuyModel(buyModel.id)
                        modelUtil.delSellOrderById(sellOrderModel.id)

                        modelUtil.insertBuySellReocrd(buyModel.symbol, 0,  sellOrderModel.buyPrice, sellOrderModel.sellPrice,
                                                      sellOrderModel.buyOrderId, sellOrderModel.sellOrderId,
                                                      sellOrderModel.amount, int(time.time()))
                        continue

                    # 测试环境不会走到这里，因为测试环境能直接卖成功
                    kline = huobi.get_kline(symbol, transactionModel.period, 1)
                    if kline['status'] == 'ok' and kline['data'] and len(kline['data']) >= 1:
                        kline['data'].reverse()
                        price = float(kline['data'][0]['close'])
                        buyPrice = float(sellOrderModel.buyPrice)
                        if buyPrice > price:  # 当前价格比买入的时候低才需要判断要不要撤单
                            gap = (buyPrice - price) / buyPrice
                            if gap > 0.05:  # 比买入的时候还要低5%就撤单
                                #{'status': 'ok', 'data': '82495000363'}
                                result = huobi.cancel_order(sellOrderModel.sellOrderId)
                                if result['status'] == 'ok':
                                    modelUtil.delSellOrderById(sellOrderModel.id)
                                    buyModel = modelUtil.getBuyModelByOrderId(sellOrderModel.buyOrderId)
                                    buyModel.status = 0
                                    modelUtil.modBuyModel(buyModel)
