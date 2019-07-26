# coding: utf-8
# api入口, 统一处理api请求装饰器

from tomato.app import app

@app.handle_exception
def handle_error():
    pass

@app.before_request
def token_auth():
    pass
