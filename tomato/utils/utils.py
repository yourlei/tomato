# coding: utf-8

import bcrypt
from flask import jsonify
from uuid import uuid1 as uuid
from hashlib import md5 as md5_lib
from calendar import timegm
from datetime import datetime

from tomato.utils.errCode import ErrMap

# 数据软删除标识
DELETED_AT = ' 0000-01-01 00:00:00'

def output_json(data=None, total=None, code=0, msg=None):
  """以json结构返回数据"""
  if msg is None and ErrMap.get(code):
    msg = ErrMap.get(code)
  else:
    msg = ""
  # msg = ErrMap[code] if not msg else msg
  if data:
    return jsonify(
      code=code,
      error={"msg": msg},
      data=data,
      total=total
    )
  
  return jsonify(
    code=code,
    error={"msg": msg}
  )

def md5(s: str):
    """将字符串md5"""
    md5_hash = md5_lib()
    md5_hash.update(s.encode(encoding='utf-8'))
    return md5_hash.hexdigest()

def md5_id():
  """用于生成ID字段"""
  uid = str(uuid())
  md5_uid = md5(uid)
  return uid[:8] + md5_uid[:8]

def encrypt(passwd: str):
  """字符加密"""
  return bcrypt.hashpw(bytes(passwd, encoding = "utf8"), bcrypt.gensalt(10))

def decrypt(passwd: str, hashed: str) -> bool:
  """校验明文"""
  return bcrypt.checkpw(bytes(passwd, encoding = "utf8"), hashed)

def utc_timestamp():
  return timegm(datetime.utcnow().utctimetuple())

if __name__ == "__main__":
  print(md5_id(), ".........")