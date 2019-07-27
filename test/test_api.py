# coding: utf-8
# 自动化API测试

import unittest
import requests
from tomato.setting import TestConfig

host = TestConfig["host"]

class Test_tomato(unittest.TestCase):
    def test_login(self):
        """登录接口"""
        post_data = {
            "account": "tomato",
            "passwd": "tomato5321"
        }
        url = host + "/admin/login"
        res = requests.post(url, json=post_data).json()
        self.assertEqual(res["code"], 0, res["error"]["msg"])
    
    def test_user_passwd(self):
        """修改用户密码"""
        put_data = {
            "old_passwd": "tomato",
            "new_passwd": "tomato5321"
        }
        url = host + "/admin/passwd/84320f86496fdcbb"
        res = requests.put(url, json=put_data).json()
        self.assertEqual(res["code"], 0, res["error"]["msg"])

if __name__ == "__main__":
    unittest.main()