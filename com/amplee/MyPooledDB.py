# -*- coding: UTF-8 -*-

import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor
import DBConfig
import logUtil

# 连接池对象
__pool = None

def getConn():
    global  __pool
    """
    @summary: 静态方法，从连接池中取出连接
    @return MySQLdb.connection
    """
    if __pool is None:
        logUtil.error("is None")
        __pool = PooledDB(creator=pymysql, mincached=5, maxcached=20,
                          host=DBConfig.DBHOST, port=DBConfig.DBPORT, user=DBConfig.DBUSER, passwd=DBConfig.DBPWD,
                          db=DBConfig.DBNAME, use_unicode=True, charset=DBConfig.DBCHAR, cursorclass=DictCursor)
    return __pool.connection()