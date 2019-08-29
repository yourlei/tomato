# coding: utf-8
# 应用入口程序

import logging
from flask import Flask
from flask_cors import CORS
from tomato.setting import DBConfig
from tomato.utils.journal import setup_logging

"""创建Flask实例"""
app = Flask(__name__, static_folder='../static')
# 加载配置
app.config.from_pyfile('setting.py')
# 支持跨域
CORS(app, supports_credentials=True)

app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DBConfig.URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 上传文件大小限制: 25M
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024

# fixed: MySQL server has gone away
app.config['SQLALCHEMY_POOL_SIZE'] = 128  # 线程池大小
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 90  # 超时时间
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3  # 空闲连接自动回收时间
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 128  # 控制在连接池达到最大值后可以创建的连接数。

# 配置日志
setup_logging(app.config["LOGGING_LEVEL"])
# handler = logging.FileHandler("my.log", encoding="UTF-8")
# handler.setLevel(logging.DEBUG)
# logging_format = logging.Formatter(
#     '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
# handler.setFormatter(logging_format)
# app.logger.addHandler(handler)

if __name__ == "__main__":
    print(app.config)