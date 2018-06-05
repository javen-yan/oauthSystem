#coding:utf-8
# @Time    : 2018/6/5 下午6:46
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint

oauth = Blueprint(
            'oauth',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static/'
            )

from oauth import views