import datetime
from flask import Flask, render_template, request, jsonify, session
import settings
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


@app.route('/api/me', methods=['GET', 'POST'])
def me():
    if request.args.get('token'):
        return jsonify(code=0,token=request.args.get('token'))



@app.before_request
def _db_connect():
    mysql_db.connect()


@app.teardown_request
def _db_close(exc):
    if not mysql_db.is_closed():
        mysql_db.close()


if __name__ == '__main__':
    app.run()
