#!/usr/bin/python36
# -*- coding: utf-8 -*-
#多线程学习的关键
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
        try:
            ssh.connect(hostname=self.hostname,
                username=self.username,
                password=self.password) 
        except Exception as e:
            print (e)
        
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
                    if int(i[-1]) > 60:
                        n = n + 1
            else:
                break
        ssh.close()
        log_list.put(n)


if __name__ == '__main__':
    hostnames = ["10.100.174.2","10.100.174.3"]
    username = 'root'
    password = 'D@ll2018'

    log_list = Queue()
    ll = []
    tlist = []  #线程的序列，需要先将所有线程存入序列再进行并发操作
    for hostname in hostnames:
        host = MyServer(hostname,username,password,"cat /tmp/test.log")
        thread = threading.Thread(target=host.get_congestion,args=(log_list,))
        tlist.append(thread)
#经过多次测试，需要将使用以下方式进行执行才可以保证所有线程都完成
    for t in tlist:
        t.start()
    for t in tlist:
        t.join()
        
    for i in range(log_list.qsize()):
        ll.append(log_list.get())
    print (ll)
    print (max(ll))