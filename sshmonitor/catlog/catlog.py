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

    def get_errmsg(self,err_list):
        #err_list是一个队列
        errmsg = self.compare("error")
        if errmsg[self.hostname]:
            err_list.put(errmsg)

    def get_congestion(self,log_list):
        #log_list是一个队列
        ssh = self.sshclient()
        sin,sout,serr = self.catlog(ssh)
        n = 0
        while True:
            li1 = [0]
            l = sout.readline()
            if len(l) == 37:
                li1[0]=l.strip("\n")
                for i in range(6):
                    l = sout.readline()
                    li1.append(l.strip(" ").strip("\n").split(":"))
                for i in li1[1:]:
                    if int(i[-1]) > 50:
                        n = n + 1
            else:
                break
        if n >= 1:
            print (1)
        else:
            print (0)


if __name__ == '__main__':
    hostnames = ["10.100.174.2","10.100.174.3"]
    username = 'root'
    password = 'D@ll2018'
    t1 = time.time()
    #多线程实现
    err_list = Queue()
    for hostname in hostnames:
        host = MyServer(hostname,username,password,"cat /tmp/test.log")
        thread = threading.Thread(target=host.get_errmsg,args=(err_list,))
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
##################################################################################
    log_list = Queue()
    for hostname in hostnames:
        host = MyServer(hostname,username,password,"cat /tmp/test.log")
        thread = threading.Thread(target=host.get_congestion,args=(log_list,))
        thread.start()
    thread.join()
