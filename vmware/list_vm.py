# encoding: utf-8
import atexit
from pyVmomi import vim, vmodl
from .vcenter_class import vcenter_class 


#根据传入的虚拟机对象，获取单个虚拟机的相关summary信息，返回自己组的dict
def vm_info(virtual_machine):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    summary = virtual_machine.summary
    # print("Name       : ", summary.config.name)
    vmname = summary.config.name
    # print("Template   : ", summary.config.template)
    # print("Path       : ", summary.config.vmPathName)
    vmpath = summary.config.vmPathName
    # print("Guest      : ", summary.config.guestFullName)
    os = summary.config.guestFullName
    instanceuuid = summary.config.instanceUuid
    #备注
    annotation = summary.config.annotation
    #电源状态
    state = summary.runtime.powerState
    if summary.guest is not None:
        ip_address = summary.guest.ipAddress
        tools_version = summary.guest.toolsStatus
    #     print("Question  : ", summary.runtime.question.text)
    vminfo = {
    		"vmname" : vmname,
    		"os" : os,
            "ip_address" : ip_address,
            "state" : state,
            "instanceuuid" : instanceuuid
    }
    
    return vminfo
    

#获取单个虚拟机对象dict，并排成列表
def get_vm_info():

    try:
        children=vcenter_class.hdzjzvc.get_vms_and_templates()
        vmlist = []
        for child in children:
            if child.config.template:
                pass
            else:
                vmlist.append(vm_info(child))
        return vmlist
    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1



# Start program
if __name__ == "__main__":
    vm_summary()