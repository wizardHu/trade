class TranPairs:
    symbols1 = ''
    symbols2 = ''
    pvalue = 0
    corr = 0

    def __init__(self, symbols1, symbols2,pvalue,corr):
        self.symbols1 = symbols1
        self.symbols2 = symbols2
        self.pvalue = pvalue
        self.corr = corr

    def getValue(self):
        return "{},{},{},{}".format(self.symbols1,self.symbols2,self.pvalue,self.corr)