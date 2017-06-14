from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		employee = Employee(email=form.email.data, username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, password=form.password.data)
		db.session.add(employee)
		db.session.commit()
		flash('Registration successful.')

		return redirect(url_for('auth.login'))

	return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		#check if the employee already exists in the DB and if password provided is a match
		employee = Employee.query.filter_by(email=form.email.data).first()
		if employee is not None and employee.verify_password(form.password.data):

			#login the user
			login_user(employee)

			if employee.is_admin:
				return redirect(url_for('home.admin_dashboard'))

			else:
			    #redirect user to dashboard after login
			    return redirect(url_for('home.dashboard'))

		else:
			flash('Invalid email or password combination')
	return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
	logout_user()

	flash('Logout successfull')

	return redirect(url_for('auth.login'))