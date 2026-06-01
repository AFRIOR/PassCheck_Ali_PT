from flask import Flask, jsonify, request
from Captcha  import *

app=Flask(__name__)
@app.route("/")
def index():
    return """
    <h1>Server Status Ok</h1>
    """
@app.route("/PassCheck",methods=["POST"])
def PassCheck():
    req_json=request.json
    origin=req_json["origin"]
    ua=req_json["ua"]
    sid=req_json["sid"]
    res=PassCaptcha(sid,origin,ua)
    if res:
        return jsonify({"code":200,"Msg":"PassCheck success","captchaVerifyParam":res})
    else:
        return jsonify({"code": 400, "Msg": "PassCheck Fail"})

app.run(host="0.0.0.0",port=5000,debug=True)

