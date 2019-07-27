# coding: utf-8
# 注册路由
# 服务启动函数
from tomato.api.api import app
from tomato.setting import api_version
from tomato.api.user import user_action
from tomato.api.login import login_action

def handle_url_prefix(url: str):
  return api_version + url

app.register_blueprint(login_action, url_prefix=handle_url_prefix("/admin"))
app.register_blueprint(user_action, url_prefix=handle_url_prefix("/admin"))

def run(debug=False, port=8095, host="0.0.0.0"):
  """ 启动服务 """
  app.run(port=port, debug=debug, host=host)