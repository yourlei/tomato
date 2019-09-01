# 服务
HOST = "0.0.0.0"

# 服务端口
PORT = "8095"

# 解决响应中文乱码
JSON_AS_ASCII = False

# 启用调试模式
DEBUG = True # False

# flask密钥
SECRET_KEY = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'

"""数据库配置"""
db_user = "tomato"
db_passwd = "tomato"
db_host = "127.0.0.1"
db_name = "tomato"
db_port = 3306

"""redis配置"""
REDIS_CONFIG = {
  "host":  "localhost",
  "port": 6379,
  "password": "",
  "db": 1
}

JWT_SECRET = "tomato"

EXPIRED_TIME = 1 * 30 * 60
# 日志记录等级
LOGGING_LEVEL = 'INFO'

# mysql 
class DBConfig:
  """数据库配置"""
  URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (db_user, db_passwd, db_host, db_port, db_name)
  TB_PREFIX = 'tomato_'  # 表名前缀
  DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# test request header
TestConfig = {
  "host": "http://localhost:8095",
  "header": {}
}

api_version = "/api/v1"
STATICPATH = "static/captcha/"