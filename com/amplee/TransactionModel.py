# -*- coding: utf-8 -*-
class TransactionModel:
    id = 0
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

    #止损点
    stopLoss = 0.05

    # 价格小数点精度
    pricePrecision = 2

    def __init__(self,id,symbol,everyExpense,tradeGap,minIncome,period,precision,stopLoss,pricePrecision):
        self.id = id
        self.symbol = symbol
        self.everyExpense = everyExpense
        self.tradeGap = tradeGap
        self.tradeGap = tradeGap
        self.minIncome = minIncome
        self.period = period
        self.precision = precision
        self.stopLoss = stopLoss
        self.pricePrecision = pricePrecision


    def __str__(self):
        return "{},{},{},{},{},{}".format(self.id,self.symbol,self.everyExpense,self.tradeGap,self.minIncome,self.period)

    def __repr__(self):
        return "{},{},{},{},{},{}".format(self.id,self.symbol,self.everyExpense,self.tradeGap,self.minIncome,self.period)

    def printTransaction(self):
        print('symbol={} everyExpense={} tradeGap={} minIncome={} period={}'.format(self.symbol,self.everyExpense,self.tradeGap,self.minIncome,self.period))
