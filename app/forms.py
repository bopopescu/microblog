from flask.ext.wtf import Form
from wtforms import StringField, BooleanField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(Form):
	facebook_login = SubmitField('facebook')
	remember_me = BooleanField('remember_me', default=False)
	google_login = SubmitField('google')