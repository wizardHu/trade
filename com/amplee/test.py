from UrgentSellModel import  UrgentSellModel
from BuyModel import BuyModel

if __name__ == '__main__':
    buyModel = BuyModel(4.6258,1563877860,0.65,41867946880,0.015)
    urgentSellModel = UrgentSellModel(buyModel,1563877960,41867946980,3.6258)
    print(urgentSellModel)
