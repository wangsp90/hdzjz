# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from .list_vm import *
from .db_orm import *
from .models import *
from .vsphere6_generate_html5_console import *
from .powerctl_vm import *
import json
from django.http import JsonResponse

def admin(request):
    """
    管理员首页
    """
    return render(request, 'admin.html')

def user(request):
    """
    普通用户首页
    """
    return render(request, 'index.html')

#虚拟机webconsole的调用
def webmks(request):
    """
    vmware vsphere virtual machine web console
    """
    vm_name = request.GET.get("url")
    weburl = get_webmks_url(vm_name)
    if weburl == 0:
        return HttpResponse("Server is not powerOn!")
    else:
        url = { 'weburl':weburl }
        return render(request, 'webmks/webconsole.html', url) 


#由主页中的AJAX调用，并返回虚拟机信息，其中虚拟机信息从数据库中查询，虚拟机状态从vcenter获取
def getvminfo(request):
    """
    首页
    """
    vminfo = []
    dbvms=db_getvminfo()
    livevms=get_vm_info()
    for v in dbvms:
        for lv in livevms:
            if v.VMNAME == lv['vmname']:
                state=lv['state']
                break
        vmdict = {
            "vmname" : v.VMNAME,
            "os" : v.OS,
            "ip_address" : v.IPADDRESS,
            
            "state" : state
        }
        vminfo.append(vmdict)
        vminfo_json=json.dumps({'vminfo' : vminfo})
        
    return JsonResponse({'vminfo' : vminfo})

#获取虚拟机列表，并插入到数据库表中，如果有新增加或者更新，则自动修改表，但是不会将已经不存在的虚拟机从表中删除    
def vminfo_input(request):
    try:
        vminfo = get_vm_info()
        namelist=[]
        for vm in vminfo:
            editvmtable(vm['vmname'],vm['ip_address'],vm['os'],vm['instanceuuid'])
            namelist.append(vm['vmname'])
        cleanvmtable(namelist)
        return HttpResponse("successful!")
    
    except Exception as e:
        print ('22222')
        return HttpResponse(e)

#虚拟机电源开
def poweronvm(request):
    name=request.GET.get("name")
    vmiuuid=vminfo.objects.get(VMNAME=name).INSTANCEUUID
    poweronvm_task(vmiuuid)
    return HttpResponse("success")
#虚拟机电源关
def poweroffvm(request):
    name=request.GET.get("name")
    vmiuuid=vminfo.objects.get(VMNAME=name).INSTANCEUUID
    poweroffvm_task(vmiuuid)
    return HttpResponse("success")

#Only for test some function,testurl
def testurl(request):
    v=db_getvminfo()
    return HttpResponse(v)