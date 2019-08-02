# coding: utf-8
# 文章管理API

from flask import json
from flask import Blueprint
from flask import request
from jsonschema import validate

from tomato.database.model import Article
from tomato.utils.errCode import ErrCode
from tomato.utils.utils import output_json
from tomato.server.article import ArticleService

article_action = Blueprint("article_action", __name__)

create_schema = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "minLength": 2
        },
        "author": {
            "type": "string",
            "minLength": 1
        },
        "content": {
            "type": "string"
        },
        "cid": {
            "type": "string",
            "minLength": 16
        }
    },
    "required": ["title", "author", "content", "uid"]
}

@article_action.route("/article", methods=["POST"])
def create():
    body = request.json

    validate(body, create_schema)
    handler = ArticleService()
    res = handler.create(Article(
        title=body["title"],
        author=body["author"],
        content=body["content"],
        cid=body["cid"]
    ))

    return res

@article_action.route("/article", methods=["GET"])
def list():
    query = request.args.get("query")

    try:
        query = json.loads(query)
    except:
        return output_json(code=ErrCode.ERR_PARAMS)

    where = query.get("where") or {}
    offset = query.get("offset") or 0
    limit = query.get("limit") or 15
    handler = ArticleService()
    res = handler.list(where, offset, limit)

    return res