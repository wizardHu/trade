import logging

# 1.初始化日志默认配置
logging.basicConfig(filename='./my.log',                                                 # 日志输出文件
                    level=logging.INFO,                                                 # 日志写入级别
                    datefmt='%Y-%m-%d %H:%M:%S',                                         # 时间格式
                    format='%(asctime)s Line:%(lineno)s==>%(message)s')    # 日志写入格式

def info(msg):
    #logging.info(msg)
    print(msg)