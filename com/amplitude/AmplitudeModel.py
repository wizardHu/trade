class AmplitudeModel:
    symbols = ''
    amplitude = 0
    std = 0
    cv = 0

    def __init__(self, symbols,amplitude):
        self.symbols = symbols
        self.amplitude = amplitude

    def getValue(self):
        return "{},{},{},{}".format(self.symbols,self.amplitude,self.std,self.cv)

    def __str__(self):
        return "{},{},{},{}".format(self.symbols,self.amplitude,self.std,self.cv)