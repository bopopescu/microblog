from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask_oauth import OAuth
from config import basedir
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view='login'
oid = OpenID(app,os.path.join(basedir,'tmp'))
oauth= OAuth()
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=413764145465595,
    consumer_secret='8eb287f3edce544d0a5ad20c2b6a2c90',
    request_token_params={'scope': 'email'}
)
from app import views, models
