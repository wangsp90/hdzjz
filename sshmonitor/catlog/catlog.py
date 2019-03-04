#!/usr/bin/python36
# -*- coding: utf-8 -*-
import paramiko,threading
from queue import Queue
import time,re

class MyServer(object):
    def __init__(self, hostname,username,password,cmd):
        super(MyServer, self).__init__()
        self.hostname = hostname
        self.username = username
        self.password = password
        self.cmd = cmd

    def sshclient(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname,
            username=self.username,
            password=self.password)
        return ssh

    def catlog(self,ssh):
        sin,sout,serr = ssh.exec_command(self.cmd)
        return sin,sout,serr

    def compare(self,err):
        ssh = self.sshclient()
        errmsg = []
        sin,sout,serr = self.catlog(ssh)
        while True:
            l = sout.readline()
            if l:
                r = re.search(err,l,re.I)
                if r:
                    errmsg.append(l)
            else :
                break
        return {self.hostname:errmsg}

def get_errmsg(host,err_list):
    errmsg = host.compare("error")
    if errmsg[host.hostname]:
        err_list.put(errmsg)


if __name__ == '__main__':
    hostnames = ["10.100.174.26","10.100.174.27","10.100.174.28","10.100.174.21"]
    username = 'root'
    password = 'HD@it2019'
    t1 = time.time()
    #多线程实现
    err_list = Queue()
    for hostname in hostnames:
        host = MyServer(hostname,username,password,"cat /root/passwd")
        thread = threading.Thread(target=get_errmsg,args=(host,err_list,))
        thread.start()
    thread.join()
    while True:
        if err_list.empty():
            print ("空的")
            break
        else:
            print (err_list.get(block=True,timeout=1))
    #非多线程实现
    # for hostname in hostnames:
    #     host = MyServer(hostname,username,password,"cat /root/passwd")
    #     errmsg = host.compare("error")
    #     if errmsg[host.hostname]:
    #         print (errmsg)

    t2 = time.time()
    print (t2 - t1)