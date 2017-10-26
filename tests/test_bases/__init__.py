import unittest

from flask import url_for
from flask_security.utils import hash_password

from app import create_app, db
from app.auth.models import User, Role


class ViewBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)
        self.test_user = {
            'email': 'john@example.com',
            'password': hash_password('cat')
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _add_role_name_to_user(self, user, role_name):
        role = Role.query.filter_by(name=role_name).first()
        self.assertIsNotNone(role)
        user.add_role(role)

    def _log_in_as(self, user):
        roles = user.get('roles') or []
        email, password = user['email'], user['password']
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User.create_user(
                username=email,
                email=email,
                password=hash_password(password)
            )
        for role in roles:
            self._add_role_name_to_user(user, role)
        resp = self.client.post(url_for('auth.login'), data={
            'email': email,
            'password': password,
            'remember': 'y'     # Not sure why it's required, but some
                                # test cases having follow_redirects=True
                                # fails without it.
        })
        self.assertEqual(resp.status_code, 302)


class DecoratorBaseTestCase(ViewBaseTestCase):
    def setUp(self):
        super().setUp()

        @self.app.route('/test-view')
        @self.get_decorator_in_question()
        def test_view():
            return 'decorator_pass'

    def get_decorator_in_question(self):
        """
        Return the decorator to test. Example::

            def get_decorator_in_question(self):
                return catalog_roles_required('math', ['member', 'mod'])

        :return: The decorator to test
        """
        raise NotImplementedError
