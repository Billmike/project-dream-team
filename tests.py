import unittest
import os
from flask import abort, url_for
from flask_testing import TestCase
from app import create_app, db
from app.models import Employee, Department, Role

class TestBase(TestCase):
	"""docstring for TestBase"""
	def create_app(self):
		config_name = 'testing'
		app = create_app(config_name)
		app.config.update(SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sql8180116:g7h5sit9MR@sql8.freemysqlhosting.net/sql8180116')

		return app

	def setUp(self):
		db.create_all()

		#create test admin user
		admin = Employee(username="admin", password="admin2016", is_admin=True)

		#create a test non-admin user
		employee = Employee(username="test_user", password="test2016")

		db.session.add(admin)
		db.session.add(employee)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

class TestModels(TestBase):
	"""docstring for TestModels"""
	def test_employee_model(self):
		self.assertEqual(Employee.query.count(), 2)

	def test_department_model(self):
		department = Department(name="IT", description="The IT Department")

		db.session.add(department)
		db.session.commit()
		self.assertEqual(Department.query.count(), 1)

	def test_role_model(self):
		role = Role(name="CEO", description="Run the whole company")

		db.session.add(role)
		db.session.commit()
		self.assertEqual(Role.query.count(), 1)

class TestViews(TestBase):
	"""docstring for TestViews"""
	def test_homepage_view(self):
		response = self.client.get(url_for('home.homepage'))
		self.assertEqual(response.status_code, 200)

	def test_login_view(self):
		response = self.client.get(url_for('auth.login'))
		self.assertEqual(response.status_code, 200)

	def test_logout_view(self):
		target_url = url_for('auth.logout')
		redirect_url = url_for('auth.login', next=target_url)
		response = self.client.get(target_url)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, redirect_url)

	def test_dashboard_view(self):
		target_url = url_for('home.dashboard')
		redirect_url = url_for('auth.login', next=target_url)
		response = self.client.get(target_url)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, redirect_url)


	def test_admin_dashboard(self):
		target_url = url_for('home.admin_dashboard')
		redirect_url = url_for('auth.login', next=target_url)
		response = self.client.get(target_url)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, redirect_url)

	def test_departments_view(self):
		target_url = url_for('admin.list_departments')
		redirect_url = url_for('auth.login', next=target_url)
		response = self.client.get(target_url)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, redirect_url)

	def test_roles_view(self):
		target_url = url_for('admin.list_roles')
		redirect_url = url_for('auth.login', next=target_url)
		response = self.client.get(target_url)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, redirect_url)

	def test_employees_view(self):
		target_url = url_for('admin.list_employees')
		redirect_url = url_for('auth.login', next=target_url)
		response = self.client.get(target_url)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, redirect_url)

class TestErrorPages(TestBase):
	"""docstring for TestErrorPages"""
	def test_403_forbidden(self):
		@self.app.route('/403')
		def forbidden_error():
			abort(403)

		response = self.client.get('/403')
		self.assertEqual(response.status_code, 403)
		self.assertTrue("403 Error" in response.data)

	def test_404_not_found(self):
		response = self.client.get('/nothinghere')
		self.assertEqual(response.status_code, 404)
		self.assertTrue("404 Error" in response.data)

	def test_500_internal_server_error(self):
		@self.app.route('/500')
		def internal_server_error():
			abort(500)

		response = self.client.get('/500')
		self.assertEqual(response.status_code, 500)
		self.assertTrue("500 Error" in response.data)


		
		
		

if __name__ == '__main__':
	unittest.main()

		