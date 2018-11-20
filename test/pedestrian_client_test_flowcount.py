#-*- coding:utf-8 -*-
'''
functional: a test client for the flow count alarm http request with Face++
env: py3
time： 2018-09-25
'''


import json
import urllib
from urllib import request
import time

def send_post(request_url, request_params={}):
    if request_url:
        request_url = request_url.strip()
        if request_url:
            headers = {'Content-Type': 'multipart/form-data'}
            data = bytes(json.dumps(request_params),'utf8')
            request = urllib.request.Request(url=request_url, headers =headers,data=data)
            try:
                response_data = urllib.request.urlopen(request)
                response_data_str = response_data.read()
                if isinstance(response_data_str,bytes):
                    print('step in isinstance',type(response_data_str))
                    response_data_str = response_data_str.decode('utf-8')
                response_data_dict = json.loads(response_data_str)
                if response_data_dict['status'] == 'success':
                    success_data = response_data_str
                    return success_data
                elif response_data_dict['status'] == 'error':
                    error_data = response_data_str
                    return error_data
                else:
                    return "something error in response data"
            except Exception as e:
                print('Request Error:', e)
                return None
        else:
            print('request url bad')
            return None
    print('request url error')
    return None


if __name__ == '__main__':
    real_url = "http://127.0.0.1:8083/pedestrian_identification"
    time_format = "%Y-%m-%d %H:%M:%S"
    while True:
        #data = {} # a error test
        _alarm_time = time.strftime(time_format,time.localtime(time.time()))
        data = {
            "camera_id":"9",
            "camera_ip":"10.90.129.102",
            "start_time":"2018-09-25 12:20:01",
            "alarm_time":_alarm_time,
            "alarm_pic":"/home/q/Interface/imgs/test.png",
            "counts": "2",
            "ped_info":[
                {
                    "ped_ID":"1",
                    "ped_bbox":"10,20,100,300",
                    "ped_dress":"黄色上衣，黑色裤子"
                },
                {
                    "ped_ID": "2",
                    "ped_bbox": "10,20,100,400",
                    "ped_dress": "绿色上衣，黑色裤子"
                }
            ]
        }
        print(send_post(real_url, data))
        time.sleep(10)
