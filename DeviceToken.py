import time,random
from Utils import *
from v78d98s import Gen_Key
def FindIpbyVersion(Version_Code):
    if Version_Code=="069":return "111.1.156.204"
    if Version_Code=="084":return "123.152.213.19"
    else:return "123.152.213.20"
def Gen_DeviceToken(SessionId,AES_Key,Version_Code,timestamps:list,GatherCost):
    key=Gen_Key(SessionId[-8:],Version_Code)
    ip=FindIpbyVersion(Version_Code=Version_Code)
    env_data=f"W.10051#####Linux aarch64#WeChat#8.0.70.3060#############8#{key}###########b5edd5be394adaca15866d8a285a8847##8##Android#14#####{ip}#10-0|11-113|20-114|23-295|30-297|40-311|41-2814|70-2815|71-813|80-813#true###889*400##5##################saf-captcha#0###AcXaauXsImO6Ez2H9johSbbpMNBb0Co37dw5mvAz#{timestamps[0]}#HHz3uOBqluzi1Z1wFMQlXI3Ph6kHWWT89r1t4HUlMx#{timestamps[1]}#mobile#false##9d4568c009d203ab10e33ea9953a0264#########{timestamps[2]}#MCMwIzAjMCMwIzAjMCMwIzAjMCMwIzAjMCMwIzAjMCMwIzAjMCMxIzEjMCMxMTExMTEwMDExMTExMTExMTExMTExMTExMQ==#1#1#true##################-1#######################"
    Enc_data=AES_Encrypt(env_data, AES_Key, "d35db7e39ebbf3d001083105")
    data_md5=Gen_Md5("WEB#"+SessionId+"#"+Enc_data+f"#{GatherCost}#"+"daye,raolewoba!")
    t_data="WEB#"+SessionId+"#"+Enc_data+f"#{GatherCost}#"+data_md5
    return base64.b64encode(t_data.encode()).decode()