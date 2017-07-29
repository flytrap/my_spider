# coding:utf8
# Author: flytrap


class CustomException(Exception):
    """自定义异常"""


class LoginException(CustomException):
    """定义登录异常"""
