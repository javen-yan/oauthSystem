#coding:utf-8
# @Time    : 2018/6/7 下午2:15
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : helpler.py
# @Software: PyCharm
import json

from flask import Response

from models.auth_token import AuthToken


def need_auth(fn):
    def wrapper(request, *args, **kwargs):
        auth = json.loads(request.data.decode()).get('payload')
        if auth:
            token_tmp = AuthToken.select().filter(AuthToken.access_token == auth.get('accessToken')).first()
            if token_tmp:
                if token_tmp.is_access_token_expired():
                    return Response('access_token_expired', status=401)
                else:
                    return fn(request, *args, **kwargs)
            else:
                return Response('access_token_invalid', status=401)
        else:
            return Response('Unauthorized', status=401)
    return wrapper
