#coding:utf-8
# @Time    : 2018/6/6 下午8:52
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : auth_token_lib.py
# @Software: PyCharm
from libs.security.security import gen_salt, generate_token
from models.auth_token import AuthToken
from models.client import Client


def gen_token_return(params):
    access_token = generate_token(48)
    refresh_token = generate_token(48)
    client_id = params.get('client_id')
    client = Client.select().filter(Client.client_id == client_id).first()
    if client:
        token_tmp = AuthToken(
            user_id=client.user_id,
            client_id=client.client_id,
            token_type='public',
            access_token=access_token,
            refresh_token=refresh_token,
            scope=client.scope,
            expires_in=172800
        )
        token_tmp.save()
        return {'code': 0, 'msg': 'token is ok', 'data': token_tmp}
    else:
        return {'code': 1, 'msg': 'token general error No such client'}


def verify_token(request):
    auth = request.headers.get('Authorization')
    print(request.headers)
    token_tmp = AuthToken.select().filter(AuthToken.access_token == auth).first()
    if token_tmp:
        if token_tmp.is_access_token_expired():
            return {'code':1, 'msg':'access_token_expired'}
        else:
            return {'code':0, 'msg':'access_token_is_ok'}
    else:
        return {'code': 1, 'msg': 'access_token_invalid'}