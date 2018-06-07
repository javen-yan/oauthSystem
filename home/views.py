#coding:utf-8
# @Time    : 2018/6/5 下午8:21
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : views.py
# @Software: PyCharm
from flask import session, request, jsonify, render_template, redirect
from werkzeug.security import generate_password_hash

from home import home
from models.client import Client
from models.user import User
from libs.security.security import gen_salt


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.get(User.id == uid)
    return None


def get_client(uid):
    if uid is None:
        return None
    else:
        clients = Client.select().filter(Client.user_id == uid).first()
        if clients:
            return Client.get(Client.user_id == uid)
        else:
            return None


@home.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = request.form.get('user')
        pw = request.form.get('pw')
        user = User.select().filter(User.username == user).first()
        if user:
            if user.check_password(pw):
                session.permanent = True
                session['id'] = user.id
                clients = get_client(user.id)
                return render_template('index.html', user=user, clients=clients)
            else:
                return jsonify(code=1, msg='密码错误')
        else:
            return jsonify(code=1,msg='没有此用户')
    else:
        user = current_user()
        if user is not None:
            clients = get_client(user.id)
        else:
            clients = []
        return render_template('index.html', user=user, clients=clients)


@home.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('user')
        pw = request.form.get('pw')
        pw1 = request.form.get('pw1')
        user = User.select().filter(User.username == username).first()
        if user:
            return jsonify(code=1,msg='用户已经存在')
        else:
            if pw != pw1:
                return jsonify(code=1,msg='密码出问题')
            else:
                user_tmp = User(
                    username=username,
                    password=generate_password_hash(pw)
                )
                user_tmp.save()
                session['id'] = user_tmp.id
                session.permanent = True
                return redirect('/home')
    else:
        return render_template('register.html')


@home.route('/logout')
def logout():
    try:
        del session['id']
    except Exception as e:
        return redirect('/home')
    return redirect('/home')


@home.route('/client',methods=['GET', 'POST'])
def clients():
    if request.method == 'GET':
        return render_template('create_client.html', errors=None)
    else:
        client_name = request.form.get('client_name')
        scope = request.form.get('scope')
        redirect_uri = request.form.get('redirect_uri')
        grant_type = request.form.get('grant_type')
        response_type = request.form.get('response_type')
        if client_name == '' or scope == '' or redirect_uri == '' or grant_type == '' or response_type == '':
            errors = {
                'code': 1,
                'msg': '请按要求填写数据'
            }
            return render_template('create_client.html', errors=errors)
        else:
            client = Client(
                client_name=client_name,
                scope=scope,
                redirect_uri=redirect_uri,
                grant_type=grant_type,
                response_type=response_type,
                user_id=current_user().id,
                client_id=gen_salt(24),
                client_secret=gen_salt(48)
            )
            client.save(force_insert=True)
            return redirect('/home')