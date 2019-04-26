# -*- coding: utf-8 -*-
import numpy as np

if __name__ == '__main__':
    a = [1,2,3,4,5]
    b = a[-1*3:]
    print(b)
    print(np.nanmean(b))