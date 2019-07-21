# coding: utf-8
from tomato.server.api import app
from tomato.setting import api_version

def handle_url_prefix(url: str):
  return api_version + url

# app.register_blueprint(map_action, url_prefix=handle_url_prefix("/map"))

def run(debug=False, port=8095, host="0.0.0.0"):
  """ 启动服务 """
  app.run(port=port, debug=debug, host=host)