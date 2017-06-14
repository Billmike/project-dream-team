from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Employee(UserMixin, db.Model):
	"""docstring for Employee"""
	__tablename__ = 'employees'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60), index=True, unique=True)
	username = db.Column(db.String(60), index=True, unique=True)
	first_name = db.Column(db.String(60), index=True)
	last_name = db.Column(db.String(60), index=True)
	password_hash = db.Column(db.String(128))
	department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	is_admin = db.Column(db.Boolean, default=False)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<Employee: {}>'.format(self.username)

@login_manager.user_loader
def load_user(user_id):
	return Employee.query.get(int(user_id))

class Department(db.Model):
	"""docstring for Department"""
	__tablename__ = 'departments'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(200))
	employees = db.relationship('Employee', backref='department', lazy='dynamic')

	def __repr__(self):
		return '<Department: {}>'.format(self.name)

class Role(db.Model):
	"""docstring for Role"""
	__tablename__ = 'roles'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(300))
	employees = db.relationship('Employee', backref='role', lazy='dynamic')

	def __repr__(self):
		return '<Role: {}>'.format(self.name)
