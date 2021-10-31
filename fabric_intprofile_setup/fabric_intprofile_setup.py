import re
import sys
import requests
import json
sys.path.append("..")
from login.get_token import get_token
from login_info import apic
from startup_config import startupconfig

#block below: user input leaf range, from $leaf1 to $leaf2, every leaf add $portcount port profile
####################################################################################################
leaf1=''
leaf2=''
portcount=''

#below input leaf range ex. 101-106
while True:
    swtmp = input("Enter leaf range: ex. 101-106\n")
    if re.match(r'^([1-9])([0-9]{2})\-([1-9])([0-9]{2})$',swtmp):
        ma=re.match(r'^([1-9])([0-9]{2})\-([1-9])([0-9]{2})$',swtmp)
        if ma.group(1)==ma.group(3) and ma.group(2)<=ma.group(4):
            leaf1 = ma.group(1)+ma.group(2)
            leaf2 = ma.group(3)+ma.group(4)
            print(leaf1+"\t"+leaf2)
            break
leaf1=int(leaf1)
leaf2=int(leaf2)+1

#below input port count on every leaf
while True:
    pctmp = input("Enter port count: ex. 48\n")
    if re.match(r'^[0-9]{2}$',pctmp):
        portcount=pctmp
        break
portcount=int(portcount)+1

###################################################################################################
###################################################################################################
   

#method to config Fabric->Access Policies->Interfaces->Leaf Interfaces->Profiles
#for each leaf
###################################################################################################
def swint_startup(itoken,iswitch):
    iswitch=str(iswitch)
    dn = "uni/infra/accportprof-"+iswitch+"_interface"
    profilename = iswitch+"_interface"
    url = "https://"+apic+"/api/mo/"+dn+".json"
    payload = {
        "totalCount": "1",
        "imdata": [
            {
                "infraAccPortP": {
                    "attributes": {
                        "descr": "",
                        "dn": dn,
                        "name": profilename,
                    }
                }
            }
        ]
    }
    
    headers = {
        "Cookie": f"APIC-Cookie={itoken}",
    }
    
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url,data=json.dumps(payload),headers=headers,verify=False)
    
    if (response.status_code == 200):
        print("swint profile:"+profilename+"  OK\n")
    else:
        print(response.text+"\n")
        print("swint profile:"+profilename+"  fail\n")
        input("continue?\n")

###################################################################################################

#method to config Fabric->Access Policies->Interfaces->Leaf Interfaces->Profiles->
#for each port under each leaf   
###################################################################################################
def int_setup(itoken,iport,iswitch):
    iswitch=str(iswitch)
    iport=str(iport)
    dn = "uni/infra/accportprof-"+iswitch+"_interface/hports-"+iport+"-typ-range"
    url = "https://"+apic+"/api/mo/"+dn+".json"
    #below   from \..\startup_config\startupconfig get common interface policy name for port selector
    tdn = "uni/infra/funcprof/accportgrp-"+startupconfig["common_intpolicy"]
    payload = {
        "totalCount": "1",
        "imdata": [
            {
                "infraHPortS": {
                    "attributes": {
                        "descr": "",
                        "dn": dn,
                        "name": iport,
                        "type": "range"
                    },
                    "children": [
                        {
                            "infraRsAccBaseGrp": {
                                "attributes": {
                                    "fexId": "101",
                                    "tDn": tdn
                                }
                            }
                        },
                        {
                            "infraPortBlk": {
                                "attributes": {
                                    "descr": "",
                                    "fromCard": "1",
                                    "fromPort": iport,
                                    "name": "block2",
                                    "toCard": "1",
                                    "toPort": iport
                                }
                            }
                        }
                    ]
                }
            }
        ]
    }
    
    headers = {
        "Cookie": f"APIC-Cookie={itoken}",
    }
    
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url,data=json.dumps(payload),headers=headers,verify=False)
    
    if (response.status_code == 200):
        print("sw:%s  port:%s  OK\n"%(iswitch,iport))
    else:
        print(response.text+"\n")
        print("sw:%s  port:%s  fail\n"%(iswitch,iport))
        input("continue?\n")
        
###################################################################################################

#login apic ask for a token
###################################################################################################
token = get_token()
if not token:
    print("get token fail")
    sys.exit()
###################################################################################################

#create interface profile for every switch from leaf1(ex.101) to leaf2(ex.106)
#under every leaf interface profile add portcount(ex.48) interface selector and config common interface policy
#common interface policy set the interface to trunk mode, diliver endpoint to different epg regarding packet's vlan tag
###################################################################################################
for switch in range(leaf1,leaf2):
    input(token+"\n"+str(switch))
    swint_startup(token,switch)
    for port in range(1,portcount):
        input(str(port))
        int_setup(token,port,switch)





