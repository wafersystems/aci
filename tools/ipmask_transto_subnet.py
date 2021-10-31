import re

#this method is used to recognize the subnet of an IP address   ex. 172.31.56.193/25 return 172.31.56.128/25
def ipmask_transto_subnet(iptmp):
    #devide ip read from request.csv file  ex. 172.31.56.100/25  172.31.56.100 and 25
    ma = re.match(r'(.*)/([0-9]+)',iptmp)
    ip = ma.group(1)
    ipblock = ip.split('.')
    #check mask is between /16 and /24  or above /24, (this site dont need mask below /16)
    fo = int(ma.group(2))-24
    th = int(ma.group(2))-16
    subnetlast=''
    if fo >= 0:
        subnetlast = int(ipblock[3])-(int(ipblock[3])%(2**(8-fo)))
        subnetlast = str(subnetlast)
        subnet = ipblock[0]+'.'+ipblock[1]+'.'+ipblock[2]+'.'+subnetlast+'/'+ma.group(2)
    elif th >= 0:
        subnetlast = int(ipblock[2])-(int(ipblock[2])%(2**(8-th)))
        subnetlast = str(subnetlast)
        subnet = ipblock[0]+'.'+ipblock[1]+'.'+subnetlast+'.0/'+ma.group(2)
    else:
        print("ip/mask format wrong  ex.10.1.1.0/24\n")
        return()
    return(subnet)
