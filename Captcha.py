import os
import random
import re
import time

from Init import InitCaptcha
from Log1 import Get_DeviceConfig
from Log2 import UploadLog2
from Log3 import UploadLog3
from UploadLog import _UploadLog
from DeviceToken import Gen_DeviceToken
from Track import GenCrack_Data,Cipher_Init
from Utils import *
from captcha_recognizer.slider import Slider
import requests
import cv2
import json
slider = Slider()
def Compute_Slide(res_json):
    header_url = "https://static-captcha.aliyuncs.com/"
    backImg_Url = header_url + res_json["Image"]
    PuzzleImage_Url = header_url + res_json["PuzzleImage"]
    target_bytes = requests.get(PuzzleImage_Url).content
    background_bytes = requests.get(backImg_Url).content
    with open(os.path.dirname(os.path.abspath(__file__))+"/temp/temp.png", "wb") as f:
        f.write(background_bytes)
        f.close()
    box, confidence = slider.identify(source=os.path.dirname(os.path.abspath(__file__))+'/temp/temp.png')
    im = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/temp/temp.png")
    im = cv2.rectangle(im, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color=(0, 0, 255), thickness=2)
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/temp/result.jpg", im)
    print(f'缺口坐标: {box}')
    print(f'可信度: {confidence}')
    return {
        "xpos": int(box[0])+1 if box[0]-int(box[0]) >= 0.9 else int(box[0]),
        "pos_total":box,
        "confidence":confidence,
    }
def PassCaptcha(SID,Origin,UA):
    Cipher_Init()
    Params=Parse_Params("87f879f135f27da7", Get_DeviceConfig(Origin,UA))
    # print(Params)
    version=Params["version"]
    if re.match(r".*?/feilin([0-9]+)",version):
        version_code=re.match(r".*?/feilin([0-9]+)",version).group(1)
        res_json =InitCaptcha(Origin, UA,SID)
    print(f"当前Feilin版本:{version_code}")
    if version_code not in ["053","054","055","056","057","058","059","060","061","062","063","064","065"]:return False
    t=int(Params["timestamp"])
    res2,GatherCost,timestamp1,timestamp2=UploadLog2(AES_Key=Params["key"],SessionId=Params["sessionId"],Origin=Origin,UA=UA,version=version,Version_Code=version_code,Config_Time=t)
    # res3 = UploadLog3(AES_Key=Params["key"], SessionId=Params["sessionId"], Origin=Origin, UA=UA)
    CertifyId = res_json["CertifyId"]
    _UploadLog(Origin,UA,SID,CertifyId)
    result=Compute_Slide(res_json)
    x_pos=result["xpos"]
    TrackData=GenCrack_Data(x_pos)
    captchaVerifyParam={
        "sceneId": SID,
        "certifyId": CertifyId,
        "deviceToken":Gen_DeviceToken(AES_Key=Params["key"], SessionId=Params["sessionId"],Version_Code=version_code,timestamps=[timestamp1,timestamp2,t],GatherCost=GatherCost),
        "data": TrackData
    }
    return json.dumps(captchaVerifyParam, separators=(',', ':'), ensure_ascii=False)
