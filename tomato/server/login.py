# coding: utf-8
# 登录模块

import re
import jwt
from tomato.setting import JWT_SECRET
from tomato.database.model import db
from tomato.database.model import User
from tomato.utils.errCode import ErrCode
from tomato.utils.utils import decrypt
from tomato.utils.utils import DELETED_AT
from tomato.utils.utils import output_json
from tomato.utils.utils import utc_timestamp

class LoginService():
  def login(self, **kwargs: object):
    """ 登录 """
    account = kwargs.get("account")
    passwd = kwargs.get("passwd")

    query = User.query
    # 邮箱或账户名登录
    if re.search(r'@', account):
      user = query.filter(User.email==account, User.deleted_at==DELETED_AT).first()
    else:
      user = query.filter(User.name==account, User.deleted_at==DELETED_AT).first()
    # 用户不存在
    if user is None:
      return output_json(code=ErrCode.NO_DATA)
    user = user.to_dict()
    # 密码错误
    if not decrypt(passwd, bytes(user["password"], encoding="utf-8")):
      return output_json(code=ErrCode.ERR_PASSWD)

    payload =  {
      # 'iss': 'yourlin127@gmail.com',
      "id": user["id"],
      'exp': utc_timestamp() + 3600,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

    res = {
      "id": user["id"],
      "name": user["name"],
      "email": user["email"],
      "token": token
    }

    return output_json(data=res, code=0)

if __name__ == "__main__":
  # jwt_message = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJqZWZmIiwiZXhwIjoxNTYzNzA1NTk3LCJjbGFpbSI6Imluc2FuaXR5In0.1E3p0xPh5pLTMkuAdKpsGL6KTx7ZxR136ZOj6I63LeA'
  # decoded_payload = jwt.decode(jwt_message, "youme")
  handler = LoginService()
  body = {
    "account": "tomato",
    "passwd": "tomat"
  }
  res = handler.login(**body)