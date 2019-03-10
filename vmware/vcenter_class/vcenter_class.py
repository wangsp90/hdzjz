# encoding: utf-8
import atexit
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnectNoSSL, Disconnect

class vCenter(object):
	def __init__(self):
		self.host = "please enter vcenter ip or URL"
		self.user = "please enter vcenter user"
		self.pwd = "please enter user's password"
		self.si = ""
	
	def get_value(self,host,user,pwd):
		self.host = host
		self.user = user
		self.pwd = pwd
		self.si = self.get_si()

	def get_si(self):
		try:
			si = SmartConnectNoSSL(host=self.host, user=self.user, pwd=self.pwd, port=443)
			return si
		except vmodl.MethodFault as error:
			print ("Caught vmodl fault : " + error.msg)
			return (False, error.msg)
			return True, "ok"
#get方法获取数据中心的各种数据信息集合
	def get_vms_and_templates(self):
		try:
			atexit.register(Disconnect, self.si)
			content = self.si.content
			container = content.rootFolder  # starting point to look into
			viewType = [vim.VirtualMachine]  # object types to look for
			recursive = True  # whether we should look into it recursively
			containerView = content.viewManager.CreateContainerView(
			    container, viewType, recursive)
			vm_children = containerView.view
			return vm_children
		except Exception as error:
			return error

	def get_datastores(self):
		try:
			atexit.register(Disconnect, self.si)
			content = self.si.content
			container = content.rootFolder  # starting point to look into
			viewType = [vim.Datastore]  # object types to look for
			recursive = True  # whether we should look into it recursively
			containerView = content.viewManager.CreateContainerView(
			    container, viewType, recursive)
			ds_children = containerView.view
			return ds_children
		except Exception as error:
			return error

	def get_network(self):
		try:
			atexit.register(Disconnect, self.si)
			content = self.si.content
			container = content.rootFolder  # starting point to look into
			viewType = [vim.Network]  # object types to look for
			recursive = True  # whether we should look into it recursively
			containerView = content.viewManager.CreateContainerView(
			    container, viewType, recursive)
			net_children = containerView.view
			return net_children
		except Exception as error:
			return error

	def get_host(self):
		try:
			atexit.register(Disconnect, self.si)
			content = self.si.content
			container = content.rootFolder  # starting point to look into
			viewType = [vim.HostSystem]  # object types to look for
			recursive = True  # whether we should look into it recursively
			containerView = content.viewManager.CreateContainerView(
			    container, viewType, recursive)
			host_children = containerView.view
			return host_children
		except Exception as error:
			return error

	def get_spec(self):
		try:
			atexit.register(Disconnect, self.si)
			content = self.si.content
			spec_list = content.customizationSpecManager.info
			return spec_list
		except Exception as error:
			return error
#find方法，通过指定条件查找指定内容
	def find_byip(self):
		pass

	def find_bydnsname(self):
		pass

	def find_byuuid(self):
		pass

	def find_bydatastorepath(self):
		pass

	def find_byfolder(self):
		pass

#主机组组内测试环境			
host="vc.hdzjj.local"
user="administrator@vsphere.local"
pwd="HD@it2019"

hdzjzvc = vCenter()
hdzjzvc.get_value(host,user,pwd)

if __name__ == '__main__':

	hdzjz = vCenter()
	hdzjz.get_value(host,user,pwd)
	vm_list = hdzjz.get_vms_and_templates()
	ds_list = hdzjz.get_datastores()
	network_list = hdzjz.get_network()
	host_list = hdzjz.get_host()
	spec_list = hdzjz.get_spec()
	print (spec_list)