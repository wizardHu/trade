# -*- coding: utf-8 -*-
from threading import Thread
import HuobiService as huobi
import logUtil
import Refresh as refresh
import TickUtil as tickUtil

class TradeThread(Thread):

    def __init__(self, name="tradeThread"):
        super().__init__()
        self.name = name

    def run(self):
        try:
            transactionModels = refresh.getAllPairAndRefresh()
            while True:
                for transactionModel in transactionModels:
                    result = huobi.get_trade(transactionModel.symbol)
                    tickUtil.add(result,transactionModel.symbol)

        except Exception as err:
            logUtil.info('TradeThread error', err)

if __name__ == '__main__':
    thread_01 = TradeThread()
    thread_01.start()