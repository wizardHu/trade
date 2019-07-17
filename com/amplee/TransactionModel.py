# -*- coding: utf-8 -*-
class TransactionModel:
    #交易对 eosusdt
    symbol = ''

    #每次交易的金额
    everyExpense = 0.0

    #与以往的交易间隔
    tradeGap = 0.0

    #最低收益率
    minIncome = 0.0

    #K线周期
    period = '1min'

    # 小数点精度
    precision = 2

    def __init__(self,symbol,everyExpense,tradeGap,minIncome,period,precision):
        self.symbol = symbol
        self.everyExpense = everyExpense
        self.tradeGap = tradeGap
        self.tradeGap = tradeGap
        self.minIncome = minIncome
        self.period = period
        self.precision = precision


    def __str__(self):
        return "{},{},{},{},{}".format(self.symbol,self.everyExpense,self.tradeGap,self.minIncome,self.period)

    def __repr__(self):
        return "{},{},{},{},{}".format(self.symbol,self.everyExpense,self.tradeGap,self.minIncome,self.period)

    def printTransaction(self):
        print('symbol={} everyExpense={} tradeGap={} minIncome={} period={}'.format(self.symbol,self.everyExpense,self.tradeGap,self.minIncome,self.period))
