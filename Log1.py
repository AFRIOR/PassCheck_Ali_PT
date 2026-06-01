import requests
from Utils import *
def Get_DeviceConfig(Origin,UserAgent):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": Origin,
        "Referer": Origin+"/",
        "User-Agent": UserAgent
    }
    url = "https://cloudauth-device-dualstack.cn-shanghai.aliyuncs.com/"
    data = {
        "AccessKeyId": "LTAI5tGjnK9uu9GbT9GQw72p",
        "Version": "2020-10-15",
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "Format": "JSON",
        "Action": "Log1",
        "Data": Gen_Enc_Data(Dec_parmam("FqJB6iRNVYdEGpwb","8KmHIQsc5+LZJA7uYex3WaHdkjgCtS6epbG/bc9xss0="),"ab034ec0643f91399eb33e062dc7fae1#W#V0z3lM83c/TjjZu6HWeg96NVWTsvgiYD2c0CYNq7AAJoR/lIaPMTto0iCFQCGNlUggHhY4unb7T2y7BWhcdf3A==#W20220202#CLOUD#"),
        "SignatureNonce": Gen_SignatureNonce(),
    }
    signature = Gen_Signature("fpOKzILEajkqgSpr9VvU98FwAgIRcX&", data)
    data.update({
        "Signature": signature
    })
    try:
        res_json = requests.post(url, headers=headers, data=data).json()
        return res_json["ResultObject"]["DeviceConfig"]
    except Exception as e:
        print(f"Error:{e}")
        return None