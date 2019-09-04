# coding: utf-8
# 登录模块API
from flask import request
from flask import Blueprint
from jsonschema import validate
from tomato.utils.errCode import ErrCode
from tomato.utils.utils import output_json
from tomato.server.login import LoginService

login_action = Blueprint("login_action", __name__)
# 登录请求体参数验证
login_schema = {
    "type": "object",
    "properties": {
        "account": {
            "type": "string"
        },
        "passwd": {
            "type": "string",
            "minLength": 8
        }
    },
    "required": ["account", "passwd"]
}

@login_action.route("/login", methods=["POST"])
def login():
    """登录接口"""
    body = request.json
    validate(body, login_schema)

    login_handler = LoginService()
    code, res = login_handler.login(**body)

    return output_json(code=code) if code else output_json(data=res)
