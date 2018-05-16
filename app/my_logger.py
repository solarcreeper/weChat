#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
from time import strftime
import logging

def init_logger(level, log_name=None):
    FLASK_LOG_DIR = os.path.join(os.path.abspath('.'), 'log', 'log_{}'.format(strftime('%Y%m%d')))

    if not os.path.exists(os.path.dirname(FLASK_LOG_DIR)):
        os.makedirs(os.path.dirname(FLASK_LOG_DIR))

    logger = logging.getLogger(log_name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(FLASK_LOG_DIR, encoding='utf-8')
    formatter = logging.Formatter('[%(asctime)s %(filename)s:%(lineno)s] - %(message)s')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger

logger = init_logger(logging.DEBUG, log_name="flask")
