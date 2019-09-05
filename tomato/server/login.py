# coding: utf-8
# 登录模块
import re
import jwt
from tomato.setting import JWT_SECRET
from tomato.setting import EXPIRED_TIME
from tomato.database.model import User
from tomato.utils.errCode import ErrCode
from tomato.utils.utils import decrypt
from tomato.utils.utils import DELETED_AT
from tomato.utils.utils import utc_timestamp
from tomato.utils.rsa import rsa_decrpyt

class LoginService():
    def login(self, **kwargs: object):
        """登录
        Args:
            kwargs: object
                - account: string, 登录账户
                - passwd:  string, 登录密码
        :return
            code: int, 错误码
            data: dict, 登录成功返回的用户信息
        """
        account = kwargs.get("account")
        passwd = kwargs.get("passwd")
        # rsa解密加密字符
        try:
            passwd = rsa_decrpyt(passwd)
        except Exception as e:
            print(e, "无效的密码")
            return ErrCode.ERR_PASSWD, None
        
        query = User.query
        # 邮箱或账户名登录
        if re.search(r'@', account):
            user = query.filter(User.email==account, User.deleted_at==DELETED_AT).first()
        else:
            user = query.filter(User.name==account, User.deleted_at==DELETED_AT).first()
        # 用户不存在
        if user is None:
            return ErrCode.LOGIN_ERR, None

        user = user.to_dict()
        # 密码错误
        if not decrypt(passwd, bytes(user["password"], encoding="utf-8")):
            return ErrCode.LOGIN_ERR, None

        payload =  {
            # 'iss': 'yourlin127@gmail.com',
            "id": user["id"],
            "role_id": user["role_id"],
            'exp': utc_timestamp() + EXPIRED_TIME,
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

        res = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "token": bytes.decode(token)
        }

        return 0, res

if __name__ == "__main__":
    handler = LoginService()
    body = {
        "account": "tomato",
        "passwd": "tomato"
    }
    # res = handler.login(**body)