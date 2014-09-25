from flask import render_template, flash, redirect, url_for, g, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, lm
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN

@app.route('/')
@app.route('/index')
@login_required
def index():
	user= g.user
	return render_template("index.html", 
							title = 'Home',
							user = user)

@app.route('/login', methods = ['GET','POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		remember_me = form.remember_me.data
		user_email = form.email.data
		password = form.password.data
		registered_user = User.query.filter_by(user_email=user_email).first()
		if registered_user is None or not registered_user.verify_password(password):
			flash("The email or password you entered is incorrect." , "error")
			return redirect(url_for('login'))
		login_user(registered_user, remember = remember_me)
		flash("Login requested for Email : " + form.email.data + ", password : " + form.password.data + ", remember me : " + str(form.remember_me.data))
		return redirect(request.args.get('next') or url_for('index'))
	return render_template("login.html", 
		title = "Log In",
		form = form)


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for("index"))