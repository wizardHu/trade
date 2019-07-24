from UrgentSellModel import  UrgentSellModel
from BuyModel import BuyModel
import BiTradeUtil as biTradeUtil

if __name__ == '__main__':
    buyModel = BuyModel(4.6258,1563877860,0.65,41867946880,0.015)
    biTradeUtil.urgentSell("dev",0.88,12346,buyModel,"htusdt",0.015)