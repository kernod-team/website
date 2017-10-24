import unittest

from app import create_app, db
from flask_security.utils import verify_password
from app.services.security import UserService, RoleService, user_datastore


class ModelsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        RoleService.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_role(self):
        r = RoleService.create_role(
            name='dummy',
            description='dummy'
        )

        self.assertIsNotNone(r)
        self.assertEqual(
            RoleService.query.filter_by(name='dummy').first(), r
        )


    def test_user(self):
        u = UserService.create_user(
            username='john',
            email='john@example.com',
            password='cat',
        )

        self.assertIsNotNone(u)
        self.assertEqual(
            UserService.query.filter_by(email='john@example.com').first(), u
        )
        self.assertTrue(verify_password(u.password, 'cat'))
        self.assertFalse(verify_password(u.password, 'dog'))


    def test_user_role(self):
        r = RoleService.create_role(
            name='dummy',
            description='dummy'
        )
        u = UserService.create_user(
            username='john',
            email='john@example.com',
            password='cat'
        )

        user_datastore.add_role_to_user(u, r)
        self.assertEqual(r.users.all(), [u])
        self.assertEqual(u.roles.all(), [r])
