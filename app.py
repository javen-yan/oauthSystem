import datetime
import json

from flask import Flask, render_template, request, jsonify, session, Response
import settings
from libs.auth_token_lib.auth_token_lib import  verify_token_response
from libs.helper_lib.helpler import need_auth
from models.auth_token import AuthToken
from models.db import mysql_db
from home import home
from oauth import oauth
app = Flask(__name__)
app.register_blueprint(oauth, url_prefix='/oauth')
app.register_blueprint(home, url_prefix='/home')
app.config.from_object(settings)
app.permanent_session_lifetime = datetime.timedelta(seconds=10*60)


@app.route('/')
def index():
    return 'Oauth server'


@need_auth
@app.route('/api/me', methods=['GET', 'POST'])
def me():
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


@app.before_request
def _db_connect():
    mysql_db.connect()


@app.teardown_request
def _db_close(exc):
    if not mysql_db.is_closed():
        mysql_db.close()


if __name__ == '__main__':
    app.run(debug=True)
