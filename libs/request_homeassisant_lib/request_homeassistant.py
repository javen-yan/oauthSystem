#coding:utf-8
# @Time    : 2018/6/14 下午4:44
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : request_homeassistant.py
# @Software: PyCharm
import requests
import json


def ask_homeassisant(ha_url, ha_password):
    url = ha_url + '/api/states?api_password=' + ha_password
    res = requests.get(url=url,headers={'Content-Type': 'application/json'})
    if res.status_code == 200:
        devices = json.loads(res.text)
        return devices
    else:
        return None


if __name__ == "__main__":
    ha_url = 'http://ha.ealine.cn'
    ha_password = '127521yzz'

    datas = ask_homeassisant(ha_url,ha_password)
    for data in datas:
        print(data.get('entity_id'))
        print(data.get('state'))