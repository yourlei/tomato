# coding: utf-8

from uuid import uuid1 as uuid
from hashlib import md5 as md5_lib

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

if __name__ == "__main__":
  print(md5_id(), ".........")