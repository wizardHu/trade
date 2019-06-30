# -*- coding: utf-8 -*-
class KDJModel:
    K = 0.0

    D = 0.0

    J = 0.0

    def __init__(self,K,D,J):
        self.K = K
        self.D = D
        self.J = J

    def __str__(self):
        return "{},{},{}".format(self.K,self.D,self.J)

    def __repr__(self):
        return "{},{},{}".format(self.K, self.D, self.J)