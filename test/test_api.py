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
            "passwd": "tomato123"
        }
        url = host + "/login"
        res = requests.post(url, json=data).json()
        self.assertEqual(res["code"], 0, res["msg"])
    
    def test_user_passwd(self):
        """修改用户密码"""
        data = {
            "old_passwd": "tomato",
            "new_passwd": "tomato5321"
        }
        url = host + "/admin/passwd/84320f86496fdcbb"
        res = requests.put(url, json=data).json()
        self.assertEqual(res["code"], 0, res["msg"])

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
        self.assertEqual(res["code"], 0, res["msg"])

    # def test_article_create(self):
    #     """发布文章"""
    #     pass
    
    def test_article_index(self):
        url = host + '/admin/article?query={"where":{"title": "linux"}}'
        res = requests.get(url).json()
        self.assertEqual(res["code"], 0, res["msg"])

    def test_article_show(self):
        """文章详情"""
        url = host + "/admin/article/4682075a57b34813"
        res = requests.get(url).json()
        self.assertEqual(res["code"], 0, res["msg"])

    def test_categroy_relation_create(self):
        """文章添加分类"""
        url = host + "/admin/category/relation"
        data = {
            "name": "python",
            "aid": "11"
        }
        res = requests.post(url, json=data).json()
        self.assertEqual(res["code"], 0, res["msg"])

if __name__ == "__main__":
    unittest.main()