# -*- coding: utf-8 -*-
from .vcenter_class import vcenter_class

def poweronvm_task(iuuid):
	vmlist=vcenter_class.hdzjzvc.get_vms_and_templates()
	for v in vmlist:
		if v.summary.config.instanceUuid == iuuid:
			v.PowerOn()
			return 1

def poweroffvm_task(iuuid):
	vmlist=vcenter_class.hdzjzvc.get_vms_and_templates()
	for v in vmlist:
		if v.summary.config.instanceUuid == iuuid:
			v.PowerOff()
			return 1