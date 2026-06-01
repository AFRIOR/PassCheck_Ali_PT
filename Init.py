from Utils import *
import requests
def InitCaptcha(Origin,useragent,SID):
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": Origin,
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": Origin+"/",
        "user-agent": useragent
    }
    url = "https://psgmtn.captcha-open.aliyuncs.com/"
    data = {
        "AccessKeyId": "LTAI5tSEBwYMwVKAQGpxmvTd",
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "Format": "JSON",
        "Timestamp": Get_UTC_Timestamp(),
        "Version": "2023-03-05",
        "Action": "InitCaptcha",
        "SceneId": SID,
        "Language": "cn",
        "Mode": "popup",
        "SignatureNonce": Gen_SignatureNonce(),
    }
    signature=Gen_Signature("YSKfst7GaVkXwZYvVihJsKF9r89koz&",data)
    data.update({
        "Signature":signature
    })
    try:
        res_json = requests.post(url, headers=headers, data=data).json()
        return res_json
    except Exception as e:
        print(f"Error:{e}")
        return None

