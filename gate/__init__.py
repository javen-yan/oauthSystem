#coding:utf-8
# @Time    : 2018/6/8 下午4:24
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint

gate = Blueprint(
            'gate',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static/'
            )

from gate import views