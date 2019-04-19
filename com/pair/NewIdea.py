# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from statsmodels.tsa.stattools import coint
np.random.seed(107)

import matplotlib.pyplot as plt
Xreturns = np.random.normal(0, 1, 100)
# sum them and shift all the prices up
X = pd.Series([1,2,3,4], name='X') + 50

noise = np.random.normal(0, 1, 100)
Y = X + 5
Y.name = 'Y'
# pd.concat([X, Y], axis=1).plot(figsize=(15,7))

# (Y/X).plot(figsize=(15,7))
# plt.axhline((Y/X).mean(), color='red', linestyle='--')
# plt.xlabel('Time')
# plt.legend(['Price Ratio', 'Mean'])

score, pvalue, _ = coint(X,Y)#pvalue 就是协整值  越小越好  值低于 0.05 时，协整关系便非常强
print(pvalue,X.corr(Y)) #X.corr(Y) 是相关性 [-1,1]越大越好 0.7以上就行

plt.show()