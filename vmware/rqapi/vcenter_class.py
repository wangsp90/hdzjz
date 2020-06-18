import json
import base64
import requests
#֤�鲻��ȫʱ��POST������Ҫ��verify=False����ʱ���Ӿͻ��о��棬��Ҫ��urllib3�е�disable_warnings����ȥ������
requests.packages.urllib3.disable_warnings()
vcname = "vc.hdzjj.local"
user = "administrator@vsphere.local"
passwd = ""

class vCenter(object):
	"""docstring for vCenter"""
	def __init__(self):
		self.vcname = ""
		self.user = ""
		self.passwd = ""
		self.token = ""
		self.sessionid = ""

	def get_value(self,vcname,user,passwd):
		self.vcname = vcname
		self.user = user
		self.passwd = passwd
		authen_info = self.authen_info()
		self.get_token(authen_info)

#http post����header����
	def authen_info(self):
		user_pwd = self.user + ":" + self.passwd
		user_pwd_encode = user_pwd.encode()
		userinfo = base64.b64encode(user_pwd_encode).decode("ascii")
		authen_headers = {'Authorization' : 'Basic %s' % userinfo}
		return authen_headers

	def get_token(self,authen_headers):
		url = 'https://' + self.vcname + '/rest/com/vmware/cis/session'
		r = requests.post(url,headers=authen_headers,verify=False)
		self.token = json.loads(r.text)
		self.sessionid = {'vmware-api-session-id':self.token["value"]}		

	def get_vms(self,vmname):
		url = 'https://' + self.vcname + '/rest/vcenter/vm/' + vmname
		r = requests.get(url, headers=self.sessionid,verify=False)
		return r.text

	def get_tasks(self):
		url = 'https://' + self.vcname + '/rest/cis/tasks'
		r = requests.get(url, headers=self.sessionid, verify=False)
		print (r.text)

if __name__ == '__main__':
	zjzvc = vCenter()
	zjzvc.get_value(vcname,user,passwd)
	zjzvc.get_tasks()
