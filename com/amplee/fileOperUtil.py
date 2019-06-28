# -*- coding: utf-8 -*-

def readAll(fileName):
    lines = []
    f = open(fileName, encoding='utf-8')
    for line in f.readlines():
        if line != '\n' and line != '':
            lines.append(line.replace('\n', ''))

    f.close()
    return lines
