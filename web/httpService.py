# encoding=utf-8
from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
import hashlib
import json
import time
import os
import sys

app = Flask(__name__)


# 返回对象
def result(queryID, question, sqlRespond):
    resultDic = {}
    resultDic['queryID'] = queryID
    resultDic['question'] = question
    resultDic['queryResult'] = sqlRespond
    resultDic['timestamp'] = "xxx"
    resultDic['history'] = "xxx"
    return resultDic

def __make_random_id__():
    src = 'filed_46546546464631361sdfsdfgsdgfsdgdsgfsd' + str(time.time())
    m1 = hashlib.md5()
    m1.update(src.encode())
    return m1.hexdigest()


@app.route('/nl2sql/', methods=['post','get'])
def post_http():
    if not request.data:  # 检测是否有数据
        return ('fail')
    params = request.data.decode('utf-8')
    # 获取到POST过来的数据，因为我这里传过来的数据需要转换一下编码。根据晶具体情况而定
    print("recive:", params)
    query = json.loads(params)
    question = query['question']
    queryID = query['queryID']
    sqlRespond="SELECT DISTINCT class_group FROM tp_mis.change_driver_basic_info "
    respond = result(queryID,question, sqlRespond)
    
    time.sleep(10)
    print("respond: ", respond)
    # 把区获取到的数据转为JSON格式。
    return jsonify(respond)


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=8000, threaded=True)
    WSGIServer(('0.0.0.0', 6006), app).serve_forever()
