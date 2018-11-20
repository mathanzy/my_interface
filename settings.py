#-*- coding:utf-8 -*-
'''
functional: common configure of the parameters
env:py 3
time: 2018-10-08
'''


#######  Common  #########
# The response for http request
success_response = {"status":"success"}
error_response = {"status":"error","data":{"error_code":403,"error_message":"传入参数不正确"}}
common_error_response = {"status":"error1"}

# The camera list for different function
endplugging_id_list = ['10','11']  # Cameras list of endplugging
crossboundary_id_list = []         # Cameras list of crossboundary
flowcount_id_list = ['9']          # Cameras list of flowcount


####### Tai yuan Station  #######
# Tai yuan station MySQL parameters
TYS_MYSQL_IP = "172.28.3.91"  # 172.28.3.137/91 for test; 10.90.129.163 is Tai yuan Station
TYS_MYSQL_PORT = 3306
TYS_MYSQL_USER = "facepp"    #facepp for test; root is Tai yuan Station
TYS_MYSQL_PW = "111111"       #111111 for test; root is Tai yuan Station
TYS_MYSQL_DB = "smartvideo"

# brain http url
brain_http_url = "http://10.90.129.163:8082/queueLength"
#brain_http_url = "http://127.0.0.1:8082/queueLength"  #test



######### Face++ #############
# Face++ region_crowd url
region_crowd_url = "http://127.0.0.1:9099/region_crowd"
config_update_url = "http://127.0.0.1:8084/dlconfigupdate"
config_url_headers = {'Content-Type': 'multipart/form-data'}



######## Front End #############
# Front End progress
front_end_alarm_url = "http://172.28.3.137:8082/platform_alarm"



####### FTP ##############
# FTP
FTP_IP = "172.28.3.91"
FTP_PORT = 21
FTP_USER = "platformftp"
FTP_PW = "111111"
FTP_EP_DIR = "E:/platform_alarm/endPlugging/"
FTP_CB_DIR = "E:/platform_alarm/crossBoundary/"
FTP_FC_DIR = "E:/platform_alarm/flowCount/"


##############
FLOW_COUNT_LOCK_NUM = 5   # a global variable as a threading lock for the flow count threadings
