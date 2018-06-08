#coding:utf-8
# @Time    : 2018/6/6 下午8:52
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : auth_token_lib.py
# @Software: PyCharm
import json

from libs.security.security import gen_salt, generate_token
from models.auth_code import AuthCode
from models.auth_token import AuthToken
from models.client import Client


def gen_token_return(params):
    access_token = generate_token(48)
    refresh_token = generate_token(48)
    client_id = params.get('client_id')
    code = params.get('code')
    authcode = AuthCode.select().filter(AuthCode.code == code).first()
    if authcode and not authcode.is_expired():
        client = Client.select().filter(Client.client_id == client_id).first()
        if client:
            token_tmp = AuthToken(
                user_id=authcode.user_id,
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
    else:
        return {'code': 1, 'msg': 'auth_code is_expired'}


def verify_token_response(request):
    token = json.loads(request.data.decode()).get('payload').get('accessToken')
    print('\r\n request.data \r\n',request.data.decode())
    _token = AuthToken.get(AuthToken.access_token == token)
    user_id = _token.user_id
    client_id = _token.client_id
    resp = {'code':0,'data':{'user_id':user_id,'client_id':client_id}}
    print('\r\n request.response \r\n',resp)
    return resp