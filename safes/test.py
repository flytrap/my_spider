# coding:utf8
# Author: flytrap
import unittest
from unittest import TestCase
from safes.logins import SinaLogin

from settings import SINA_PASSWORD, SINA_USERNAME


class TestSinaLoin(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSinaLoin, self).__init__(*args, **kwargs)
        self.username = SINA_USERNAME
        self.password = SINA_PASSWORD

    def test_sina_login(self):
        sina_login = SinaLogin(self.username, self.password)
        self.assertTrue(sina_login.check_login())
        del sina_login

    def test_sina_send_weibo(self):
        sina_login = SinaLogin(self.username, self.password)
        sina_login.send_wb('weibo send ok')
        del sina_login


if __name__ == '__main__':
    unittest.main()
