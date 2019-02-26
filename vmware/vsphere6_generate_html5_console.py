
import atexit
import OpenSSL
import ssl
import sys
import time

from pyVim.connect import SmartConnect, Disconnect, SmartConnectNoSSL
from pyVmomi import vim


def get_thevm(content, name):
    try:
        # name = unicode(name, 'utf-8')
        name = str(name, 'utf-8')
    except TypeError:
        pass

    vm = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True)

    for c in container.view:
        if c.name == name:
            vm = c
            break
    return vm


def get_webmks_url(vm_name):
    """
    Simple command-line program to generate a URL
    to open HTML5 Console in Web browser
    """

    try:
        si = SmartConnectNoSSL(host="vc.hdzjj.local",
                            user="administrator@vsphere.local",
                            pwd="HD@it2019",
                            port=443)
        # si = SmartConnect(host=args.host,
        #                   user=args.user,
        #                   pwd=args.password,
        #                   port=int(args.port))
    except Exception as e:
        print ('Could not connect to vCenter host')
        print (repr(e))
        sys.exit(1)

    atexit.register(Disconnect, si)
    
    content = si.RetrieveContent()

    vm = get_thevm(content, vm_name)

    if vm.summary.runtime.powerState == "poweredOff":
        return 0
    elif vm.summary.runtime.powerState == "poweredOn":
        x = vm.AcquireTicket("webmks")

        url = "wss://" + str(x.host) +":" + str(x.port)   + "/ticket/" + str(x.ticket)
    
        return url
    # print ("Waiting for 60 seconds, then exit")

# Start program
if __name__ == "__main__":
    vm_name = "mysql"
    print (get_webmks_url(vm_name))