#-*- coding:utf-8 -*-

from multiprocessing import Manager

from data_request import Region_Proc
from mysql_insert import Mysql_Proc

class Run_Proc(object):
    def __init__(self):
        print("init Run_Proc...")
        process_manager = Manager()
        response_queue = process_manager.Queue(100)
        for i in range(5):
            response_queue.put(str(i))
        print(response_queue.get())

        self.buffer_room = {"camera_id_list":"1,2"}
        hct_process = Region_Proc(self.buffer_room,response_queue,5)
        hct_process.daemon = True
        hct_process.start()

        self.waiting_room = {"camera_id_list":"3,4,5,6"}
        hcs_process = Region_Proc(self.waiting_room,response_queue,5)
        hcs_process.daemon = True
        hcs_process.start()

        self.ticket_room = {"camera_id_list":"7,8"}
        spt_process = Region_Proc(self.ticket_room, response_queue,5)
        spt_process.daemon = True
        spt_process.start()

        pri_process = Mysql_Proc(response_queue)
        pri_process.daemon = True
        pri_process.start()

        #time.sleep(10)
        #hct_process.join()
        #hcs_process.join()
        #spt_process.join()
        #pri_process.join()
