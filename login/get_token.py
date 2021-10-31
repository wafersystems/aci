import requests
import json
import sys 
sys.path.append("..") 
from login_info import apic
from login_info import usrpwd

#get token method
def get_token():
    url = "https://" + apic + "/api/aaaLogin.json"
    
    payload = usrpwd
    
    headers = {
        "Content-type" : "application/json"
    }
    
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url,data=json.dumps(payload),headers=headers,verify=False).json()
    
    token = response['imdata'][0]['aaaLogin']['attributes']['token']
    return token
    
def main():
    token = get_token()
    print ("Token: " + token)
    
if __name__ == "__main__":
    main()
