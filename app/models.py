from app import db
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_email = db.Column(db.String(50), index = True, unique = True)
	password_hash = db.Column(db.String(128), nullable = False)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	name = db.Column(db.String(20), default = user_email)
	registered_on = db.Column(db.DateTime)
	shops = db.relationship('Shop', backref = 'owner', lazy = 'dynamic')
	subscriptions = db.relationship('Subscription', backref = 'user', lazy = 'dynamic')

	def __init__(self, name, email, password, role):
		self.name = name
		self.user_email = email
		self.role = role
		self.hash_password(password)
		self.registered_on = datetime.utcnow()

	def __repr__(self):
		return '<User %r>' % (self.user_email)

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def is_admin(self):
		if self.role == ROLE_ADMIN:
			return True
		return False

class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(20), unique = True)
	description = db.Column(db.Text)
	image_url = db.Column(db.String(200))
	shops = db.relationship('Shop', backref = 'category', lazy = 'dynamic')

	def __init__(self, name, desc, img):
		self.name = name
		self.description = desc
		self.image_url = img

	def __repr__(self):
		return '<Category %r>' % (self.name)

class Shop(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(20))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	categories = db.Column(db.Integer, db.ForeignKey('category.id'))
	description = db.Column(db.Text)
	services = db.Column(db.String(100))
	website = db.Column(db.String(50))
	start_time = db.Column(db.Time)
	end_time = db.Column(db.Time)
	visitor_count = db.Column(db.Integer, default = 0)
	isActive = db.Column(db.Boolean, default = False)
	location = db.relationship("Location", uselist=False, backref="shop")	
	contacts = db.relationship('Contact', backref = 'shop', lazy = 'dynamic')
	holidays = db.relationship('Holiday', backref = 'shop', lazy = 'dynamic')
	images = db.relationship('Image', lazy = 'dynamic')

	def __repr__(self):
		return '<Shop %r>' % (self.name)

class Location(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)

	def __repr__(self):
		return '<Location (%r,%r)>' % (self.latitude, self.longitude)

class Contact(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
	name = db.Column(db.String(20))
	designation = db.Column(db.String(10))
	email = db.Column(db.String(50))
	phone = db.Column(db.String(50))
	mobile = db.Column(db.String(50))

class Holiday(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
	day = db.Column(db.String(10))

class Image(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
	url = db.Column(db.String(200))
	description = db.Column(db.Text)

class Subscription(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	start_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)
	fee = db.Column(db.Float)

