# coding: utf-8
# 自动化API测试

import unittest
import requests
from tomato.setting import TestConfig

host = TestConfig["host"]

class Test_tomato(unittest.TestCase):
    def test_login(self):
        """登录接口"""
        data = {
            "account": "tomato",
            "passwd": "tomato5321"
        }
        url = host + "/admin/login"
        res = requests.post(url, json=data).json()
        self.assertEqual(res["code"], 0, res["error"]["msg"])
    
    def test_user_passwd(self):
        """修改用户密码"""
        data = {
            "old_passwd": "tomato",
            "new_passwd": "tomato5321"
        }
        url = host + "/admin/passwd/84320f86496fdcbb"
        res = requests.put(url, json=data).json()
        self.assertEqual(res["code"], 0, res["error"]["msg"])

    def test_user_create(self):
        """创建用户"""
        data = {
            "name": "dev",
            "email": "dev@dev.com",
            "password": "scut2092",
            "role_id": "20459894aee58f78"
        }
        url = host + "/admin/user"
        res = requests.post(url, json=data).json()
        self.assertEqual(res["code"], 0, res["error"]["msg"])

    def test_article_create(self):
        """发布文章"""
        pass
if __name__ == "__main__":
    unittest.main()