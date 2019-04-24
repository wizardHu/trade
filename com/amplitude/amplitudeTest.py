import numpy as np

if __name__ == '__main__':
    list = [1,1,1.1]
    print(np.mean(list))
    print(np.mean(np.std(list, ddof=1)))