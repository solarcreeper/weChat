#!/usr/bin/python
# -*- coding:utf-8 -*-
import os, stat
from time import strftime
import logging
import platform


def init_logger(level, log_name=None):
    if platform.platform().startswith("Windows"):
        FLASK_LOG_DIR = os.path.join(os.path.abspath('.'), 'log')
    else:
        FLASK_LOG_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log')

    if not os.path.exists(FLASK_LOG_DIR):
        os.makedirs(FLASK_LOG_DIR)
    FLASK_LOG_FILE = os.path.join(FLASK_LOG_DIR, 'log_{}.log'.format(strftime('%Y%m%d')))

    open(FLASK_LOG_FILE, 'a').close()
    logger = logging.getLogger(log_name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(FLASK_LOG_FILE, encoding='utf-8')
    formatter = logging.Formatter('[%(asctime)s %(filename)s:%(lineno)s] - %(message)s')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger


logger = init_logger(logging.DEBUG, log_name="flask")
