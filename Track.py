import json
import os
import random
import time
import base64
import math
import zlib
import base64
import execjs
from TrackV2 import _create_track_list
ctx = None
def Cipher_Init():
    global ctx
    with open(os.path.dirname(os.path.abspath(__file__))+"/Encrypt.js", "r") as f:
        ctx=execjs.compile(f.read())
        f.close()
def GenCrack_Data(xpos):
    data1=_create_track_list(73,230,xpos,int(time.time()*1000))
    Hash = ctx.call("GenHash", [
        data1,
        "0000"
    ])
    data2=Hash+data1
    data2_b64=base64.b64encode(zlib.compress(data2.encode())).decode()
    result2 = ctx.call("GenEnc", [
        data2_b64,
        "3e627e1b4c63f913"
    ])
    return result2