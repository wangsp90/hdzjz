import paramiko,threading
from queue import Queue
import time

hostnames = ["10.100.174.26","10.100.174.27","10.100.174.28","10.100.174.21"]
username = 'root'
password = 'HD@it2019'

sshs = Queue()

def sshclient(hostname,username,password):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=hostname,
		username=username,
		password=password)
	return ssh

def qput(q,hostname,username,password):
	ssh = sshclient(hostname,username,password)
	#q.put(ssh,block=True,timeout=1)
	q.put(ssh)

def read_df(ssh,cmd):
	sin,sout,serr = ssh.exec_command(cmd)
	l = sout.read().decode("utf-8")
	print (l)
	ssh.close()

if __name__ == '__main__':
	t1 = time.time()

	for hostname in hostnames:
		p1=threading.Thread(target=qput,args=(sshs,hostname,username,password,))
		p1.start()
	print ("all ssh done")
	p1.join()
	print (sshs.empty())
	print (sshs.qsize())

	while True:
		if sshs.empty():
			print ("空的")
			break
		else:
			value = sshs.get(block=True,timeout=2)
			p2=threading.Thread(target=read_df,args=(value,"df -h",))
			p2.start()
			print(value)
	p2.join()

	t2 = time.time()

	print (t2 - t1)