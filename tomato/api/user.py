# coding: utf-8
# 用户管理

from flask import request
from flask import Blueprint
from jsonschema import validate

from tomato.database.model import User
from tomato.server.user import UserService
from tomato.utils.utils import output_json
from tomato.utils.errCode import ErrCode

user_action = Blueprint("user_action", __name__)

passwd_schema = {
    "type": "object",
    "properties": {
        "old_passwd": {
            "type": "string",
            "minLength": 6
        },
        "new_passwd": {
            "type": "string",
            "minLength": 6
        }
    },
    "required": ["old_passwd", "new_passwd"]
}

create_user_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 3
        },
        "email": {
            "type": "string",
            "minLength": 5
        },
        "password": {
            "type": "string",
            "minLength": 8
        },
        "role_id": {
            "type": "string",
            "length": 16
        }
    },
    "required": ["name", "email", "password", "role_id"]
}

@user_action.route("/user", methods=["POST"])
def create():
    """创建用户"""
    body = request.json

    validate(body, create_user_schema)
    user_handler = UserService()
    code = user_handler.create(User(
        name=body["name"],
        email=body["email"],
        password=body["password"],
        role_id=body["role_id"]
    ))
    
    return output_json(code=code)

@user_action.route("/user/<string:user_id>", methods=["put"])
def update(user_id):
    """编辑用户信息"""
    if user_id is None:
        return output_json(code=ErrCode.ERR_PARAMS)

    body = request.json
    allow_field = ["name", "email", "role_id"]
    for key in body.keys():
        if key not in allow_field:
            return output_json(code=ErrCode.ERR_PARAMS)

    user_handler = UserService()
    code = user_handler.update(user_id, body)
    
    return output_json(code=code)

@user_action.route("/passwd/<string:user_id>", methods=["PUT"])
def changePasswd(user_id):
    """修改密码"""
    if user_id is None:
        return output_json(code=ErrCode.ERR_PARAMS)
    
    body = request.json
    validate(body, passwd_schema)
    user_handler = UserService()
    code = user_handler.changePasswd(user_id, **body)
    
    return output_json(code=code)
