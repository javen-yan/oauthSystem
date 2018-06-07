#coding:utf-8
# @Time    : 2018/6/5 下午6:47
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : views.py
# @Software: PyCharm
import json

import os
from flask import request, jsonify, render_template, Response
import logging
import settings
from libs.json_file.json_file_lib import json_file_redaer, json_write
from libs.rewrite.rewrite_utils import redirect
from home.views import current_user
from libs.auth_code_lib.auth_code_lib import gen_auth_code, verify_auth_code
from libs.auth_token_lib.auth_token_lib import gen_token_return
from models.client import Client
from oauth import oauth
_redirect_url = None
grant = None

# log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'oauth2.log')
log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'oauth2.log')
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=settings.LOG_FORMAT, datefmt=settings.DATE_FORMAT)
save_json = json_file_redaer()


@oauth.route('/token', methods=['GET','POST'])
def oauth_token():
    global save_json
    if request.method == 'GET':
        return jsonify(code=1,msg='Not support GET methods')
    else:
        data = request.values
        logging.debug('values param is %s' % request.values)
        logging.debug('*********redirec_uri param is %s**********' % request.values.get('redirect_uri'))
        print('values param is %s' % request.values)
        res = verify_auth_code(data)
        if res.get('code') == 1:
            error_token = {
                'error': "001",
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
            if response.get('code') == 1:
                error_token = {
                    "error": "001",
                    "error_description":response.get('msg')
                }
                format = json.dumps(error_token)
                save_json['eror_token'] = error_token
                json_write(save_json)
                return Response(
                    response=format,
                    mimetype="application/json",
                    status=200
                )
            else:
                res_Data = response.get('data')
                token_res = {
                    "access_token": res_Data.access_token,
                    "refresh_token": res_Data.refresh_token,
                    "expires_in": res_Data.expires_in
                }
                formarts = json.dumps(token_res)
                save_json['token'] = token_res
                json_write(save_json)
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
        redirect_url = request_data.get('redirect_uri')
        raw_redirect_url = redirect_url.split('?')[0]
        _token = request_data.get('token')
        _state = request_data.get('state')
        _redirect_url = redirect_url+'&token=%s&state=%s' % (_token, _state)
        response_type = request_data.get('response_type')
        grant = Client.select().filter(Client.client_id == client_id).first()
        if grant:
            if grant.response_type != response_type:
                return jsonify(code=1,msg='Not support response_type')
            else:
                if raw_redirect_url == grant.redirect_uri:
                    return render_template('oauth.html', grant=grant, user=user)
                else:
                    return jsonify(code=1,msg='incorrect redirect_uri')
        else:
            return jsonify(code=1,msg='grant Not such client')
    else:
        if request.form['confirm']:
            uri = gen_auth_code(grant, _redirect_url)
            return redirect(uri)
        else:
            return render_template('oauth.html', grant=grant, user=user)

