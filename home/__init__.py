#coding:utf-8
# @Time    : 2018/6/5 下午8:21
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint

home = Blueprint(
            'home',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static/'
            )

from home import views