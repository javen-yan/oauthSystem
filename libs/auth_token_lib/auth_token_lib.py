#coding:utf-8
# @Time    : 2018/6/6 下午8:52
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : auth_token_lib.py
# @Software: PyCharm
from libs.security.security import gen_salt
from models.auth_token import AuthToken
from models.client import Client


def gen_token_return(params):
    access_token = gen_salt(48)
    refresh_token = gen_salt(48)
    client_id = params.get('client_id')
    client = None
    try:
        client = Client.get(Client.client_id == client_id)
    except Exception as e:
        pass
    token_tmp = AuthToken(
        user_id=client.user_id,
        client_id=client.client_id,
        token_type='public',
        access_token=access_token,
        refresh_token=refresh_token,
        scope=client.scope,
        expires_in=17600000
    )
    token_tmp.save()
    return {'code':0, 'msg':'token is ok', 'data':token_tmp}