#coding:utf-8
# @Time    : 2018/6/5 下午6:58
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : user.py
# @Software: PyCharm
from peewee import *
from werkzeug.security import check_password_hash

from models.db import mysql_db
from datetime import datetime


class User(Model):
    id = AutoField(primary_key=True)
    username = CharField(max_length=40)
    password = CharField(max_length=200)
    first_name = CharField(max_length=20, null=True)
    last_name = CharField(max_length=20, null=True)
    create_at = DateField(default=datetime.now())
    is_superuser = BooleanField(default=False)
    last_login = TimestampField()

    def __str__(self):
        return self.username

    def get_user_id(self):
        return self.id

    def check_password(self, password):
        if check_password_hash(self.password, password):
            return True
        else:
            return False

    class Meta:
        database = mysql_db
        db_table = 'user'
