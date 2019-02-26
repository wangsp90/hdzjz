# encoding: utf-8
import atexit

from pyVmomi import vmodl
from pyVmomi import vim
from .connect_vc import *
from pyVim.connect import SmartConnectNoSSL, Disconnect

#获取所有虚拟机以及模板，并返回所有对象
def get_vms_and_templates():

    try:
        service_instance = get_si(host="vc.hdzjj.local",user="administrator@vsphere.local",pwd="HD@it2019")
        atexit.register(Disconnect, service_instance)

        content = service_instance.RetrieveContent()

        container = content.rootFolder  # starting point to look into
        viewType = [vim.VirtualMachine]  # object types to look for
        recursive = True  # whether we should look into it recursively
        containerView = content.viewManager.CreateContainerView(
            container, viewType, recursive)

        children = containerView.view
        return children
    except Exception as error:
        return error

#根据传入的虚拟机对象，获取虚拟机的相关summary信息，返回自己组的json
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
    

#获取虚拟机对象，做成dict后，并排成列表
def get_vm_info():

    try:
        children=get_vms_and_templates()
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