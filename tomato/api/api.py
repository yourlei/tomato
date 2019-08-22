# coding: utf-8
# api入口, 统一处理api请求装饰器
from tomato.app import app
from tomato.utils.errCode import ErrCode
from tomato.utils.utils  import output_json
from jsonschema.exceptions import ValidationError

@app.errorhandler(ValidationError)
def handle_bad_request(e):
    """处理全局异常参数请求"""
    return output_json(code=ErrCode.ERR_PARAMS), 400

@app.errorhandler(Exception)
def handle_inner_error(e):
    return output_json(code=ErrCode.INNERERR), 500
