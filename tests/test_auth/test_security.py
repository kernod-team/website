from flask import url_for
from flask_security.decorators import login_required
from flask_security.utils import hash_password

from app.auth.models import User
from tests.test_bases import ViewBaseTestCase


class TestLogin(ViewBaseTestCase):
    """
    Normally I don't test code written by others, but I don't trust Flask-
    Security very well.
    """
    def setUp(self):
        super().setUp()

        @self.app.route('/test-view')
        @login_required
        def test_view():
            return 'login_pass'

        self.app.config['SECURITY_POST_LOGIN_VIEW'] = 'test_view'

    def test_login_view_accessible(self):
        resp = self.client.get(url_for('auth.login'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Login</h1>', resp.get_data(as_text=True))

    def test_login_view_redirect(self):
        resp = self.client.get(url_for('test_view'))
        self.assertEqual(resp.status_code, 302)

    def test_login_view_redirect_follow(self):
        resp = self.client.get(url_for('test_view'), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Login</h1>', resp.get_data(as_text=True))

    def test_login_correct(self):
        User.create_user(
            username='john',
            email='john@example.com',
            password=hash_password('cat')
        )
        correct_credential = {
            'email': 'john@example.com',
            'password': 'cat',
            'remember': 'y'
        }

        resp = self.client.post(
            url_for('auth.login'),
            data=correct_credential
        )
        self.assertEqual(resp.status_code, 302)
        self.assertIn(
            '<a href="/test-view">/test-view</a>',
            resp.get_data(as_text=True)
        )

    def test_login_correct_follow(self):
        User.create_user(
            username='john',
            email='john@example.com',
            password=hash_password('cat')
        )
        correct_credential = {
            'email': 'john@example.com',
            'password': 'cat',
            'remember': 'y'
        }

        resp = self.client.post(
            url_for('auth.login'),
            data=correct_credential,
            follow_redirects=True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn('login_pass', resp.get_data(as_text=True))

    def test_login_incorrect(self):
        User.create_user(
            username='john',
            email='john@example.com',
            password=hash_password('cat')
        )
        incorrect_credential = {
            'email': 'john@example.com',
            'password': 'dog',
            'remember': 'y'
        }
        resp = self.client.post(
            url_for('auth.login'),
            data=incorrect_credential
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Login</h1>', resp.get_data(as_text=True))

    def test_login_incorrect_follow(self):
        User.create_user(
            username='john',
            email='john@example.com',
            password=hash_password('cat')
        )
        incorrect_credential = {
            'email': 'john@example.com',
            'password': 'dog',
            'remember': 'y'
        }
        resp = self.client.post(
            url_for('auth.login'),
            data=incorrect_credential,
            follow_redirects=True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<li>Invalid password</li>', resp.get_data(as_text=True))
