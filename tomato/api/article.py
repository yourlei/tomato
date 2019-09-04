# coding: utf-8
# 文章管理API
from flask import json
from flask import request
from flask import Blueprint
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
        "author_id": {
            "type": "string",
            "minLength": 16
        },
        "content": {
            "type": "string"
        },
        "status": {
            "type": "integer"
        }
    },
    "required": ["title", "author_id", "content"]
}
@article_action.route("/article", methods=["POST"])
def create():
    """创建文章"""
    body = request.json

    validate(body, create_schema)
    handler = ArticleService()
    res = handler.create(Article(
        title=body["title"],
        author_id=body["author_id"],
        content=body["content"],
        status=body["status"]
    ))

    return output_json(data=res)

@article_action.route("/article", methods=["GET"])
def list():
    """文章列表"""
    query = request.args.get("query")

    try:
        query = json.loads(query)
    except:
        return output_json(code=ErrCode.ERR_PARAMS)

    where = query.get("where") or {}
    offset = query.get("offset") or 0
    limit = query.get("limit") or 15
    handler = ArticleService()
    data, count = handler.list(where, offset, limit)

    return output_json(data=data, total=count)

@article_action.route("/article/<string:id>", methods=["GET"])
def show(id):
    """文章详情"""
    if id is None:
        return output_json(code=ErrCode.ERR_PARAMS)
    handler = ArticleService()
    
    flag, data = handler.show(id)

    return output_json(data=data) if flag else output_json(code=ErrCode.NO_DATA)


@article_action.route("/article/<string:id>", methods=["PUT"])
def update(id):
    """编辑文章"""
    if id is None:
        return output_json(code=ErrCode.ERR_PARAMS)
    
    body = request.json
    if body is None:
        return output_json(code=ErrCode.ERR_PARAMS)

    allowField = ["title", "status", "content"]
    # 检查更新字段
    for key in body.keys():
        if key not in allowField:
            return output_json(code=ErrCode.ERR_PARAMS)

    handler = ArticleService()
    res = handler.update(id, body)

    return output_json(code=0) if res else output_json(code=ErrCode.NO_DATA)

@article_action.route("/article/<string:id>", methods=["DELETE"])
def delArticle(id):
    """删除文章"""
    if id is None:
        return output_json(code=ErrCode.ERR_PARAMS)
    handler = ArticleService()
    res = handler.destory(id)

    return output_json(code=0) if res else output_json(code=ErrCode.NO_DATA)
    