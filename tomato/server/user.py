# coding: utf-8
# 用户管理
from datetime import datetime

from tomato.setting import DBConfig
from tomato.utils.errCode import ErrCode
from tomato.database.model import db
from tomato.database.model import User
from tomato.database.model import Role
from tomato.utils.utils import DELETED_AT
from tomato.utils.utils import md5_id
from tomato.utils.utils import decrypt
from tomato.utils.utils import encrypt
from tomato.utils.utils import output_json

class UserService:
    def create(self, user: User):
        """创建用户""" 
        exist = User.query\
        .filter(db.or_(User.name==user.name, User.email==user.email))\
        .filter(User.deleted_at == DELETED_AT)\
        .first()
        
        if exist is None:
            # 密码加密
            user.password = encrypt(user.password)
            user.id = md5_id()
            db.session.add(user)
            db.session.commit()
        else:
            return output_json(code=ErrCode.EXIST_DATA)
        
        return output_json(code=0)
    
    def update(self, user_id: str, user: object):
        """更新用户信息"""
        allow_field = ["name", "email", "role_id"]
        for key in user.keys():
            if key not in allow_field:
                return output_json(code=ErrCode.ERR_PARAMS)

        query = User.query
        exist = query.filter_by(id=user_id)

        if not exist:
            return output_json(code=ErrCode.NO_DATA)
        # update
        exist.update(user)
        db.session.commit()
        return output_json(code=0)

    def list(self, where: object, offset=0, limit=15):
        """查询用户列表
        Args:
        where:  object, 查询条件
        offset: int, 分页
        limit:  int, 页宽
        """
        query = db.session.query(User.id, User.name, User.email, 
        User.created_at, User.updated_at, Role.name)
        # 按用户名查询
        if where.get("name"):
            name_like = "%" + where["name"] + "%"
            query = query.filter(User.name.like(name_like))
        # 按邮箱查询
        if where.get("email"):
            email_like = "%" + where["email"] + "%"
            query = query.filter(User.email.like(email_like))

        if where.get("created_at") and len(where.get("created_at")) == 2:
            created_time = where.get("created_at")
            query = query.filter(User.created_at.between(created_time[0], created_time[1]))

        query = query.filter(User.role_id == Role.id). \
        filter_by(deleted_at=DELETED_AT)
        
        count = query.count()
        offset = offset * limit
        rows = query.offset(offset).limit(limit).all()
        
        # 转为字典数组
        result = []
        for item in rows:
            obj = {
                "id": item[0],
                "name": item[1],
                "email": item[2],
                "created_at": item[3].strftime(DBConfig.DATETIME_FORMAT),
                "updated_at": item[4].strftime(DBConfig.DATETIME_FORMAT),
                "role_name": item[5]
            }
            result.append(obj)

        return output_json(data=result, total=count)
  
    def show(self, id: str):
        """用户详情
        Args:
        id: string, 用户ID
        """
        user = User.query.filter(User.id==id, User.deleted_at==DELETED_AT).first()
        if user is None:
            return output_json(code=ErrCode.NO_DATA)
        
        user = user.to_dict()
        del user["password"]
        return output_json(data=user, total=1, code=0)

    def destory(self, user_id: str):
        """删除用户
        Args:
        user_id: string,
        """
        user = User.query.filter(User.id==user_id, User.deleted_at==DELETED_AT).first()
        if user is None:
            return output_json(code=ErrCode.NO_DATA)

        User.query.filter_by(id=user_id).update({"deleted_at": datetime.now()})
        db.session.commit()

        return output_json(code=0)

    def changePasswd(self, user_id: str, **kwagrs):
        """修改密码
        Args:
        user_id: string
        kwagrs:
            - new_passwd: string, 新密码
            - old_passwd: string, 旧密码
        """
        row = User.query.filter(User.id==user_id, User.deleted_at==DELETED_AT).first()
        if row is None:
            return output_json(code=ErrCode.NO_DATA)

        row = row.to_dict()
        if not decrypt(kwagrs.get("old_passwd"), bytes(row["password"], encoding = "utf8")):
            return output_json(code=ErrCode.ERR_PASSWD)
        
        User.query.filter_by(id=user_id).update({
        "password": encrypt(kwagrs["new_passwd"])
        })
        db.session.commit()

        return output_json(code=0)

if __name__ == "__main__":
    user = UserService()

    # user.create(User(
    #   id=md5_id(),
    #   name="tomato",
    #   email="tomato@qq.com",
    #   password="tomato",
    #   role_id="20459894aee58f78"
    # ))
    # res = user.list(where={})
    user.update("80643aba3978c58e", {"name": "devp"})
    print(res)