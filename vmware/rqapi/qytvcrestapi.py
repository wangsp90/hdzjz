import json
from cred import *
from urllib3 import *
from base64 import b64encode

disable_warnings()

http = PoolManager()

user_pass_str = username + ':' + password
user_pass_str_encode = user_pass_str.encode()
userAndPass = b64encode(user_pass_str_encode).decode("ascii")

#print(user_pass_str)
#print(user_pass_str_encode)
#print(b64encode(user_pass_str_encode))
#print(userAndPass)

authen_headers = {'Authorization' : 'Basic %s' % userAndPass}

#print(authen_headers)

def get_token(vcip,username,password):
    url = 'https://' + vcip + '/rest/com/vmware/cis/session'
    r = http.request('POST',url,headers=authen_headers)
    token = r.data.decode()
    return json.loads(token)['value']

def get_vms(vcip,token):
    headers = {'vmware-api-session-id':token}
    url = 'https://' + vcip + '/rest/vcenter/vm'
    r = http.request('GET', url, headers=headers)
    return json.loads(r.data.decode())['value']

def get_hosts(vcip,token):
    headers = {'vmware-api-session-id':token}
    url = 'https://' + vcip + '/rest/vcenter/host'
    r = http.request('GET', url, headers=headers)
    return json.loads(r.data.decode())['value']

def get_folders(vcip,token):
    headers = {'vmware-api-session-id':token}
    url = 'https://' + vcip + '/rest/vcenter/folder'
    r = http.request('GET', url, headers=headers)
    return json.loads(r.data.decode())['value']

def get_datastores(vcip,token):
    headers = {'vmware-api-session-id':token}
    url = 'https://' + vcip + '/rest/vcenter/datastore'
    r = http.request('GET', url, headers=headers)
    return json.loads(r.data.decode())['value']

def get_networks(vcip,token):
    headers = {'vmware-api-session-id':token}
    url = 'https://' + vcip + '/rest/vcenter/network'
    r = http.request('GET', url, headers=headers)
    return json.loads(r.data.decode())['value']

def create_vm(vcip,token,vmname):
    headers = {'vmware-api-session-id':token,'Content-Type':'application/json'}
    vm_json = {
               "spec": {
                        "placement": {
                                      "folder": "group-v65",#文件夹的唯一标识
                                      "host": "host-28",#主机的唯一标识
                                      "datastore": "datastore-29"#输出存储的唯一标识
                                      },
                        "name": vmname,#主机名
                        "guest_OS": "RHEL_7_64",#操作系统
                        "memory": {
                                   "hot_add_enabled": True,#注意Python需要大写首部的True
                                   "size_MiB": 1024#内存大小
                                  },
                        "cpu": {
                                "count": 1,#物理CPU数量
                                "hot_add_enabled": True,#注意Python需要大写首部的True
                                "hot_remove_enabled": True,#注意Python需要大写首部的True
                                "cores_per_socket": 1#CPU内核数
                                }
                        }
               }
    url = 'https://' + vcip + '/rest/vcenter/vm'
    r = http.request('POST', url, headers=headers,body=json.dumps(vm_json))
    return json.loads(r.data.decode())['value']


def add_vm_nic(vcip,token,vmid,network_name):
    headers = {'vmware-api-session-id':token,'Content-Type':'application/json'}
    add_nic_json = {
                        "spec": {
                                 "backing": {
                                             "type": "STANDARD_PORTGROUP",
                                             "network": network_name
                                            },
                                 "allow_guest_control": True,
                                 "mac_type": "ASSIGNED",
                                 "wake_on_lan_enabled": True,
                                 "start_connected": True,
                                 "type": "VMXNET3"
                                 }
                        }
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/hardware/ethernet'
    r = http.request('POST', url, headers=headers,body=json.dumps(add_nic_json))
    return json.loads(r.data.decode())['value']

def get_vm_nics(vcip,token,vmid):
    headers = {'vmware-api-session-id':token}
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/hardware/ethernet'
    r = http.request('GET', url, headers=headers)
    return json.loads(r.data.decode())['value']

def get_vm_nic_detail(vcip,token,vmid,nic):
    headers = {'vmware-api-session-id':token}
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/hardware/ethernet/' + nic
    r = http.request('GET', url, headers=headers)
    return json.loads(r.data.decode())['value']

def update_vm_nic(vcip,token,vmid,nic,network_name):
    headers = {'vmware-api-session-id':token,'Content-Type':'application/json'}
    update_nic_json = {
        "spec": {
            "backing": {
                "type": "STANDARD_PORTGROUP",
                "network": network_name
            },
        }
    }
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/hardware/ethernet/' + nic
    r = http.request('PATCH', url, headers=headers,body=json.dumps(update_nic_json))
    return r.data

def get_vm_power_status(vcip,token,vmid):
    headers = {'vmware-api-session-id':token}
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/power'
    r = http.request('GET', url, headers=headers)
    return json.loads(r.data.decode())['value']

def poweron_vm(vcip,token,vmid):
    headers = {'vmware-api-session-id':token}
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/power/start'
    r = http.request('POST', url, headers=headers)
    return r.data

def poweroff_vm(vcip,token,vmid):
    headers = {'vmware-api-session-id':token}
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid + '/power/stop'
    r = http.request('POST', url, headers=headers)
    return r.data

def delete_vm(vcip,token,vmid):
    headers = {'vmware-api-session-id':token}
    url = 'https://' + vcip + '/rest/vcenter/vm/' + vmid
    r = http.request('DELETE', url, headers=headers)
    return r.data

if __name__ == '__main__':
    token = get_token(vcip,username,password)
    #print(token)
    #print(get_vms(vcip,token))
    #[{'memory_size_MiB': 4096, 'vm': 'vm-32', 'name': 'QYTvSphere-CentOS', 'power_state': 'POWERED_OFF', 'cpu_count': 2}, {'memory_size_MiB': 2048, 'vm': 'vm-61', 'name': 'QYTvSphere-CentOS2', 'power_state': 'POWERED_OFF', 'cpu_count': 1}, {'memory_size_MiB': 1024, 'vm': 'vm-71', 'name': 'newtest', 'power_state': 'POWERED_OFF', 'cpu_count': 1}]
    #print(get_hosts(vcip, token))
    #[{'host': 'host-28', 'name': '172.16.1.201', 'connection_state': 'CONNECTED', 'power_state': 'POWERED_ON'}]
    #print(get_folders(vcip,token))
    #[{'folder': 'group-d1', 'name': 'Datacenters', 'type': 'DATACENTER'}, {'folder': 'group-h23', 'name': 'host', 'type': 'HOST'}, {'folder': 'group-n25', 'name': 'network', 'type': 'NETWORK'}, {'folder': 'group-s24', 'name': 'datastore', 'type': 'DATASTORE'}, {'folder': 'group-v22', 'name': 'vm', 'type': 'VIRTUAL_MACHINE'}, {'folder': 'group-v65', 'name': 'qytvm', 'type': 'VIRTUAL_MACHINE'}]
    #print(get_datastores(vcip,token))
    #[{'datastore': 'datastore-29', 'name': 'datastore1', 'type': 'VMFS', 'free_space': 63896027136, 'capacity': 99321118720}]
    #print(get_networks(vcip,token))
    #[{'name': 'VM Network', 'type': 'STANDARD_PORTGROUP', 'network': 'network-30'}, {'name': 'qytang_net1', 'type': 'STANDARD_PORTGROUP', 'network': 'network-68'}]
    #print(create_vm(vcip,token,'finaltest2'))
    #print(add_vm_nic(vcip, token, 'vm-77', 'network-30'))
    #print(get_vm_nics(vcip,token,'vm-77'))
    #print(get_vm_nic_detail(vcip,token,'vm-77','4000'))
    #print(update_vm_nic(vcip,token,'vm-77','4000','network-68'))
    #print(get_vm_power_status(vcip,token,'vm-77'))
    #print(poweron_vm(vcip,token,'vm-32'))
    #print(poweroff_vm(vcip,token,'vm-77'))
    #print(delete_vm(vcip,token,'vm-77'))
