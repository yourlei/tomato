# coding: utf-8
# 映射数据库表模型

from datetime import datetime
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLALchemy
from tomato.app import app
from tomato.setting import DBConfig
from tomato.utils.utils import md5_id
from tomato.utils.utils import DELETED_AT

class SQLAlchemy(_SQLALchemy):
    @contextmanager
    def auto_commit(self):
        """通过contextlib管理自动提交及异常回滚,避免出现多个try/except的情况
        Usage:
        with 语法
        with db.auto_commit():
            # do something
        替换
        try:
            # doing something
            db.commit()
        except:
            db.rollback()
            raise
        """
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

TB_PREFIX = DBConfig.TB_PREFIX
DATETIME_FORMAT = DBConfig.DATETIME_FORMAT
db = SQLAlchemy(app)

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
    deleted_at = db.Column(db.DateTime, default=DELETED_AT)

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
    deleted_at = db.Column(db.DateTime, default=DELETED_AT)
    
    def __init__(self, name, email, password, role_id):
        # self.id = md5_id()
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

class Role_Relationship(db.Model):
    """角色资源关联表"""
    __tablename__ = TB_PREFIX + "role_relationship"

    id = db.Column(db.CHAR(16), primary_key=True, comment="主键")
    role_id = db.Column(db.CHAR(16), nullable=False, comment="角色ID")
    resource_id = db.Column(db.Integer, nullable=False, comment="资源ID")
    from_id = db.Column(db.Integer, nullable=False, comment="区别资源类型,1菜单资源")
    created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted_at = db.Column(db.DateTime, default=DELETED_AT)

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
    deleted_at = db.Column(db.DateTime, default=DELETED_AT)
    
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
    author_id  = db.Column(db.String(16), nullable=False, comment="作者ID")
    content = db.Column(db.Text, default="", comment="文章内容")
    cid = db.Column(db.CHAR(16), default="", comment="分类ID")
    status = db.Column(db.Integer, default=1, comment="文章状态1:已发布, 2:存为草稿")
    # comments = db.relationship('Comments', backref=__tablename__, lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_at = db.Column(db.DateTime, onupdate=datetime.now, comment="更新时间")
    deleted_at = db.Column(db.DateTime, default=DELETED_AT)

    def __init__(self, title, author_id, content, status):
        self.title  = title
        self.author_id = author_id
        self.content = content
        self.status = status
        # self.cid = cid

    def to_dict(self):
        return  {
            "id": self.id,
            "title": self.title,
            # "author": self.author,
            "content": self.content,
        }

class Category(db.Model):
    """分类表"""
    __tablename__ = TB_PREFIX + "category"

    id = db.Column(db.CHAR(16), primary_key=True, comment="唯一id")
    name = db.Column(db.String(32), nullable=False, comment="类名")
    created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted_at = db.Column(db.DateTime, default=DELETED_AT)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

# class Tag(db.Model):
#     """标签表"""
#     __tablename__ = TB_PREFIX + "tag"

#     id = db.Column(db.CHAR(16), primary_key=True, comment="唯一id")
#     name = db.Column(db.String(64), nullable=False, comment="标签名")
#     # article_id = db.Column(db.init_app, db.ForeignKey("tomato_article.id"), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
#     updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
#     deleted_at = db.Column(db.DateTime, default=DELETED_AT)

#     def __init__(self, name):
#         self.name = name
#
class Category_Relationship(db.Model):
    """标签与文章关联表"""
    __tablename__ = TB_PREFIX + "category_relationship"

    __table_args__ = (
        db.UniqueConstraint('cid', 'aid', name='uix_cid_aid'),
        # db.Index('index_name', 'column', 'column'),
    )

    # id = db.Column(db.CHAR(16), primary_key=True, comment="唯一id")
    id = db.Column(db.Integer, primary_key=True, comment="主键id")
    cid = db.Column(db.CHAR(16), default="", nullable=False, comment="category id")
    aid = db.Column(db.CHAR(16), default="", nullable=False, comment="article id")
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    deleted_at = db.Column(db.DateTime, default=DELETED_AT)

    def __init__(self, cid, aid):
        # self.id = id
        self.cid = cid
        self.aid = aid

class Comments(db.Model):
    """评论"""
    __tablename__ = TB_PREFIX + "comments"

    id = db.Column(db.CHAR(16), primary_key=True, comment="唯一id")
    comments = db.Column(db.String(256), nullable=False, comment="评论")
    article_id = db.Column(db.CHAR(16), db.ForeignKey("tomato_article.id"), nullable=False)