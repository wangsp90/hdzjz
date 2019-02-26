# -*- coding: utf-8 -*-
import vmware.list_vm

def poweronvm_task(iuuid):
	vmlist=vmware.list_vm.get_vms_and_templates()
	for v in vmlist:
		if v.summary.config.instanceUuid == iuuid:
			v.PowerOn()
			return 1

def poweroffvm_task(iuuid):
	vmlist=vmware.list_vm.get_vms_and_templates()
	for v in vmlist:
		if v.summary.config.instanceUuid == iuuid:
			v.PowerOff()
			return 1