import requests
from Utils import *
import json
AES_KEY_FINAL = "a549a55c60a39aa0"
def GenLog3Data(AES_KEY,SessionId):
    timestamp = str(int(datetime.now().timestamp() * 1000))
    Data30= AES_Encrypt("W.10051#saf-captcha", AES_KEY, "d35db7e39ebbf3d001083105")
    Data31 = AES_Encrypt("saf-captcha", AES_KEY, "d35db7e39ebbf3d001083105")
    Data32 = AES_Encrypt("W.10051", AES_KEY, "d35db7e39ebbf3d001083105")
    Data33 = AES_Encrypt(str(int(datetime.now().timestamp()*1000)), AES_KEY, "d35db7e39ebbf3d001083105")
    str1 = json.dumps(
        {"mousemove": [], "mouseclick": [], "keyup": [], "scrollTop": [], "scrollLeft": [], "clientType": "mobile",
         "startTime": int(datetime.now().timestamp() * 1000) + 5000,
         "timestamp": str(int(datetime.now().timestamp() * 1000))}, separators=(',', ':'), ensure_ascii=False)
    Data3_4 = AES_Encrypt(str1, AES_KEY, "d35db7e39ebbf3d001083105")
    Data3_5 = AES_Encrypt(str(int(datetime.now().timestamp() * 1000)), AES_KEY, "d35db7e39ebbf3d001083105")
    _Data3_p1=base64.b64encode((SessionId+"##"+Data31+"#"+Data32+"##"+Data33).encode()).decode()
    _Data3_p2 = base64.b64encode((SessionId + "#" + Data3_4 + "#" + Data31 +"#"+ Data32 + "##" + Data3_5).encode()).decode()
    _Data3_p0 = base64.b64encode(("511#"+_Data3_p1+"-504#"+_Data3_p2).encode()).decode()
    Data="ab034ec0643f91399eb33e062dc7fae1#W#"+Data30+"#W20220202#CLOUD##"+_Data3_p0
    return AES_Encrypt(Data,AES_KEY_FINAL,"d35db7e39ebbf3d001083105")

def UploadLog3(AES_Key,SessionId,Origin,UA):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": Origin,
        "Referer": Origin+"/",
        "User-Agent": UA,
    }
    url = "https://cloudauth-device-dualstack.cn-shanghai.aliyuncs.com/"
    data = {
        "AccessKeyId": "LTAI5tGjnK9uu9GbT9GQw72p",
        "Version": "2020-10-15",
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "Format": "JSON",
        "Action": "Log3",
        "Data": GenLog3Data(AES_Key, SessionId),
        "SignatureNonce": Gen_SignatureNonce(),
    }
    signature = Gen_Signature("fpOKzILEajkqgSpr9VvU98FwAgIRcX&", data)
    data.update({
        "Signature": signature
    })
    try:
        res_json = requests.post(url, headers=headers, data=data).json()
        print(res_json)
        return res_json["ResultObject"]
    except Exception as e:
        print(f"Error:{e}")
        return None