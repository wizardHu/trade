# -*- coding: utf-8 -*-
from threading import Thread
import HuobiService as huobi
import logUtil
import Refresh as refresh
import TickUtil as tickUtil
from bottle import run
import Route

class TradeThread(Thread):
    transactionModel = None

    def __init__(self,transactionModel, name="tradeThread"):
        super().__init__()
        self.name = name
        self.transactionModel = transactionModel

    def run(self):

        while True:
            try:
                result = huobi.get_trade(self.transactionModel.symbol)
                tickUtil.add(result,self.transactionModel.symbol)

            except Exception as err:
                logUtil.info('TradeThread error', err)

if __name__ == '__main__':

    transactionModels = refresh.getAllPairAndRefresh()
    for transactionModel in transactionModels:
        thread01 = TradeThread(transactionModel)
        thread01.start()

    run(host='127.0.0.1', port=8089, debug=False)