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

# mysql config
db_user = "tomato"
db_passwd = "D024Ad41d8cd98f00b204"
db_host = "114.215.186.147"
db_name = "tomato"
db_port = 443

# redis config
REDIS_CONFIG = {
  # "host":  "192.168.80.81",
  "host": "10.162.84.86",
  "port": 6379,
  # "password": "scut2017",
  "password": "",
  "db": 1
}

JWT_SECRET = "example"

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