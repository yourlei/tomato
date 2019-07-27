# coding: utf-8
# 映射数据库表模型

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from tomato.app import app
from tomato.setting import DBConfig

db = SQLAlchemy(app)

deleted_at = "0000-01-01 00:00:00"

TB_PREFIX = DBConfig.TB_PREFIX
DATETIME_FORMAT = DBConfig.DATETIME_FORMAT

class Role(db.Model):
    """角色表"""
    __tablename__ = TB_PREFIX + "role"
    """
    tag: 角色类型, 1管理员, 2开发者
    """
    id   = db.Column(db.CHAR(16), primary_key=True, comment="唯一id")
    name = db.Column(db.String(64), nullable=False, comment="角色名称")
    tag  = db.Column(db.Integer, nullable=False, comment="角色类别")
    created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.now, comment="更新时间")
    deleted_at = db.Column(db.DateTime, default=deleted_at)

    def __init__(self, name, tag):
        self.name = name
        self.tag = tag
  
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "tag": self.tag,
            "created_at": self.created_at.strftime(DATETIME_FORMAT),
            "updated_at": self.updated_at.strftime(DATETIME_FORMAT)
        }

class User(db.Model):
    """用户表"""
    __tablename__ = TB_PREFIX + "user"

    id = db.Column(db.CHAR(16), primary_key=True, comment="唯一id")
    role_id = db.Column(db.CHAR(16), db.ForeignKey('tomato_role.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False, comment="用户名称")
    email = db.Column(db.String(64), nullable=False, comment="注册邮箱")
    password = db.Column(db.String(128), nullable=False, comment="账户密码")
    created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted_at = db.Column(db.DateTime, default=deleted_at)
    
    def __init__(self, id, name, email, password, role_id):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role_id = role_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role_id": self.role_id,
            "password": self.password,
            "created_at": self.created_at.strftime(DATETIME_FORMAT),
            "updated_at": self.updated_at.strftime(DATETIME_FORMAT)
        }

# class Resource(db.Model):
#   """资源表"""
#   __tablename__ = TB_PREFIX + "resource"

#   id = db.Column(db.Integer, primary_key=True, comment="主键")
#   from_id = db.Column(db.Integer, comment="资源外键")
#   name = db.Column(db.String(128), nullable=False, comment="资源名")
#   classify = db.Column(db.Integer, nullable=False, comment="资源类别")
#   remark = db.Column(db.String(256), nullable=True, comment="说明信息")
#   created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
#   updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
#   deleted_at = db.Column(db.DateTime, default=deleted_at)

#   def __init__(self, name, classify, remark=None, from_id=None):
#     self.name = name
#     self.classify = classify
#     self.from_id = from_id
#     self.remark = remark

#   def to_dict(self, encrypt=True):
#     return {
#       "id": self.id if encrypt else self.id,
#       "name": self.name,
#       "classify": self.classify,
#       "remark": self.remark,
#       "created_at": self.created_at.strftime(DATETIME_FORMAT),
#       "updated_at": self.updated_at.strftime(DATETIME_FORMAT)
#     }

class Role_Resoruce(db.Model):
    """角色资源关联表"""
    __tablename__ = TB_PREFIX + "role_resource"

    id = db.Column(db.CHAR(16), primary_key=True, comment="主键")
    role_id = db.Column(db.CHAR(16), nullable=False, comment="角色ID")
    resource_id = db.Column(db.Integer, nullable=False, comment="资源ID")
    from_id = db.Column(db.Integer, nullable=False, comment="区别资源类型,1菜单资源")
    created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted_at = db.Column(db.DateTime, default=deleted_at)

    def __init__(self, role_id, resource_id):
        self.role_id = role_id
        self.resource_id = resource_id

    def to_dict(self):
        return {
            "id": self.id,
            "role_id": self.role_id,
            "resource_id": self.resource_id,
            "created_at": self.created_at.strftime(DATETIME_FORMAT)
        }

class Menu(db.Model):
    """菜单表"""
    __tablename__ = TB_PREFIX + "menu"

    id = db.Column(db.CHAR(16), primary_key=True, comment="唯一id")
    name = db.Column(db.String(64), nullable=False, comment="资源名")
    url = db.Column(db.String(128), nullable=False, comment="页面路由")
    sort = db.Column(db.Integer, default=1, comment="菜单排序") 
    created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted_at = db.Column(db.DateTime, default=deleted_at)
    
    def __init__(self, name, url, sort):
        self.name = name
        self.url = url
        self.sort = sort

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "sort": self.sort,
            "created_at": self.created_at.strftime(DATETIME_FORMAT)
        }

class Article(db.Model):
    """文章表"""
    __tablename__ = TB_PREFIX + "article"

    id = db.Column(db.CHAR(16), primary_key=True, comment="唯一id")
    title = db.Column(db.String(128), nullable=False, comment="标题")
    author_id = db.Column(db.CHAR(16), db.ForeignKey("tomato_user.id"), nullable=False)
    content = db.Column(db.Text, default="", comment="文章内容")
    comments = db.relationship('Comments', backref=__tablename__, lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted_at = db.Column(db.DateTime, default=deleted_at)

class Tag(db.Model):
    """标签表"""
    __tablename__ = TB_PREFIX + "tag"

    id = db.Column(db.CHAR(16), primary_key=True, comment="唯一id")
    name = db.Column(db.String(32), nullable=False, comment="标签名")
    # article_id = db.Column(db.init_app, db.ForeignKey("tomato_article.id"), nullable=False)

class Comments(db.Model):
    """评论"""
    __tablename__ = TB_PREFIX + "comments"

    id = db.Column(db.CHAR(16), primary_key=True, comment="唯一id")
    comments = db.Column(db.String(256), nullable=False, comment="评论")
    article_id = db.Column(db.CHAR(16), db.ForeignKey("tomato_article.id"), nullable=False)