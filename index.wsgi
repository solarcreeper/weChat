#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/web_root/wechat/")  #你app的目录
from app import app as application
