import unittest

from flask_security.utils import hash_password, verify_password

from app import create_app, db
from app.auth.models import User, Role, user_datastore


class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_role(self):
        r = Role.create_role(
            name='dummy',
            description='dummy'
        )

        self.assertIsNotNone(r)
        self.assertEqual(
            Role.query.filter_by(name='dummy').first(), r
        )

    def test_user(self):
        u = User.create_user(
            username='john',
            email='john@example.com',
            password=hash_password('cat'),
        )

        self.assertIsNotNone(u)
        self.assertEqual(
            User.query.filter_by(email='john@example.com').first(), u
        )
        self.assertTrue(verify_password('cat', u.password))
        self.assertFalse(verify_password('Cat', u.password))
        self.assertFalse(verify_password('dog', u.password))

    def test_user_role(self):
        r = Role.create_role(
            name='dummy',
            catalog='random',
            description='dummy'
        )
        u = User.create_user(
            username='john',
            email='john@example.com',
            password=hash_password('cat')
        )

        user_datastore.add_role_to_user(u, r)
        self.assertEqual(r.users.all(), [u])
        self.assertEqual(u.roles, [r])

    def test_add_role(self):
        r = Role.create_role(
            name='dummy',
            catalog='random',
            description='dummy'
        )
        u = User.create_user(
            username='john',
            email='john@example.com',
            password=hash_password('cat')
        )

        u.add_role(r)
        self.assertEqual(r.users.all(), [u])
        self.assertEqual(u.roles, [r])

    def test_add_user(self):
        r = Role.create_role(
            name='dummy',
            catalog='random',
            description='dummy'
        )
        u = User.create_user(
            username='john',
            email='john@example.com',
            password=hash_password('cat')
        )

        r.add_user(u)
        self.assertEqual(r.users.all(), [u])
        self.assertEqual(u.roles, [r])
