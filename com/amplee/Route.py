# -*- coding: utf-8 -*-

from bottle import route
import TickUtil as tickUtil


@route('/getAmount/:symbol')
def start(symbol):
    return str(tickUtil.tickDict[symbol])