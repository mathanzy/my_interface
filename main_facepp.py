#-*- coding:utf-8 -*-
'''
functional : the main function of the interface with Face++
env: py3
time: 2018-09-23
'''
from __future__ import unicode_literals
import flask
from flask import Flask, Response
import os
import json
import threading
import urllib
from urllib import request
import time

import pymysql
import cv2

import run_process 
from run_process import Run_Proc
import common_func
import FTP_class
import settings


print ("init flask...")
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

run_proc_ = Run_Proc()

success_response = settings.success_response
error_response = settings.success_response
common_error_response = settings.common_error_response

front_end_alarm_url = settings.front_end_alarm_url
config_update_url = settings.config_update_url
config_url_headers = settings.config_url_headers

endplugging_id_list = settings.endplugging_id_list
crossboundary_id_list = settings.crossboundary_id_list
flowcount_id_list = settings.flowcount_id_list

flow_count_num = 0
flow_count_lock = threading.Lock()

@app.route('/pedestrian_identification', methods=['POST'])
def handle_alarm_request():
    global success_response
    global error_response
    global endplugging_id_list
    global crossboundary_id_list
    try:
        print('step in the handle alarm request')
        params_json_str = flask.request.get_data().decode('utf-8')
        #print('111111',params_json_str)
        params_json = json.loads(params_json_str)
        print('111111',type(params_json))
        start_time = params_json['start_time']
        alarm_time = params_json['alarm_time']
        camera_id = params_json['camera_id']
        camera_ip = params_json['camera_ip']
        img = params_json['alarm_pic']
        alarm_data = params_json['counts']
        ped_info = json.dumps(params_json['ped_info'],ensure_ascii=False)  #ensure_ascii for the encode of chinese, the default is ascii.
        #print("***************ped_info:",params_json['ped_info'],type(params_json['ped_info'])) 
        #ped_info = params_json['ped_info']
        #ped_info = ""
        now_time = time.time()
        if camera_id in endplugging_id_list or camera_id in crossboundary_id_list:
            alarm_thread = threading.Thread(target=alarm_send,args=(alarm_time,camera_id,camera_ip, alarm_data,img,now_time,))
            alarm_thread.start()
        ftp_thread = threading.Thread(target=ftp_send,args=(now_time,camera_id,img))
        ftp_thread.start()
        mysql_thread = threading.Thread(target=mysql_insert,args = (alarm_time,start_time,camera_id,camera_ip,alarm_data,img,ped_info,now_time,))
        mysql_thread.start()
        return json.dumps(success_response)
    except Exception as e:
        print('handle alarm request error',e)
        return json.dumps(error_response)


def alarm_send(alarm_time,camera_id,camera_ip, alarm_data,img,now_time):
    if camera_id in endplugging_id_list:
        alarm_type = "endPlugging"
    else:
        alarm_type = "crossBoundary"
    img_ori = cv2.imread(img)
    img_base64 = common_func.image_to_base64(img_ori,ratio=0.2)
    alarm_info = {'cameraId':camera_id,
                  'cameraIp':camera_ip,
                  'createTime':int(now_time),
                  'type':alarm_type,
                  'desc':[{'position':'一站台2#区域','level':'green','count':alarm_data}],
                  'img':img_base64
    }
    common_func.send_post(front_end_alarm_url,alarm_info)
    print('sending alarm info to front end...')

def ftp_send(now_time,camera_id,img):
    img_base_name = str(camera_id) + str(int(now_time*1000))+".png"
    camera_id = str(camera_id)
    if camera_id in endplugging_id_list:
        alarm_type = "endPlugging"
    elif camera_id in crossboundary_id_list:
        alarm_type = "crossBoundary"
    else:
        alarm_type = "flowCount"
    try:
        myftp = FTP_class.My_FTP(settings.FTP_IP, settings.FTP_PORT, settings.FTP_USER, settings.FTP_PW)
        myftp.uploadfile('%s/'%(alarm_type) + os.path.basename(img_base_name),img)
        print('ftp uploading...')
    except Exception as e:
        print('myftp error:',e)


def mysql_insert(alarm_time,start_time,camera_id,camera_ip,alarm_data,img,ped_info,now_time):
    _db = common_func.mysql_connect(host=settings.TYS_MYSQL_IP, port=settings.TYS_MYSQL_PORT,
                        user=settings.TYS_MYSQL_USER, passwd=settings.TYS_MYSQL_PW, dbname=settings.TYS_MYSQL_DB)
    _cursor = _db.cursor()
    camera_id = str(camera_id)
    try:
        if camera_id in endplugging_id_list:
            alarm_type_id = 'AT6'
            #img_ftp_path = settings.FTP_EP_DIR + camera_id + str(int(now_time*1000)) + ".png"
            img_ftp_path = ''.join((settings.FTP_EP_DIR,camera_id,str(int(now_time*1000)),".png"))
            sql_str = "insert into alarm_info (alarm_time,camera_id,camera_ip,alarm_type_id,alarm_data,img,ped_info) " \
                      "values('%s','%d','%s','%s','%d','%s','%s')" \
                      %(alarm_time,int(camera_id),camera_ip,alarm_type_id,int(alarm_data),img_ftp_path,ped_info)
            print("insert into alarm_info")
            _cursor.execute(sql_str)
            _db.commit()
        elif camera_id in crossboundary_id_list:
            alarm_type_id = 'AT8'
            #img_ftp_path = settings.FTP_CB_DIR + camera_id + str(int(now_time*1000)) + ".png"
            img_ftp_path = ''.join((settings.FTP_CB_DIR, camera_id, str(int(now_time * 1000)), ".png"))
            sql_str = "insert into alarm_info (alarm_time,camera_id,camera_ip,alarm_type_id,alarm_data,img,ped_info) " \
                      "values('%s','%d','%s','%s','%d','%s','%s')" \
                      %(alarm_time, int(camera_id), camera_ip, alarm_type_id, int(alarm_data), img_ftp_path, ped_info)
            print("insert into alarm_info")
            _cursor.execute(sql_str)
            _db.commit()
        elif camera_id  in flowcount_id_list:
            global flow_count_num
            #img_ftp_path = settings.FTP_FC_DIR + camera_id + str(int(now_time*1000)) + ".png"
            img_ftp_path = ''.join((settings.FTP_FC_DIR, camera_id, str(int(now_time * 1000)), ".png"))
            try:
                sql_str_his = "insert into flowcount_info_his (alarm_time,start_time,camera_id,camera_ip,flowcount,img,ped_info)" \
                      "values('%s','%s','%d','%s','%d','%s','%s')" \
                      %(alarm_time,start_time,int(camera_id),camera_ip,int(alarm_data),img_ftp_path,ped_info)
                _cursor.execute(sql_str_his)
                _db.commit()
                print("inserting into flowcount_info_his...")
            except Exception as e:
                print('flowcount_info_mysql error:',e)
            lock_flag = flow_count_lock.acquire(True)  #True:block
            if lock_flag:
                if flow_count_num < settings.FLOW_COUNT_LOCK_NUM:   # threads blocking ....
                    flow_count_num += 1
                    flow_count_lock.release()
                else:
                    flow_count_num = 0
                    flow_count_lock.release()
                    sql_str = "insert into flowcount_info (alarm_time,camera_id,camera_ip,flowcount,img,ped_info)" \
                      "values('%s','%d','%s','%d','%s','%s')" \
                      %(alarm_time,int(camera_id),camera_ip,int(alarm_data),img_ftp_path,ped_info)
                    _cursor.execute(sql_str)
                    _db.commit()
                    print("inserting into flowcount_info...")
            print("-----flow_count_num------:",flow_count_num)
        else:
            print("camera_id is not for endplugging, crossboundary or flowcount alarming")
    except Exception as e:
        print("mysql error",e)
    finally:
        _cursor.close()
        _db.close()


@app.route('/dlconfigupdate', methods=['POST'])
def handle_config_request():
    global config_update_url
    global config_url_headers
    global common_error_response
    try:
        params_json_str = flask.request.get_data()
        if isinstance(params_json_str,bytes):
            params_json_str = params_json_str.decode('utf-8')
        print('------------params_json_str----------:',params_json_str)
        params_json = json.loads(params_json_str)
        camera_ids = params_json['camera_ids']
        try:
            data = {"camera_ids":camera_ids}
            data = bytes(json.dumps(data), 'utf8')
            request = urllib.request.Request(url=config_update_url, headers=config_url_headers, data=data)
            response_data = urllib.request.urlopen(request).read()
            if isinstance(response_data,bytes):
                response_data = response_data.decode('utf-8')
            print("------dlconfigupdate response data--------:",response_data,type(response_data))
            return response_data
        except Exception as e:
            print("config update error",e)
            return json.dumps(common_error_response)
    except Exception as e:
        print("request data error",e)
        return json.dumps(common_error_response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8083, threaded=True)
