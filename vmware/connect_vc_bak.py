# encoding: utf-8
import atexit
from pyVmomi import vim, vmodl
from pyVim.connect import SmartConnectNoSSL, Disconnect

def get_si(host,user,pwd):
    try:
        si = SmartConnectNoSSL(host=host, user=user, pwd=pwd, port=443)
        print (si)
        return si
    except vmodl.MethodFault as error:
        print ("Caught vmodl fault : " + error.msg)
        return (False, error.msg)
    return True, "ok"

def connect_vc(host,user,pwd):
    try:
        si = SmartConnectNoSSL(host=host, user=user, pwd=pwd, port=443)
        atexit.register(Disconnect, si)
        content = si.RetrieveContent()
        dcs=content.rootFolder.childEntity
        print (dcs)
        return (content,dcs)
    except vmodl.MethodFault as error:
        print ("Caught vmodl fault : " + error.msg)
        return (False, error.msg)
    return True, "ok"

if __name__ == '__main__':
    connect_vc("vc.hdzjj.local","administrator@vsphere.local","HD@it2019")
