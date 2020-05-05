import logging.config

LOG_LEVEL = logging.INFO

LOGGER = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s Line:%(lineno)s==>%(message)s'
        },'kline': {
            'class': 'logging.Formatter',
            'format': '%(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file1': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'mode': 'w',
            'formatter': 'default',
            'filename': 'my.log',
            'encoding': 'utf-8'
        },
        'file2': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'mode': 'a',
            'formatter': 'kline',
            'filename': 'kline.log',
            'encoding': 'utf-8'
        },'file3': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'mode': 'w',
            'formatter': 'default',
            'filename': 'error.log',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '__main__': {
            'handlers': ['file1', 'file2', 'console'],
            'level': LOG_LEVEL,
        },'default': {
            'handlers': ['file1'],
            'level': LOG_LEVEL,
        },'kline': {
            'handlers': ['file2'],
            'level': LOG_LEVEL,
        },'error': {
            'handlers': ['file3'],
            'level': LOG_LEVEL,
        }
    }
}

logging.config.dictConfig(LOGGER)

def info(*msg):
    # logger = logging.getLogger("default")
    # logger.info(msg)
    print(msg)
    # pass

def kLineData(*msg):
    # logger = logging.getLogger("kline")
    # logger.info(msg)
    # print(msg)
    pass

def error(*msg):
    logger = logging.getLogger("error")
    logger.info(msg)