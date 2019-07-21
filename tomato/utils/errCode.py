# coding: utf-8
# 定义错误码

class ErrCode:
  # 正常返回
  SUCCESS = 0
  # 内部错误
  INNERERR = 1
  NO_AUTH  = 2 # 未授权
  # 接口返回
  ERR_PARAMS = 101 # 参数错误
  EXIST_DATA = 102 # 数据已存在
  NO_DATA    = 103 # 数据不存在
  NOT_ALLOW  = 104 # 非法字段
  ERR_PASSWD = 105 # 密码错误
  ERR_CODE   = 106 # 验证码不正确

ErrMap = {
  ErrCode.INNERERR:   u"系统错误",
  ErrCode.ERR_PARAMS: u"参数错误",
  ErrCode.EXIST_DATA: u"数据已存在",
  ErrCode.NOT_ALLOW:  u"字段错误",
  ErrCode.ERR_PASSWD: u"账户密码不正确",
  ErrCode.NO_DATA:    u"数据不存在",
  ErrCode.ERR_CODE:   u"验证码不正确",
  ErrCode.NO_AUTH:    u"未授权",
}