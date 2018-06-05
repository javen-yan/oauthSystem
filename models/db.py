#coding:utf-8
# @Time    : 2018/6/5 下午6:57
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : db.py
# @Software: PyCharm
from settings import DATABASES
from peewee import MySQLDatabase

mysql_db = MySQLDatabase(
    database=DATABASES['NAME'],
    user=DATABASES['USER'],
    password=DATABASES['PASSWORD'],
    host=DATABASES['HOST'],
    port=int(DATABASES['PORT'])
)
