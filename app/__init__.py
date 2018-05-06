# -*- coding:utf8 -*-
import hashlib
import sys
import time
import xml.etree.ElementTree as ET

from flask import Flask, request, make_response
import logging
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'hello_ian'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    else:
        data = request.data
        if type(data) == bytes:
            data = data.decode('utf-8')
        app.logger.debug(data)
        xml_recived = ET.fromstring(data)

        to_username = xml_recived.find("ToUserName").text
        from_username = xml_recived.find("FromUserName").text
        content = xml_recived.find("Content").text

        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        reply = reply % (from_username, to_username, str(int(time.time())), content)
        response = make_response(reply)
        response.content_type = 'application/xml'
        return response


if __name__ == "__main__":
    app.debug = True
    sys.setdefaultencoding('utf8')
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    file_handler = logging.FileHandler('wechat_log.log')
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.run()
