# coding: utf-8
# 文章与分类模块
from flask import json
from flask import request
from flask import Blueprint
from jsonschema import validate
from tomato.utils.errCode import ErrCode
from tomato.utils.utils import output_json
from tomato.server.category_relation import CategoryRelation

category_relation_action = Blueprint("category_relation_action", __name__)

relation_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "aid": {
            "type": "string" 
        }
    },
    "required": ["name", "aid"]
}

@category_relation_action.route("/category/relation", methods=["POST","DELETE"])
def create():
    body = request.json
    
    validate(body, schema=relation_schema)
    handler = CategoryRelation()
    if request.method == "POST":
        res = handler.bindCategory(body.get("name"), body.get("aid"))
    else:
        res = handler.unbindCategory(body.get("name"), body.get("aid"))
    return res