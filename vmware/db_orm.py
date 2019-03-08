# -*- coding: utf-8 -*-
from .models import vminfo

#更新现有虚拟机或将新的虚拟机录入数据库
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

#从数据库中删除已经不存在的虚拟机信息
def cleanvmtable(namelist):
	try:
		vm=vminfo.objects.all()
		for v in vm:
			if v.VMNAME in namelist:
				pass
			else:
				v.delete() 
	except Exception as e:
		print (e)

#获取数据库中的所有虚拟机信息
def db_getvminfo():
	vm=vminfo.objects.all()
	return vm