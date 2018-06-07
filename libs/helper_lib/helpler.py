#coding:utf-8
# @Time    : 2018/6/7 下午2:15
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : helpler.py
# @Software: PyCharm
from flask import Response


def need_auth(fn):
    def wrapper(request, *args, **kwargs):
        if request.header.get('Authorization'):
            return fn(request, *args, **kwargs)
        else:
            print('Unauthorized',request.values)
            return Response('Unauthorized', status=401)
    return wrapper
