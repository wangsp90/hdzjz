import paramiko
import paramiko_expect
import interactive

# Create your views here.

hostname = "10.100.174.26"
username = 'root'
password = 'HD@it2019'

def SSHClient(hostname,username,password):
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=hostname,
			username=username,
			password=password)
		return ssh
	except Exception as e:
		print (e)

if __name__ == '__main__':
	ssh = SSHClient(hostname,username,password)
	#建立交互式shell连接
	channel=ssh.invoke_shell()
	#建立交互式管道
	interactive.windows_shell(channel)
	#关闭连接
	channel.close()
	ssh.close()

