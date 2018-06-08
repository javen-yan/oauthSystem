#coding:utf-8
# @Time    : 2018/6/8 下午4:24
# @Author  : yanzongzhen
# @Email   : yanzz@catial.cn
# @File    : views.py
# @Software: PyCharm
import json

from flask import jsonify, Response, request

from gate import gate
from libs.auth_token_lib.auth_token_lib import verify_token_response
from libs.helper_lib.helpler import need_auth


@need_auth
@gate.route('/', methods=['GET','POST'])
def gate():
    res = verify_token_response(request)
    if res.get('code') == 0:
        response = {
            "header": {
                "namespace": "AliGenie.Iot.Device.Discovery",
                "name": "DiscoveryDevicesResponse",
                "messageId": "1bd5d003-31b9-476f-ad03-71d471922820",
                "payLoadVersion": 1
            },
            "payload": {
                "devices": [{
                    "deviceId": "34ea34cf2e63",
                    "deviceName": "单孔插座",
                    "deviceType": "outlet",
                    "zone": "",
                    "brand": "",
                    "model": "",
                    "icon": "https://git.cn-hangzhou.oss-cdn.aliyun-inc.com/uploads/aicloud/aicloud-proxy-service/41baa00903a71c97e3533cf4e19a88bb/image.png",
                    "properties": [{
                        "name": "powerstate",
                        "value": "off"
                    }],
                    "actions": [
                        "TurnOn",
                        "TurnOff"
                    ],
                    "extensions": {
                        "extension1": "",
                        "extension2": ""
                    }
                }, {
                    "deviceId": "34ea34cf2eff",
                    "deviceName": "灯",
                    "deviceType": "light",
                    "zone": "",
                    "brand": "",
                    "model": "",
                    "icon": "https://git.cn-hangzhou.oss-cdn.aliyun-inc.com/uploads/aicloud/aicloud-proxy-service/41baa00903a71c97e3533cf4e19a88bb/image.png",
                    "properties": [{
                        "name": "powerstate",
                        "value": "off"
                    }],
                    "actions": [
                        "TurnOn",
                        "TurnOff"
                    ],
                    "extensions": {
                        "parentId": "34ea34cf2e63",
                        "extension1": "",
                        "extension2": ""
                    }
                }]
            }
        }
        data = json.dumps(response)
        return Response(
            response=data,
            mimetype='application/json'
        )
    else:
        return jsonify(res)
