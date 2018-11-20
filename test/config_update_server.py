#-*- coding:utf-8 -*-
import flask
from flask import Flask, Response
import json

success_response = {"status":"success"}
error_response = {"status":"error","data":{"error_code":403,"error_message":"传入参数不正确"}}

print("init config flask...")
app = Flask(__name__)

@app.route('/dlconfigupdate',methods=['POST'])
def update_request():
    params_json = flask.request.get_data()
    if isinstance(params_json,bytes):
        params_json = params_json.decode('utf-8')
    params_json_dict = json.loads(params_json)
    if params_json_dict['camera_ids']:
        response = json.dumps(success_response)
        print("success response:",response,type(response))
        return response
    else:
        response = json.dumps(error_response)
        print("error response:",response,type(response))
        return response
    
        

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8084',threaded=True)
