import datetime
import json

from flask import Flask, render_template, request, jsonify, session, Response
import settings
from libs.auth_token_lib.auth_token_lib import  verify_token_response
from libs.helper_lib.helpler import need_auth
from gate import gate
from models.db import mysql_db
from home import home
from oauth import oauth
app = Flask(__name__)
app.register_blueprint(oauth, url_prefix='/oauth')
app.register_blueprint(home, url_prefix='/home')
app.register_blueprint(gate, url_prefix='/gate')
app.config.from_object(settings)
app.permanent_session_lifetime = datetime.timedelta(seconds=10*60)


@app.route('/')
def index():
    return 'Oauth server'


@app.before_request
def _db_connect():
    mysql_db.connect()


@app.teardown_request
def _db_close(exc):
    if not mysql_db.is_closed():
        mysql_db.close()


if __name__ == '__main__':
    app.run(debug=True)
