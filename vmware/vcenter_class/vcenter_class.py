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

	def get_vms_and_templates(self):
		try:
			atexit.register(Disconnect, self.si)
			content = self.si.RetrieveContent()
			container = content.rootFolder  # starting point to look into
			viewType = [vim.VirtualMachine]  # object types to look for
			recursive = True  # whether we should look into it recursively
			containerView = content.viewManager.CreateContainerView(
			    container, viewType, recursive)
			children = containerView.view
			return children
		except Exception as error:
			return error



if __name__ == '__main__':
	host="vc.hdzjj.local"
	user="administrator@vsphere.local"
	pwd="HD@it2019"

	hdzjz = vCenter()
	hdzjz.get_value(host,user,pwd)
	vm_children = hdzjz.get_vms_and_templates()
	print (vm_children)