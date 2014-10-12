from flask import render_template, flash, redirect, url_for, g, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, lm, db, category_img
from forms import LoginForm, AddUserForm, AddCategoryForm
from models import User, ROLE_USER, ROLE_ADMIN, Category

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user
	return render_template("index.html", 
							title = 'Home',
							user = user)

@app.route('/login', methods = ['GET','POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if request.method == 'POST' and form.validate_on_submit():
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

@app.route('/adduser', methods = ['GET','POST'])
@login_required
def add_user():
	if g.user.is_authenticated() and g.user.is_admin():
		form = AddUserForm()
		if request.method == 'POST' and form.validate_on_submit():
			user_email = form.user_email.data
			registered_user = User.query.filter_by(user_email = user_email).first()
			if registered_user is not None:
				flash("The email already exists" , "error")
				return redirect(url_for('add_user'))
			password = 'admin' if form.password.data == '' else form.password.data
			user = User(form.name.data, form.user_email.data, password, form.role.data)
			db.session.add(user)
			db.session.commit()
			flash("Added User : " + form.name.data + " with Email : " + form.user_email.data + ", password : " + password + ", role : " + form.role.data)
			if form.add_user.data:
				return redirect(url_for('index'))
			else:
				return redirect(url_for('test'))
		return render_template("addUser.html",
			title = "Add User",
			form = form)
	flash("You are not authorised to view the page")
	return redirect(url_for('index'))

@app.route('/addcategory', methods = ['GET','POST'])
@login_required
def add_category():
	if g.user.is_authenticated() and g.user.is_admin():
		form = AddCategoryForm()
		if request.method == 'POST' and form.validate_on_submit():
			name = form.name.data
			existing = Category.query.filter_by(name = name).first()
			if existing is not None:
				flash("Category name already exists")
				return redirect(url_for('add_category'))
			description = form.description.data
			image = request.files['image']
			image_filename = image.filename if image.filename == '' else category_img.save(image)
			category = Category(name, description, image_filename)
			db.session.add(category)
			db.session.commit()
			flash('Added Category with name : ' + name + ', description : ' + description + ', image : ' + image_filename)
			return redirect(url_for('index'))
		return render_template("addCategory.html",
			title = "Add Category",
			form = form)
	flash("You are not authorised to view the page")
	return redirect(url_for('index'))

@app.route('/test')
@login_required
def test():
	return "Hello World"

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