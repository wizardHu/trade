from TranPairs import TranPairs

def readAll(fileName):
    tranPairs = []
    f = open(fileName, encoding='utf-8')
    count = 0
    for line in f.readlines():
        if line != '\n' and line != '':
            params = line.replace('\n', '').split(',')
            first = params[0]
            second = params[1]
            pvalue = params[2]
            corr = params[3]
            tranPair = TranPairs(first, second, pvalue, corr)
            tranPairs.append(tranPair)

            count = count +1
            if count == 1000:
                break
    f.close()
    return tranPairs


if __name__ == '__main__':
    tranPairs0410 = readAll('0410.txt');
    tranPairs0411 = readAll('0411.txt');

    for tranPair0410 in tranPairs0410:
        for tranPair0411 in tranPairs0411:
            if tranPair0410.symbols1 == tranPair0411.symbols1 and tranPair0410.symbols2 == tranPair0411.symbols2:
                print(tranPair0410.getValue(),tranPair0411.getValue())

            if tranPair0410.symbols1 == tranPair0411.symbols2 and tranPair0410.symbols2 == tranPair0411.symbols1:
                print(tranPair0410.getValue(),tranPair0411.getValue())
