# coding:utf-8
# @Time    : 2018/6/6 下午8:06
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : auth_code_lib.py
# @Software: PyCharm
from flask import jsonify
from werkzeug.utils import redirect

from libs.security.security import gen_salt
from models.auth_code import AuthCode
from models.client import Client


def gen_auth_code(grant, redirect_uri):
    code = gen_salt(24)
    authcode_tmp = AuthCode(
        user_id=grant.user_id,
        client_id=grant.client_id,
        redirect_uri=redirect_uri,
        scope=grant.scope,
        response_type=grant.response_type,
        code=code
    )
    authcode_tmp.save()
    _redirect_uri = redirect_uri + '&code=%s' % code
    return _redirect_uri


def verify_auth_code(data):
    try:
        client = Client.get(Client.client_id == data.get('client_id'))
        if data.get('client_secret') != client.client_secret:
            return {'code': 1, 'msg': 'client_secret is error'}
        else:
            try:
                authcode = AuthCode.get(AuthCode.code == data.get('code'))
                if authcode.is_expired():
                    return {'code': 1, 'msg': 'code is_expired'}
                else:
                    return {'code': 0, 'msg': 'code is ok'}
            except Exception as e:
                return {'code': 1, 'msg': 'code is error'}
    except Exception as e:
        return {'code': 1, 'msg': 'code verify error no such client'}

