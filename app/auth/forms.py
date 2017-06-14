from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Employee

class RegistrationForm(FlaskForm):
	"""docstring for RegistrationForm"""
	email = StringField('Email', validators=[DataRequired(), Email()])
	username = StringField('Username', validators=[DataRequired()])
	first_name = StringField('First Name', validators=[DataRequired()])
	last_name = StringField('Last Name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
	confirm_password = PasswordField('Confirm Password')
	submit = SubmitField('Register')

	def validate_email(self, field):
		if Employee.query.filter_by(email=field.data).first():
			raise ValidationError('This email is already in use. Forgot your password?')

	def validate_username(self, field):
		if Employee.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')

class LoginForm(FlaskForm):
	"""docstring for LoginForm"""
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')
		