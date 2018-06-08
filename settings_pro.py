#coding:utf-8
# @Time    : 2018/6/5 下午6:52
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : settings.py
# @Software: PyCharm
import os

DATABASES = {
    'HOST': 'oauth.geek-ealine.xyz',
    'PORT': 3306,
    'NAME': 'oauth_system',
    'USER': 'root',
    'PASSWORD': '..127521Yzz'
}

#调试信息配置
DEBUG = True

#密钥配置
SECRET_KEY = 'hjidhiodkjkdjiqjwdjowiejdoj'

#路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#域名配置
HOST = 'https://oauth.geek-ealine.xyz'

#log
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"