from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.validators import Required, Email, EqualTo
from flask.ext.wtf.file import FileField, FileAllowed, FileRequired
from app import category_img

class LoginForm(Form):
	email = TextField('E Mail', validators = [Required(), Email()])
	password = PasswordField('Password', validators = [Required()])
	remember_me = BooleanField('Remember Me',default = False)

class AddUserForm(Form):
	name = TextField('Name', validators = [Required()])
	user_email = TextField('E Mail', validators = [Required(), Email()])
	password = PasswordField('New Password', validators = [EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Confirm Password')
	role = SelectField('Role', choices = [('0','User'), ('1','Admin')])
	add_user = SubmitField('Done')
	add_shop = SubmitField('Continue to Add Shop')

class AddShopForm(Form):
	name = TextField('Name', validators = [Required()])
	
class AddCategoryForm(Form):
	name = TextField('Name', validators = [Required()])
	description = TextAreaField()
	image = FileField('Image', validators=[FileAllowed(category_img, message = "Images Only!!")])
