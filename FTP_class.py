#-*- coding:utf-8 -*-

from ftplib import FTP
import os

class My_FTP(object):
    def __init__(self,host,port,username=None,password=None):
        self.ftp = FTP()
        self.ftp.set_debuglevel(2)  #open the debug lever of 2, show the detail information
        self.ftp.connect(host,port)
        self.ftp.login(username,password)
    def downloadfile(self,remotepath,localpath):
        buffsize = 1024   #buffer size
        fp = open(localpath,'wb')  
        self.ftp.retrbinary('RETR'+remotepath,fp.write,buffsize)
        self.ftp.set_debuglevel(0)
        fp.close()
    def uploadfile(self,remotepath,localpath):
        buffsize = 1024
        try:
            fp = open(localpath,'rb')
            self.ftp.storbinary('STOR '+remotepath,fp,buffsize)
            self.ftp.set_debuglevel(0)
        except Exception as e:
            print('ftp error:', e)
        finally:
            fp.close()

if __name__ == "__main__":
    myftp = My_FTP('172.28.3.131',21,'ftpuser','12345')
    myftp.uploadfile('crossboundary.png', 'C:/Users/hzy/Desktop/imgtest/crossboundary.png')


