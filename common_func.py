#-*- coding:utf-8 -*-
'''
functional: the common function
env: py3
time: 2018-09-26
'''

import json
import urllib
import urllib.request
import cv2
from base64 import b64encode
import numpy as np

import pymysql

def send_post(request_url, request_params={}):
    if request_url:
        request_url = request_url.strip()
        if request_url:
            headers = {'Content-Type': 'application/json'}
            data = json.dumps(request_params)
            data = bytes(data,'utf8')
            request = urllib.request.Request(url=request_url, headers =headers,data=data)
            try:
                response_data = urllib.request.urlopen(request)
                #return response_data.read()
            except Exception as e:
                print ('the response data Error:', e)
                #return None
        else:
            print ('request url is null. The error is from common_func.py')
            #return None
    else:
        print ('request url is None. The error send by common_func.py')
        #return None


def image_byte_str_to_array(byte_array):
    nparr = np.fromstring(byte_array,np.uint8)
    return cv2.imdecode(nparr,cv2.IMREAD_COLOR)

def image_array_to_byte_str(image_matrix, quality=100, r=None):
    if r:
        image_matrix = cv2.resize(image_matrix, (int(r * image_matrix.shape[1]), int(r * image_matrix.shape[0])))
    return cv2.imencode('.jpg', image_matrix, [cv2.IMWRITE_JPEG_QUALITY, quality])[1].tostring()

def image_to_base64(img_ndarray, encoding='utf-8', quality=100, ratio=1.0):
    try:
        img_bytes = image_array_to_byte_str(img_ndarray, quality=quality, r=ratio)
        base64_bytes = b64encode(img_bytes)
        base64_str = base64_bytes.decode(encoding)
        return base64_str
    except Exception as e:
        print('image_to_base64 error', e)
        return None

def mysql_connect(host,port,user,passwd,dbname):
    _conn_status = True
    _max_retries_count = 10
    _conn_retries_count = 0
    _conn_timeout = 3 # 3 secondes, the default is 10 secondes
    while _conn_status and _conn_retries_count <= _max_retries_count:
        try:
            print('MySQL is connecting...')
            conn = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=dbname,charset='utf8')
            _conn_status = False
            return conn
        except:
            _conn_retries_count += 1
            print('MySQL retry connect counts:',_conn_retries_count)
    print('connect MySQL error')
