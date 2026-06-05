import base64

def Gen_Key1(input_str):
    key1 = '1c6121ff'
    key2 = "da01cc19"

    # 核心加密: 两轮相同的逐字节加法+模运算
    def encrypt(text, key):
        return ''.join(
            chr((ord(t) + ord(k) - 64) % 95 + 32)
            for t, k in zip(text, key)
        )

    s3 = encrypt(input_str, key1)  # 第一轮
    s4 = encrypt(s3, key2)  # 第二轮

    return base64.b64encode(s4.encode()).decode()


def Gen_Key2(input_str):
    key1 = 'd7d242ae'
    str1=""
    for i,char in enumerate(input_str):
        it=ord(char)^ord(key1[i])
        str1 += chr(it)
    str2 = ""
    for i,char2 in enumerate(str1):
        a6=ord(char2)
        oI=int((49*(a6+50)-1568)/49)%95+32
        if(a6<32):oI=a6
        str2+=chr(oI)
    return base64.b64encode(str2.encode()).decode()

def Gen_Key3(input_str):
    key2 = "e3626980"
    # 第一轮
    s1 = ''.join(chr((ord(c) + 31) % 95 + 32) for c in input_str)
    # 第二轮
    s2 = ''.join(chr((ord(s1[i]) + ord(key2[i]) - 64) % 95 + 32)
                 for i in range(len(s1)))
    return base64.b64encode(s2.encode()).decode()
def Gen_Key4(input_str):
    str1=""
    str2=""
    for i,char1 in enumerate(input_str):
        e5=ord(char1)+28
        rg=-19 * e5 - -608
        ry = int(-rg / 19)
        ry %= 95
        ry += 32
        str1+=chr(ry)
    for i,char2 in enumerate(str1):
        ry = ord(char2)+17 - 32
        rf = ry % 95
        ry = rf
        ry += 32
        str2+=chr(ry)
    return base64.b64encode(str2.encode()).decode()
def Gen_Key5(input_str):
    key2="0fa4d950"
    str1=""
    str2=""
    tP=[]
    for i,char1 in enumerate(input_str):
        iM=ord(char1)+1
        ok=88*iM
        rJ=2816
        eA = int((ok - rJ) / 88)
        i6 = eA % 95
        eA = i6
        eA += 32
        tP.append(eA)
        str1+=chr(eA)
    for i in range(len(tP)):
        str2+=chr(tP[i]^ord(key2[i]))
    return base64.b64encode(str2.encode()).decode()

def Gen_Key6(input_str):
    str1=""
    str2=""
    key2="62d46263"
    for i,char1 in enumerate(input_str):
        a=ord(char1)
        b=-((a + 48) * 55)+1760
        c = int(-(b / 55))
        c=c%95
        c+=32
        str1+=chr(c)
    for i,char2 in enumerate(str1):
        lo=ord(key2[i])
        nE=-92 * lo+2944
        iE=-int(nE / 92)
        oV=ord(char2)+iE
        nw=oV-32
        nw %= 95
        nw += 32
        str2+=chr(nw)
    return base64.b64encode(str2.encode()).decode()
def Gen_Key7(input_str):
    str1=""
    str2=""
    for i,char1 in enumerate(input_str):
        a=ord(char1)
        b=  -((a + 72) * 79)
        c = b+2528
        d= -int(c / 79)
        e=d%95
        e+=32
        str1+=chr(e)
    for i,char2 in enumerate(str1):
        R=ord(char2)
        uU = R + 72
        rE = -26 * uU
        ej = rE + 832
        tf = -int(ej / 26)
        G = tf
        tf = (G % 95)
        tf += 32
        str2+=chr(tf)
    return base64.b64encode(str2.encode()).decode()

def Gen_Key8(input_str):
    str1=""
    str2=""
    key2="569b4d21"
    for i,char1 in enumerate(input_str):
        a=ord(char1)
        b=  (a+54)*81-2592
        c = int(b/81)
        e=c%95
        e+=32
        str1+=chr(e)
    for i, char2 in enumerate(str1):
        R1 = ord(char2)
        R2=ord(key2[i])
        he=R2-32
        i2=he+R1
        nf=i2-32
        nf %= 95
        nf += 32
        str2+=chr(nf)
    return base64.b64encode(str2.encode()).decode()
def Gen_Key9(input_str):
    key1="6b2f51d0"
    str1=""
    str2=""
    key2="7f44e4f8"
    for i,char1 in enumerate(input_str):
        a=ord(char1)
        b=ord(key1[i])
        c = b*69
        d = c - 2208
        e=int(d / 69)
        f=a+e
        g=f-32
        h = g % 95
        h+=32
        str1+=chr(h)
    for i,char2 in enumerate(str1):
        str2+=chr(ord(char2)^ord(key2[i%len(key2)]))
    return base64.b64encode(str2.encode()).decode()
def Gen_Key10(input_str):
    key1="1c6121ff"
    str1=""
    str2=""
    key2="63d279ac"
    for i,char1 in enumerate(input_str):
        a=ord(char1)
        b=ord(key1[i])
        c=b-32
        d=a+c-32
        e=d%95
        e += 32
        str1+=chr(e)
    for i,char2 in enumerate(str1):
        str2+=chr(ord(char2)^ord(key2[i%len(key2)]))
    return base64.b64encode(str2.encode()).decode()

def Gen_Key11(input_str):
    str1=""
    str2=""
    key2="acf5b5ad"
    for i,char1 in enumerate(input_str):
        a=ord(char1)
        b=a+85
        c=-66*b
        d=-int((c+2112) / 66)
        e=d%95
        e += 32
        str1+=chr(e)
    for i,char2 in enumerate(str1):
        R1 = ord(char2)
        R2 = ord(key2[i])
        he = R2 - 32
        i2 = he + R1
        nf = i2 - 32
        nf %= 95
        nf += 32
        str2 += chr(nf)
    return base64.b64encode(str2.encode()).decode()
def Gen_Key12(input_str):
    key1="ecfa6ec1"
    str1=""
    str2=""
    key2="9e5923e0"
    for i,char1 in enumerate(input_str):
        a=ord(char1)
        b=ord(key1[i])
        c=b-32
        d=a+c
        e=int((69 * d - 2208) / 69)
        f=e%95
        f += 32
        str1+=chr(f)
    for i,char2 in enumerate(str1):
        a = ord(char2)
        b = ord(key2[i])
        c = b - 32
        d = a + c
        e = -67 * d +2144
        f=-int(e/67)
        g = f % 95
        g += 32
        str2 += chr(g)
    return base64.b64encode(str2.encode()).decode()
def Gen_Key13(input_str):
    key1 = '1d81656a'
    str1=""
    for i,char in enumerate(input_str):
        it=ord(char)^ord(key1[i%len(key1)])
        str1 += chr(it)
    str2 = ""
    for i,char2 in enumerate(str1):
        a6=ord(char2)
        an=(a6-32)*37+60
        oI=a6+63
        c=int((-15 * oI +480)/-15)
        d = c % 95
        d += 32
        if(an>=60):
            str2 += chr(d)
        else:
            str2+=chr(a6)
    return base64.b64encode(str2.encode()).decode()

def Gen_Key14(input_str):
    key1="6a8be6df"
    str1=""
    str2=""
    key2="fb7ee4ae"
    for i,char1 in enumerate(input_str):
        a=ord(char1)
        b=ord(key1[i])
        c=  b-32+a
        d = 5 * c
        e=d-160
        f=int(e/5)
        g=f%95
        g+=32
        str1+=chr(g)
    for i, char2 in enumerate(str1):
        R1 = ord(char2)
        str2+=chr(R1^ord(key2[i%len(key2)]))
    return base64.b64encode(str2.encode()).decode()

def Gen_Key(input_str,version):
    if version == "053":
        return Gen_Key1(input_str)
    elif version == "054":
        return Gen_Key2(input_str)
    elif version == "055":
        return Gen_Key3(input_str)
    elif version == "056":
        return Gen_Key4(input_str)
    elif version == "057":
        return Gen_Key5(input_str)
    elif version == "058":
        return Gen_Key6(input_str)
    elif version == "059":
        return Gen_Key7(input_str)
    elif version == "060":
        return Gen_Key8(input_str)
    elif version == "061":
        return Gen_Key9(input_str)
    elif version == "062":
        return Gen_Key10(input_str)
    elif version == "063":
        return Gen_Key11(input_str)
    elif version == "064":
        return Gen_Key12(input_str)
    elif version == "065":
        return Gen_Key13(input_str)
    elif version == "066":
        return Gen_Key14(input_str)