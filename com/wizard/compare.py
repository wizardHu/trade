import Client as client
import ssl
ssl.match_hostname = lambda cert, hostname: True


btc = client.getKline(1200,"btc_usdt")

eos = client.getKline(1200,"eos_usdt")

count = 0

for i in btc['data']:
    index = btc['data'].index(i)
    
    if index > 1:
        eosOpen = eos['data'][index-1]["open"]
        eosClose = eos['data'][index-1]["close"]
        
        btcOpen = i["open"]
        btcClose = i["close"]
        
        if eosOpen> eosClose and btcOpen >btcClose:
            count += 1
            gap = eosOpen - eosClose
            mul = gap/eos['data'][index-2]["close"]
            if mul > 0.007:
                print(eosOpen,eosClose,eos['data'][index-2]["close"])
                count += 1
        
        if eosOpen< eosClose and btcOpen <btcClose:
            count += 1
            gap = eosClose - eosOpen
            mul = gap/eos['data'][index-2]["close"]
            if mul > 0.007:
                print(eosOpen,eosClose,eos['data'][index-2]["close"])
                count += 1
        

print(count)
        
        
        
        
        
        
        
        
        
        
