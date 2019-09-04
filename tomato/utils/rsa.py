# coding: utf-8
# 生成RSA秘钥
# PyCryptodome文档: https://pycryptodome.readthedocs.io/en/latest/src/examples.html
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from tomato.setting import rsa_public_key
from tomato.setting import rsa_private_key
from tomato.setting import rsa_secret

def init_rsa(secret_code=rsa_secret):
    """生成RSA秘钥"""
    # secret_code = "U9$vIk"
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

def rsa_decrpyt(secret_code=rsa_secret):
    recipient_key = RSA.import_key(
        open(rsa_public_key).read()
    )
    cipher_rsa = PKCS1_v1_5.new(recipient_key)

    en_data = cipher_rsa.encrypt(b"123456")
    print(len(en_data), en_data)

    # 读取密钥
    private_key = RSA.import_key(open(rsa_private_key).read(),
        passphrase=secret_code)
    cipher_rsa = PKCS1_v1_5.new(private_key)
    data = cipher_rsa.decrypt(en_data, None)

if __name__ == "__main__":
    # 加载公钥
    init_rsa()
    # rsa_decrpyt(RSA_SECRET)
