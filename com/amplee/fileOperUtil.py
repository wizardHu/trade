# -*- coding: utf-8 -*-

def readAll(fileName):
    lines = []
    try:
        f = open(fileName, encoding='utf-8')
        for line in f.readlines():
            if line != '\n' and line != '':
                lines.append(line.replace('\n', ''))

        f.close()
    except Exception as err:
        print()
    return lines

def write(msg,fileName):
    f = open(fileName, 'a', encoding='utf-8')
    f.write("{0}\n".format(msg))
    f.flush()
    f.close()

def delAll(fileName):
    f = open(fileName, 'w', encoding='utf-8')
    f.close()

def delMsgFromFile(msg,fileName):
    msg = "{0}\n".format(msg)
    lines = []
    f = open(fileName, encoding='utf-8')
    for line in f:
        if line != msg:
            lines.append(line.replace('\n', ''))

    delAll(fileName)
    f.close()

    for line in lines:
        write(line,fileName)
