import hashlib


def MD5(str):
    md5 = hashlib.md5()
    md5.update(str.encode())
    return md5.hexdigest()
def Gen_AlgoPoint(t):
    key1="XK37ML9"
    str=""
    for i,x in enumerate(t):
        u=ord(x)+37
        b=u + i ^ ord(key1[i%7])
        str+=chr(b)
    print(MD5(str)[:5])
    return MD5(str)[:5]
Gen_AlgoPoint("N2YzZmZlaA==")