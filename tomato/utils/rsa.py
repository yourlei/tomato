# coding: utf-8
# RSA实现非对称加解密
# 前后端分离的场景, 后端生成公钥及私钥匙, 前端通过JSEncrypt库对安全字符进行加密
# JSEncrypt: https://www.npmjs.com/package/jsencrypt
# PyCryptodome文档: https://pycryptodome.readthedocs.io/en/latest/src/examples.html
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5
from tomato.setting import rsa_public_key
from tomato.setting import rsa_private_key
from tomato.setting import rsa_secret

def init_rsa(secret_code=rsa_secret):
    """生成RSA秘钥"""
    key = RSA.generate(2048)
    encrypted_key = key.export_key(passphrase=secret_code, pkcs=8,
        protection="scryptAndAES128-CBC")

    # 代码参考: https://blog.csdn.net/yannanxiu/article/details/76436032
    # 生成私钥
    with open(rsa_private_key, "wb") as f:
        f.write(encrypted_key)
    # 生成公钥
    with open(rsa_public_key, "wb") as f:
        f.write(key.publickey().exportKey())

def rsa_decrpyt(passwd: str, secret_code=rsa_secret):
    """rsa解密
    Args:
        passwd: string,　使用公钥加密后字符
        secret_code: string, 创建rsa的秘钥
    """
    # """使用公钥加密"""
    # recipient_key = RSA.import_key(
    #     open(rsa_public_key).read()
    # )
    # cipher_rsa = PKCS1_v1_5.new(recipient_key)
    # en_data = cipher_rsa.encrypt(b"123456")
    # print(len(en_data), en_data)

    """通过私钥解密"""
    private_key = RSA.import_key(open(rsa_private_key).read(),
        passphrase=secret_code)
    cipher_rsa = PKCS1_v1_5.new(private_key)
    # data = cipher_rsa.decrypt(passwd, None)
    # 前端默认使用了base64加密
    try:
        data = cipher_rsa.decrypt(base64.b64decode(passwd), None)
    except Exception as e:
        # error类型: ValueError
        raise e
    if data is not None:
        data = data.decode("utf-8") 

    return data

if __name__ == "__main__":
    # 加载公钥
    # init_rsa()
    rsa_decrpyt("4vPj1H4CLhikXg6UEHGt4S2W3NcWP/tL7fkEojOvm4sRWnSSuV6w3jp4OuOWHi0mnpcEF/rvHZqRUzDWH13o5VRCJKFj9NebvVpo0QBuYx2Q1xsZY9Qp6k7yOsAFIrG8VNhaBr6DzYbX5qv2hRz9dYpSObjht+OwQZyXtGtFqbw3lYPgyx92lBsZxgEHeSwlSOGbDr1pzn844lcISM+GS+qECubgpaBm4kbQySVZfCDd54RfvpkrtI0mzyNXLJHx3VL2W2ecruQEj5Ks6/0AJZJnb13iKRFIBqh1qR6GGXWino/Q==")
