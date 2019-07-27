# coding: utf-8
# 用户管理

from flask import request
from flask import Blueprint
from jsonschema import validate
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

@user_action.route("/passwd/<string:user_id>", methods=["PUT"])
def changePasswd(user_id):
    body = request.json

    if user_id is None:
        return output_json(code=ErrCode.ERR_PARAMS)
    
    validate(body, passwd_schema)
    user_handler = UserService()
    res = user_handler.changePasswd(user_id, **body)
    return res
