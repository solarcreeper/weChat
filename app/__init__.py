import hashlib

from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'hello_ian'  # your token
        query = request.args  # GET 方法附上的参数
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)


if __name__ == "__main__":
    app.run()
