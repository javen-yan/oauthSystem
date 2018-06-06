#coding:utf-8
# @Time    : 2018/6/5 下午6:47
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : views.py
# @Software: PyCharm
import json

from flask import request, jsonify, render_template, Response
from libs.rewrite.rewrite_utils import redirect
from home.views import current_user
from libs.auth_code_lib.auth_code_lib import gen_auth_code, verify_auth_code
from libs.auth_token_lib.auth_token_lib import gen_token_return
from models.client import Client
from oauth import oauth
_redirect_url = None
grant = None


@oauth.route('/token', methods=['GET','POST'])
def oauth_token():
    if request.method == 'GET':
        return jsonify(code=1,msg='Not support GET methods')
    else:
        data = request.args
        res = verify_auth_code(data)
        if res.get('code') == 1:
            error_token = {
                'error': 1,
                'error_description': res.get('msg')
            }
            format_Res = json.dumps(error_token)
            return Response(
                response=format_Res,
                mimetype="application/json",
                status=200
            )
        else:
            response = gen_token_return(data)
            print('code response', response)
            if response.get('code') == 1:
                error_token = {
                    'error': 1,
                    'error_description':response.get('msg')
                }
                format = json.dumps(error_token)
                return Response(
                    response=format,
                    mimetype="application/json",
                    status=200
                )
            else:
                res_Data = response.get('data')
                token_res = {
                    'retCode': 0,
                    'access_token': res_Data.access_token,
                    'refresh_token': res_Data.refresh_token,
                    'expires_in': res_Data.expires_in
                }
                formarts = json.dumps(token_res)
                return Response(
                    response=formarts,
                    mimetype="application/json",
                    status=200
                )


@oauth.route('/authorize', methods=['GET', 'POST'])
def authorize():
    global grant
    global _redirect_url
    user = current_user()
    if request.method == 'GET':
        request_data = request.args
        client_id = request_data.get('client_id')
        try:
            grant = Client.get(Client.client_id == client_id)
        except Exception as e:
            return jsonify(code=1,msg='No Such Client')
        redirect_url = request_data.get('redirect_uri')
        raw_redirect_url = redirect_url.split('?')[0]
        _token = request_data.get('token')
        _state = request_data.get('state')
        _redirect_url = redirect_url+'&token=%s&state=%s' % (_token, _state)
        response_type = request_data.get('response_type')
        if grant.response_type != response_type:
            return jsonify(code=1,msg='Not support response_type')
        else:
            if raw_redirect_url == grant.redirect_uri:
                return render_template('oauth.html', grant=grant, user=user)
            else:
                return jsonify(code=1,msg='incorrect redirect_uri')
    else:
        if request.form['confirm']:
            uri = gen_auth_code(grant, _redirect_url)
            return redirect(uri)
        else:
            return render_template('oauth.html', grant=grant, user=user)



