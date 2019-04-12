#-*- endcoding:utf-8 -*-
import logging
import os
import time

#获取logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
#获取handler
fh = logging.FileHandler(os.curdir + '/log/' + time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + '.log')
ch = logging.StreamHandler()

#格式
formatter = logging.Formatter("%(asctime)s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


def log(message):
    logger.info(message)
