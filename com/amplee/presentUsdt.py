import HuobiService as huobi

if __name__ == '__main__':
    result = huobi.get_balance(huobi.ACCOUNT_ID)
    data = result['data']
    list = data['list']
    for account in list:
        if account['currency'] == 'usdt' and account['type'] == 'trade':
            print(account['balance'])

