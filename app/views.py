from flask import render_template, flash, redirect,session,url_for,request,g
from flask.ext.login import login_user,logout_user,current_user,login_required
from app import app,db,lm,oid,facebook
from .forms import LoginForm
from .models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user
	posts = [
	    {
		'author':{'nickname':'John'},
		'body':'Beautiful day in Portland!'
	    },
	    {
		'author':{'nickname':'susan'},
		'body':'The Avengers movie was so cool!'
	    }
	]
	return render_template('index.html',title='Home',user=user,posts=posts)
@app.before_request
def before_request():
	g.user=current_user

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.'% nickname)
        return redirect(url_for('index'))
    posts= [
        {'author':user, 'body':'Test post#1'},
        {'author':user,'body':'Test post#2'}
    ]
    return render_template('user.html',
                            user=user,
                            posts=posts)

@app.route('/login',methods=['GET','POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form=LoginForm()
	for e in request.form:
		print e
	if form.validate_on_submit():
		if "facebook_login" in request.form:
			print request.form
			return facebook.authorize(callback=url_for('facebook_authorized',
				        next=request.args.get('next') or request.referrer or None,_external=True))
	return render_template('login.html',
				titile='Sign In'
				,form=form,
				providers=app.config['OPENID_PROVIDERS'])
@app.route('/login/authrized')
@facebook.authorized_handler
def facebook_authorized(resp):
	print resp
	if resp is None:
		flash (' Access denied')
		return redirect(url_for('login'))
	session['oauth_token']=(resp['access_token'],'')
	me = facebook.get('/me')
	email=me.data['email']
	name=me.data['email'].split('@')[0]
	user=User.query.filter_by(email=email).first()
	if user.nickname != name:
		print "nickname is"+user.nickname+"name is"+name
		db.session.query(User).filter(User.email==email).\
				update({User.nickname:name},synchronize_session=False)
		print "not same"
		db.session.commit()
	if user is None:
		user=User(nickname=name,email=email)
		db.session.add(user)
		db.session.commit()
	login_user(user,remember=True)
	return redirect(request.args.get('next') or url_for('index'))

@facebook.tokengetter
def get_facebook_oauth_token():
	return session.get('oauth_token')
@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email=="":
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))
	user=User.query.filter_by(email=resp.email).first()
	if user is None:
		nickname=resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		user = User(nickname=nickname, email=resp.email)
		db.session.add(user)
		db.session.commit()
	remember_me=False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me',None)
	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

