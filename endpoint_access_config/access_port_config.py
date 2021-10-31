import re
import sys
import requests
import json
sys.path.append("..")
from login.get_token import get_token
from login_info import apic
from startup_config import startupconfig
from startup_config import subnet_get_epgvlan
from tools.ipmask_transto_subnet import ipmask_transto_subnet

#method below used for mode TRUNK request read from .\accessrequest.csv, packages carry vlan tag when come into ACI
####################################################################################
def access_tag(itoken,ileaf,iport,idescription):
    #according to .\accessrequest.csv config interface policy group, use ..\startup_config->startupconfig["common_intpolicy"]
    dn = "uni/infra/accportprof-"+ileaf+"_interface/hports-"+iport+"-typ-range"
    url = "https://"+apic+"/api/mo/"+dn+".json"
    tdn = "uni/infra/funcprof/accportgrp-"+startupconfig["common_intpolicy"]
    payload = {
        "totalCount": "1",
        "imdata": [
            {
                "infraHPortS": {
                    "attributes": {
                        "annotation": "",
                        "descr": idescription,
                        "dn": dn
                    },
                    "children": [
                        {
                            "infraRsAccBaseGrp": {
                                "attributes": {
                                    "tDn": tdn
                                }
                            }
                        },
                        {
                            "infraPortBlk": {
                                "attributes": {
                                    "descr": idescription,
                                    "name": "block2"
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
        print("%s-eth1/%s: %s trunk mode complete\n"%(ileaf,iport,idescription)) #print ex. 105-eth1/41: ESXI-1 trunk mode complete
    else:
        print(response.text+"\n")
        print("%s-eth1/%s description fail\n"%(ileaf,iport))
        input("continue?\n")
###################################################################################################


#method below used for mode ACCESS request read from .\accessrequest.csv, packages don't carry vlan tag when come into ACI
####################################################################################
def access_untag(itoken,ileaf,iport,idescription,iepg,ivlan):
    #according to .\accessrequest.csv config interface policy group, use ..\startup_config->startupconfig["untag_intpolicy"]
    dn = "uni/infra/accportprof-"+ileaf+"_interface/hports-"+iport+"-typ-range"
    tdn = "uni/infra/funcprof/accportgrp-"+startupconfig["untag_intpolicy"]
    url = "https://"+apic+"/api/mo/"+dn+".json"
    payload = {
        "totalCount": "1",
        "imdata": [
            {
                "infraHPortS": {
                    "attributes": {
                        "annotation": "",
                        "descr": idescription,
                        "dn": dn
                    },
                    "children": [
                        {
                            "infraRsAccBaseGrp": {
                                "attributes": {
                                    "tDn": tdn
                                }
                            }
                        },
                        {
                            "infraPortBlk": {
                                "attributes": {
                                    "descr": idescription,
                                    "name": "block2"
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
        print("%s-eth1/%s: %s complete\n"%(ileaf,iport,idescription))
    else:
        print(response.text+"\n")
        print("%s-eth1/%s description fail\n"%(ileaf,iport))
        input("continue?\n")
    
    #under specific EPG create static port
    dn1 = "uni/tn-"+startupconfig["tenant1"]+"/ap-"+startupconfig["appprofile1"]+"/epg-"+iepg+"/rspathAtt-[topology/pod-1/paths-"+ileaf+"/pathep-[eth1/"+iport+"]]"
    tdn1 = "topology/pod-1/paths-"+ileaf+"/pathep-[eth1/"+iport+"]"
    url1 = "https://"+apic+"/api/node/mo/"+dn1+".json"
    encap = "vlan-"+ivlan
    payload1 = {
        "totalCount": "1",
        "imdata": [
            {
                "fvRsPathAtt": {
                    "attributes": {
                        "annotation": "",
                        "descr": "",
                        "dn": dn1,
                        "encap": encap,
                        "instrImedcy": "lazy",
                        "mode": "untagged",
                        "primaryEncap": "unknown",
                        "tDn": tdn1
                    }
                }
            }
        ]
    }
    
    headers1 = {
        "Cookie": f"APIC-Cookie={itoken}",
    }
    
    requests.packages.urllib3.disable_warnings()
    response1 = requests.post(url1,data=json.dumps(payload1),headers=headers1,verify=False)
    
    if (response1.status_code == 200):
        print("%s-eth1/%s: %s access mode OK\n"%(ileaf,iport,idescription))
    else:
        print(response1.text+"\n")
        print("%s-eth1/%s: %s epg static config fail\n"%(ileaf,iport,idescription))
        input("continue?\n")
####################################################################################

#ask for a token.  from ..\login.get_token import get_token
token = get_token()
if not token:
    print("get token fail")
    sys.exit()

#read accessrequest.csv, there are host access requests in it
f = open("accessrequest.csv")
line = f.readline()#first line ignore
line = f.readline()
#each line is a single request
while line:
    line=line.strip()
    line=line.replace(" ","")
    #vars to use later are read from accessrequest.csv
    linearry = line.split(',')
    hostname = linearry[0]
    mode = linearry[1]
    ip = linearry[2]
    leaf = linearry[3]
    port = linearry[4]
    line = f.readline()
    
    #if mode tag use access_tag(), if mode untag use access_untag()
    if mode == "tag":
        access_tag(token,leaf,port,hostname)
    elif mode == "untag":
        #use ipmask_transto_subnet() to trans "172.31.54.193/25" to "172.31.54.128/25"
        subnet = ipmask_transto_subnet(ip)
        #use "172.31.54.128/25" to get designed EPG
        #line in object subnet_get_epgvlan is like "172.31.54.128/25":"ExadataClient_BD,542"
        epgvlan = subnet_get_epgvlan[subnet]
        epgvlantmp = epgvlan.split(',')
        epg = epgvlantmp[0]
        vlan = epgvlantmp[1]
        #go config with proceed vars above
        access_untag(token,leaf,port,hostname,epg,vlan)

    
    
    
    
    
    
    
    
    #ma = re.match(r'^([1-9])([0-9]{2})\-([1-9])([0-9]{2})$',ip)
    
    
    
    
    
    
    