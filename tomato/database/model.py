# coding: utf-8
# 映射数据库表模型

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from tomato.app import app
from tomato.utils.encrypt import IdEncrypt
from tomato.setting import DBConfig

db = SQLAlchemy(app)
# id加密
id_encrypt = IdEncrypt()

deleted_at = "0000-01-01 00:00:00"

class Role(db.Model):
  """角色表"""
  __tablename__ = "role"
  """
  tag: 角色类型, 1管理员, 2代理商, 3港口, 4船东, 5其他角色
  """
  id   = db.Column(db.Integer, primary_key=True, comment="唯一id")
  name = db.Column(db.String(64), nullable=False, comment="角色名称")
  tag = db.Column(db.Integer, nullable=False, comment="角色类别")
  created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
  updated_at = db.Column(db.DateTime, default=datetime.now, comment="更新时间")
  deleted_at = db.Column(db.DateTime, default=deleted_at)

  def __init__(self, name, tag):
    self.name = name
    self.tag = tag
  
  def to_dict(self):
    return {
      "id": id_encrypt.encode_id(self.id),
      "name": self.name,
      "tag": self.tag,
      "created_at": self.created_at.strftime(DBConfig.DATETIME_FORMAT),
      "updated_at": self.updated_at.strftime(DBConfig.DATETIME_FORMAT)
    }

class User(db.Model):
  """用户表"""
  __tablename__ = "user"

  id = db.Column(db.Integer, primary_key=True, comment="唯一id")
  name = db.Column(db.String(64), nullable=False, comment="用户名称")
  email = db.Column(db.String(64), nullable=False, comment="注册邮箱")
  password = db.Column(db.String(128), nullable=False, comment="账户密码")
  role_id = db.Column(db.Integer, nullable=False, comment="角色ID")
  created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
  updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
  deleted_at = db.Column(db.DateTime, default=deleted_at)
  
  def __init__(self, name, email, password, role_id):
    self.name = name
    self.email = email
    self.password = password
    self.role_id = role_id

  def to_dict(self):
    return {
      "id": id_encrypt.encode_id(self.id),
      "name": self.name,
      "email": self.email,
      "role_id": id_encrypt.encode_id(self.role_id),
      "password": self.password,
      "created_at": self.created_at.strftime(DBConfig.DATETIME_FORMAT),
      "updated_at": self.updated_at.strftime(DBConfig.DATETIME_FORMAT)
    }

class Resource(db.Model):
  """资源表"""
  __tablename__ = "resource"

  id = db.Column(db.Integer, primary_key=True, comment="主键")
  from_id = db.Column(db.Integer, comment="资源外键")
  name = db.Column(db.String(128), nullable=False, comment="资源名")
  """ classify: 
  1代理商, 珠江高速
  2港口, 南沙客运港
  3航线, HKC-PY
  4船只, 美珠湖,12341(船名,船id)
  5线路, 机场或市区
  以上四种资源名称应约定相应的输入格式
  """
  classify = db.Column(db.Integer, nullable=False, comment="资源类别")
  remark = db.Column(db.String(256), nullable=True, comment="说明信息")
  created_at = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
  updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
  deleted_at = db.Column(db.DateTime, default=deleted_at)

  def __init__(self, name, classify, remark=None, from_id=None):
    self.name = name
    self.classify = classify
    self.from_id = from_id
    self.remark = remark

  def to_dict(self, encrypt=True):
    return {
      "id": id_encrypt.encode_id(self.id) if encrypt else self.id,
      "name": self.name,
      "classify": self.classify,
      "remark": self.remark,
      "created_at": self.created_at.strftime(DBConfig.DATETIME_FORMAT),
      "updated_at": self.updated_at.strftime(DBConfig.DATETIME_FORMAT)
    }

class Role_Resoruce(db.Model):
  """角色资源关联表"""
  __tablename__ = "role_resource"

  id = db.Column(db.Integer, primary_key=True, comment="主键")
  role_id = db.Column(db.Integer, nullable=False, comment="角色ID")
  resource_id = db.Column(db.Integer, nullable=False, comment="资源ID")
  created_at = db.Column(db.DateTime, comment="创建时间")
  # updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
  deleted_at = db.Column(db.DateTime, default=deleted_at)

  __table_args__ = (
    db.UniqueConstraint('role_id', 'resource_id', name='uix_rid_resid'),  # 联合唯一索引
    # Index('ix_id_name', 'name', 'extra'),  # 联合索引
  )

  def __init__(self, role_id, resource_id):
    self.role_id = role_id
    self.resource_id = resource_id

  def to_dict(self):
    return {
      "id": id_encrypt.encode_id(self.id),
      "role_id": self.role_id,
      "resource_id": self.resource_id,
      "created_at": self.created_at.strftime(DBConfig.DATETIME_FORMAT)
    }

class Menu(db.Model):
  """菜单表"""
  __tablename__ = "menu"

  id = db.Column(db.Integer, primary_key=True, comment="唯一id")
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
      "id": id_encrypt.encode_id(self.id),
      "name": self.name,
      "url": self.url,
      "sort": self.sort,
      "created_at": self.created_at.strftime(DBConfig.DATETIME_FORMAT)
    }