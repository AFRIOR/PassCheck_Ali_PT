import json

import requests
import time
from Utils import *

def _UploadLog(Origin,UA,SID,CID):
    timestamp=int(round(time.time()*1000))
    Log={"sId":SID,"pfx":"psgmtn","mInit":{"t":timestamp,"s":True,"msg":"INIT_SUCCESS","rt":3068},"hst":"captcha-open.aliyuncs.com","cId":CID,"js":{"t":timestamp+166,"s":True,"msg":"DYNAMICJS_LOADED","rt":155},"pImg":{"t":timestamp+227,"s":True,"msg":"IMAGE_LOADED","rt":16},"rt":3344}
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "referer": "http://"+Origin+"/",
        "user-agent": UA,
        "x-requested-with": "com.tencent.mm"
    }
    url = "https://upload.captcha-open.aliyuncs.com/"
    data = {
        "AccessKeyId": "LTAI5tSEBwYMwVKAQGpxmvTd",
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "Format": "JSON",
        "Timestamp": Get_UTC_Timestamp(),
        "Version": "2023-03-05",
        "Action": "UploadLog",
        "log": json.dumps(Log,ensure_ascii=False,separators=(',',':')),
        "SignatureNonce": Gen_SignatureNonce(),
    }
    signature = Gen_Signature("YSKfst7GaVkXwZYvVihJsKF9r89koz&", data)
    data.update({
        "Signature": signature
    })
    try:
        res_json = requests.post(url, headers=headers, data=data).json()
        print(res_json)
        return res_json["Success"]
    except Exception as e:
        print(f"Error:{e}")
        return None