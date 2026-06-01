import base64
import random
import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from datetime import datetime, timezone
import hmac
import hashlib
def Parse_Params(key:str,Encrypt_DeviceConfig:str)->dict:
    M={}
    Plain=Dec_parmam(key,Encrypt_DeviceConfig)
    config=Plain.split("#")
    if len(config)>=4:
        M["ip"]=config[8]
        M["globalVariable"]=base64.b64decode(config[6]).decode()
        M["version"]=config[3]
        M["switch"]=int(base64.b64decode(config[1]).decode())
        M["key"] = base64.b64decode(config[0]).decode()
        M["pluginElements"]=base64.b64decode(config[4]).decode()
        M["timestamp"]=config[7]
        M["pluginResource"]=base64.b64decode(config[5]).decode()
        M["sessionId"]=config[2]
        return M
def Gen_SignatureNonce():
    e = ""
    for t in range(32):
        r = int(16 * random.random())
        if t in [8, 12, 16, 20]:
            e += "-"
        if t == 12:
            r = 4          # UUID 版本号
        elif t == 16:
            r = (3 & r) | 8  # 变体标识 (10xx)
        e += hex(r)[2:]
    return e
def Gen_Md5(data):
    data_block=data.encode('utf-8')
    MD5=hashlib.md5()
    MD5.update(data_block)
    return  MD5.hexdigest()
def Get_UTC_Timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def AES_Encrypt(origintext,key,iv):
    key=key.encode('utf-8')
    iv= base64.b64encode(bytes.fromhex(iv))
    Cipher = AES.new(key=key,mode=AES.MODE_CBC,iv=iv)
    ciphertext=base64.b64encode(Cipher.encrypt(pad(origintext.encode('utf-8'),block_size=AES.block_size,style="pkcs7"))).decode('utf-8')
    return ciphertext
def AES_Decrypt(ciphertext,key,iv):
    key=key.encode('utf-8')
    iv= base64.b64encode(bytes.fromhex(iv))
    Cipher = AES.new(key=key,mode=AES.MODE_CBC,iv=iv)
    cipherorigin=unpad(Cipher.decrypt(base64.b64decode(ciphertext)),block_size=AES.block_size,style="pkcs7").decode('utf-8')
    return cipherorigin
def Dec_parmam(param1, param2):
    if param2 is None:
        return  None
    elif param2 is None or len(param1)!=16 or len(param2)<=0:
        return None
    else:
        return AES_Decrypt(param2,param1,"d35db7e39ebbf3d001083105")
def Gen_Enc_Data(param1,param2):
    if param2 is None:
        return  None
    elif param2 is None or len(param1)!=16 or len(param2)<=0:
        return None
    else:
        return AES_Encrypt(param2,param1,"d35db7e39ebbf3d001083105")
def Gen_Signature(key,data):
    if "Signature"in data:del data["Signature"]
    keys=list(data.keys())
    s1=""
    for i,k in enumerate(sorted(keys)):
        if i==(len(keys)-1):s1+=k+"="+data[k]
        else:s1+=k+"="+data[k]+"&"
    s2="POST&%2F&"+s1.replace("=","%3D").replace("&","%26").replace("+","%252B").replace("/","%252F").replace(":","%253A").replace("%3D%3D%26","%253D%253D%26").replace("%3D%26","%253D%26").replace(
        "{","%257B"
    ).replace("}","%257D").replace("\"","%2522").replace(",","%252C")
    cipher=hmac.new(key.encode(), s2.encode(), hashlib.sha1)
    return base64.b64encode(bytes.fromhex(cipher.hexdigest())).decode('utf-8')