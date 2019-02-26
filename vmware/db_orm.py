# -*- coding: utf-8 -*-
from .models import vminfo

#虚拟机
def editvmtable(name,ip,os,iuuid):
	try:
		vm=vminfo.objects.get(VMNAME=name)
		if vm.VMNAME != name:
			vm.VMNAME = name
		elif vm.IPADDRESS != ip:
			vm.IPADDRESS = ip
		elif vm.OS != os:
			vm.OS = os
		elif vm.INSTANCEUUID != iuuid:
			vm.INSTANCEUUID = iuuid
		vm.save()
	except vminfo.DoesNotExist:
		vm=vminfo(VMNAME=name,IPADDRESS=ip,OS=os,INSTANCEUUID=iuuid)
		vm.save()

def db_getvminfo():
	vm=vminfo.objects.all()
	return vm