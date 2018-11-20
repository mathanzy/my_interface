#-*- coding:utf-8 -*-

from multiprocessing import Process
import time
from functools import reduce

import pymysql

import settings
import common_func

class Mysql_Proc(Process):
    def __init__(self,queue):
        Process.__init__(self)
        print("init Mysql_Proc...")
        self.__queue = queue
        self.table_names = ['regioncount_info','queue_info']
        self.sql_region = "insert into regioncount_info (alarm_time, camera_id, camera_ip, alarm_data,heat_img) values ('%s','%d','%s','%s','%s')"
        self.sql_queue = "insert into queue_info (alarm_time, camera_id, camera_ip, alarm_window, alarm_data) values ('%s','%d','%s','%s','%s')"
        self.time_format = "%Y-%m-%d %H:%M:%S"
        #self.__queue.put(str(100))

    def run(self):
        try:
            db = common_func.mysql_connect(host=settings.TYS_MYSQL_IP, port=settings.TYS_MYSQL_PORT, user=settings.TYS_MYSQL_USER,
                               passwd=settings.TYS_MYSQL_PW, dbname=settings.TYS_MYSQL_DB)
            cursor = db.cursor()
        except Exception as e:
            print("mysql connect error",e)
            return None
        while True:
            start_time = time.time()
            try:
                (camera_id_list, count_list, alarm_time,img) = self.__queue.get_nowait()
                print("#########camera_id_list,count_list#####",camera_id_list,count_list)
                alarm_time = time.strftime(self.time_format, time.localtime(alarm_time))
                if camera_id_list == "1,2":
                    camera_id = int(1)
                    camera_ip = "10.90.129.170"
                    #alarm_data = reduce(self.add, map(int, count_list))
                    alarm_data = reduce(lambda x,y:x+y, map(int,count_list))
                    heat_img = img
                    sql_str = self.sql_region %(alarm_time,camera_id,camera_ip,alarm_data,heat_img)
                    cursor.execute(sql_str)
                    db.commit()
                    print("1111111111111")
                    print("1,2 right",alarm_data,alarm_time,img)
                elif camera_id_list == "3,4,5,6":
                    camera_id = int(3)
                    camera_ip = "10.90.129.172"
                    alarm_data = reduce(self.add, map(int, count_list))
                    heat_img = img
                    sql_str = self.sql_region %(alarm_time,camera_id,camera_ip,int(alarm_data),heat_img)
                    cursor.execute(sql_str)
                    db.commit()
                    print("3333333333333")
                    print("3,4,5,6 ok", count_list,alarm_time)
                elif camera_id_list == "7,8":
                    camera_id = int(7)
                    camera_ip = "10.90.129.180"
                    alarm_window = "15"
                    #print("-----count_list-------",count_list,type(count_list))
                    #alarm_data = ','.join(count_list)
                    alarm_data =','.join(list(map(str,count_list))) 
                    #print('-------alarm_data-----',alarm_data)
                    sql_str = self.sql_queue %(alarm_time,camera_id,camera_ip,alarm_window,alarm_data)
                    cursor.execute(sql_str)
                    db.commit()
                    print("7777777777777777777")
                    print("7,8 yes",count_list,alarm_time)
                else:
                    print("there is no camera id list")
            except Exception as e:
                print('queue is null ',e)
            end_time = time.time()
            print('mysql runing time:',end_time - start_time)
            print('queue length:',self.__queue.qsize())
            time.sleep(1)

    def add(self, x,y):
        return x+y
