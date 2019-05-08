# -*- coding: utf-8 -*-
import numpy as np
import HuobiService as huobi

if __name__ == '__main__':
    balance = huobi.get_balance()
    data = balance['data']
    list = data['list']
    for account in list:
        currency = account['currency']
        accountBalance = account['balance']
        type = account['type']
        if currency == 'eos' and type == 'trade':
            print(account,currency,accountBalance)