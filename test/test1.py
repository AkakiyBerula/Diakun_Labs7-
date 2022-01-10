import unittest
from flask import url_for
from flask_login import current_user
from flask import request
from flask_testing import TestCase

from app import db, create_app
from app.auth.models import User


class BaseTestCase(TestCase):
    def create_app(self):
        self.baseURL = "http://diakun_host:8000/"
        return create_app('test')

    def setUp(self):
        db.create_all()
        user = User(username="kennyKing", email="kenny@gmail.com", password="password")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):

    def test_main(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_if(self):
        response = self.client.get('/if', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_for(self):
        response = self.client.get('/for', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_basic_form(self):
        response = self.client.get('/form_cabinet/basic_form', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_form_cabinet(self):
        response = self.client.get('/form_cabinet/form_cabinet', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('/auth/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get('/auth/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_main_route_requires_login(self):
        response = self.client.get('/auth/account', follow_redirects=True)
        self.assertIn(b'Remember Me', response.data)


class UserViewsTests(BaseTestCase):

    def test_login_loads(self):
        response = self.client.get('/auth/login')
        self.assertIn(b'Remember Me', response.data)



    def test_correct_register(self):
        with self.client:
            response = self.client.post(url_for('auth.register'),
                data=dict(email="nikita_yaroslavov@gmail.com",
                          username="iamnikita",
                          password1="mypassword",
                          password2="mypassword"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)

    def test_correct_register_login(self):
        with self.client:
            response = self.client.post(url_for('auth.register'),
                data=dict(email="gesteen@gmail.com",
                          username="GARAN",
                          password1="calebkonley_withAK",
                          password2="calebkonley_withAK"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)

    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=dict(email="gesteen34@gmail.com", password="calebkonley_withAK"),
                follow_redirects=True
            )
            self.assertTrue(current_user.is_active)
            self.assert_200(response)

    def test_incorrect_login(self):
        response = self.client.post(
            '/auth/login',
            data=dict(email="Jack_Swagger_God", password="Впустіть мене"),
            follow_redirects=True
        )


if __name__ == '__main__':
    unittest.main()