
def cal(fileName):

    cost = 0

    f = open(fileName, encoding='utf-8')
    for line in f.readlines():
        if line != '\n' and line != '':
            params = line.split(' ')
            price = float(params[7])
            cost = cost + price

    print(cost)

    f.close()

if __name__ == '__main__':
    cal("btmusdt")