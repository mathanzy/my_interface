#-*- coding:utf-8 -*-
'''
functional: a test server for the client of http request with Face++
env: py3
time： 2018-9-25
'''

import json
from flask import Flask, request
import os


print ("init flask...")
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/region_crowd', methods=['POST'])
def region_crowd():
    try:
        params_json_str = request.get_data().decode('utf-8')
        params_json = json.loads(params_json_str)
        camera_id_list = params_json['camera_id_list']
        if camera_id_list == "1,2":
            response = {"status":"success",
            "data":[{"ROI":"window1","peoples":"15"},{"ROI":"window2","peoples":"13"}]}
            return json.dumps(response)
        elif camera_id_list == "3,4,5,6":
            response = {"status": "success",
                        "data": [{"ROI": "window3", "peoples": "66"}, {"ROI": "window4", "peoples": "66"},{"ROI": "window5", "peoples": "66"}, {"ROI": "window6", "peoples": "66"}]}
            return json.dumps(response)
        elif camera_id_list == "7,8":
            response = {"status":"success",
                        "data":[{"ROI": "window1", "peoples": "1"}, {"ROI": "window2", "peoples": "2"},
                                {"ROI": "window3", "peoples": "3"}, {"ROI": "window4", "peoples": "4"},
                                {"ROI": "window5", "peoples": "5"}, {"ROI": "window6", "peoples": "6"},
                                {"ROI": "window7", "peoples": "7"}, {"ROI": "window8", "peoples": "8"},
                                {"ROI": "window9", "peoples": "0"}, {"ROI": "window10", "peoples": "0"},
                                {"ROI": "window11", "peoples": "0"}, {"ROI": "window12", "peoples": "0"},
                                {"ROI": "window13", "peoples": "0"}, {"ROI": "window14", "peoples": "0"},
                                {"ROI": "window15", "peoples": "0"}]}
            return json.dumps(response)
        else:
            response = {"status":"error",
            "data":{
            "error_code":403,
            "error_message":"传入参数不正确"}}
            return json.dumps(response)
    except Exception as e:
        response = {"status":"error",
    	"data":{
    	"error_code":403,
    	"error_message":"error request"
    	}}
        return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, threaded=True)
