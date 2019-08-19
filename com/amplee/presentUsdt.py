import HuobiService as huobi

def getBalance():
    result = huobi.get_balance(huobi.ACCOUNT_ID)
    data = result['data']
    list = data['list']
    for account in list:
        if account['currency'] == 'usdt' and account['type'] == 'trade':
            return account['balance']


if __name__ == '__main__':
    print(getBalance())

