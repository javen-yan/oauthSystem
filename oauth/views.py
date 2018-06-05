#coding:utf-8
# @Time    : 2018/6/5 下午6:47
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : views.py
# @Software: PyCharm
from oauth import oauth


@oauth.route('/token', methods=['GET','POST'])
def oauth_token():
    return 'token'