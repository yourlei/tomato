# coding: utf-8
# api入口, 统一处理api请求装饰器
import re
import jwt
import traceback
from flask import request
from tomato.app import app
from tomato.utils.errCode import ErrCode
from tomato.utils.utils  import output_json
from jsonschema.exceptions import ValidationError

@app.route("/", methods=["GET"])
def home():
    return "welcome to tomato"

@app.errorhandler(ValidationError)
def handle_bad_request(e):
    """处理全局异常参数请求"""
    if app.config.get("DEBUG"):
        print(traceback.format_exc())
    return output_json(code=ErrCode.ERR_PARAMS), 400

@app.errorhandler(Exception)
def handle_inner_error(e):
    if app.config.get("DEBUG"):
        print(traceback.format_exc())
    return output_json(code=ErrCode.INNERERR), 200

@app.before_request
def require_token():
    """验证token"""
    pathname = request.path
    # 权限受控接口
    if not app.config["DEBUG"]:
        if -1 != pathname.find("admin"):
            headers = request.headers
            origin = headers.get("Origin")
            token = headers.get("Token")
            
            if token is None:
                return output_json(code=ErrCode.HEADER_ERR)
            # 验证token
            try:
                payload = jwt.decode(token, app.config["JWT_SECRET"], algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return output_json(code=ErrCode.NO_AUTH), 401
            except jwt.InvalidTokenError:
                return output_json(code=ErrCode.NO_AUTH), 401