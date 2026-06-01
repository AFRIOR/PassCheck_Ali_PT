import requests
from Utils import *
from DeviceFingerprint import GenDeviceFingerprint
from v78d98s import Gen_Key
AES_KEY_FINAL = "a549a55c60a39aa0"
def GenData(AES_KEY,SessionId,Origin,version,Version_Code,Config_Time):
    key = Gen_Key(SessionId[-8:],Version_Code)
    DeviceFingerPrint,GatherCost,timestamp,timestamp2=GenDeviceFingerprint(key,Origin,Config_Time,version,Version_Code)
    # print(DeviceFingerPrint)
    Data1=AES_Encrypt("W.10051#saf-captcha#1qykdymp",AES_KEY,"d35db7e39ebbf3d001083105")
    Data22=AES_Encrypt(DeviceFingerPrint,AES_KEY,"d35db7e39ebbf3d001083105")
    Data23=AES_Encrypt("saf-captcha",AES_KEY,"d35db7e39ebbf3d001083105")
    Data24=AES_Encrypt("W.10051",AES_KEY,"d35db7e39ebbf3d001083105")
    Data25=AES_Encrypt(str(timestamp2+4),AES_KEY,"d35db7e39ebbf3d001083105")
    Data2_1=SessionId+"#"+Data22+"#"+Data23+"#"+Data24+"##"+Data25
    Data2=base64.b64encode(Data2_1.encode()).decode()
    Data="ab034ec0643f91399eb33e062dc7fae1#W#"+Data1+f"#W20220202#CLOUD#{GatherCost}#501#"+Data2
    # print(AES_Encrypt(Data,AES_KEY_FINAL,"d35db7e39ebbf3d001083105"),GatherCost,timestamp,timestamp2)
    return AES_Encrypt(Data,AES_KEY_FINAL,"d35db7e39ebbf3d001083105"),GatherCost,timestamp,timestamp2


def UploadLog2(AES_Key,SessionId,Origin,UA,version,Version_Code,Config_Time):
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": Origin,
        "Referer": Origin+"/",
        "User-Agent": UA,
    }
    Data,GatherCost, timestamp, timestamp2= GenData(AES_Key, SessionId,Origin,version,Version_Code,Config_Time)
    url = "https://cloudauth-device-dualstack.cn-shanghai.aliyuncs.com/"
    data = {
        "AccessKeyId": "LTAI5tGjnK9uu9GbT9GQw72p",
        "Version": "2020-10-15",
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "Format": "JSON",
        "Action": "Log2",
        "Data": Data,
        "SignatureNonce": Gen_SignatureNonce(),
    }
    signature = Gen_Signature("fpOKzILEajkqgSpr9VvU98FwAgIRcX&", data)
    data.update({
        "Signature": signature
    })
    try:
        res_json = requests.post(url, headers=headers, data=data).json()
        print(res_json)
        return res_json["ResultObject"],GatherCost, timestamp, timestamp2
    except Exception as e:
        print(f"Error:{e}")
        return None
if __name__ == "__main__":
    print(Gen_Key("117d4002","056"))
    print(GenData("36c54647c7842464","ab034ec0643f91399eb33e062dc7fae1-h-1779820783119-50af0aaf47ce491d9e4b0e75117d4002","","","",5))
