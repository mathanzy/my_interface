#-*- coding:utf-8 -*-
'''
functional: request data from the api /region_crowd for the region count and queue length with a period time
env: py3
time: 2018-09-23
'''

from multiprocessing import Process
import json
import urllib
from urllib import request
import time

import settings


real_url = settings.region_crowd_url
headers = {'Content-Type': 'multipart/form-data'}

class Region_Proc(Process):
    def __init__(self,data,queue,interval = 5):
        Process.__init__(self)
        print("init Region_Proc...")
        self.interval = interval
        self.data = data
        self.__queue = queue
        #print(queue.get_nowait())

    def run(self):
        global headers
        global real_url
        data = bytes(json.dumps(self.data),'utf8')
        while True:
            img = None
            request = urllib.request.Request(url= real_url, headers = headers, data = data)
            try:
                response_data = urllib.request.urlopen(request)
                # response_data_dict = json.loads(response_data.read())
                response_data_dict = json.loads(response_data.read().decode('UTF-8'))
                print("response_data_dict-------------",response_data_dict,type(response_data_dict))
                if response_data_dict['status'] == "success":
                    success_data = response_data_dict['data']
                    print("success_data-------------------------",success_data,type(success_data))
                    count_list = []
                    for i in range(len(success_data)):
                        count_list.append(success_data[i]['peoples'])
                    #print(str(count_list),type(count_list))
                    '''
                    if "heatmap" in success_data[1]:
                        img = success_data[1]["heatmap"]
                    '''
                    try:
                        if self.__queue.qsize() == 100:
                            print("queue is full")
                        self.__queue.put_nowait((self.data["camera_id_list"], count_list, time.time(),img))
                    except Exception as e:
                        print('queue put error',e)
                else:
                    print(response_data_dict['data'])
            except Exception as e:
                print("Request error:",e)
                #return None
            time.sleep(self.interval)


