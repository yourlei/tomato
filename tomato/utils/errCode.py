# coding: utf-8
# 定义错误码

class ErrCode:
    SUCCESS = 0 # 正常返回
    INNERERR = 1 # 内部错误
    NO_AUTH  = 2 # 未授权
    SERVER_ERR = 3 # 服务异常
    HEADER_ERR = 4 # 请求头缺少参数
    # 接口返回
    ERR_PARAMS = 101 # 参数错误
    EXIST_DATA = 102 # 数据已存在
    NO_DATA    = 103 # 数据不存在
    NOT_ALLOW  = 104 # 非法字段
    ERR_PASSWD = 105 # 密码错误
    ERR_CODE   = 106 # 验证码不正确
    JWT_ERR    = 107 # 无效的token
    LOGIN_ERR  = 108 # 无效的账户或密码

ErrMap = {
    ErrCode.INNERERR:   u"系统错误",
    ErrCode.SERVER_ERR: u"服务异常",
    ErrCode.ERR_PARAMS: u"参数错误",
    ErrCode.EXIST_DATA: u"数据已存在",
    ErrCode.NOT_ALLOW:  u"字段错误",
    ErrCode.ERR_PASSWD: u"账户密码不正确",
    ErrCode.NO_DATA:    u"数据不存在",
    ErrCode.ERR_CODE:   u"验证码不正确",
    ErrCode.NO_AUTH:    u"未授权",
    ErrCode.JWT_ERR:    u"无效的token",
    ErrCode.LOGIN_ERR:  u"无效的账户或密码",
    ErrCode.HEADER_ERR: u"请求头缺少参数",
}