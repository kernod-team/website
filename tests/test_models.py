import unittest

from app import create_app, db
from app.models import User, Role


class ModelsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_role(self):
        r = Role(
            name='dummy',
            description='dummy'
        )
        db.session.add(r)
        db.session.commit()

        self.assertIsNotNone(
            Role.query.filter_by(name='dummy').first()
        )

    def test_user(self):
        u = User(
            username='john',
            email='john@example.com',
            password='cat',
        )
        db.session.add(u)
        db.session.commit()

        self.assertIsNotNone(
            User.query.filter_by(email='john@example.com').first()
        )
        with self.assertRaises(AttributeError):
            u.password
        self.assertTrue(u.verify('cat'))
        self.assertFalse(u.verify('dog'))

    def test_user_role(self):
        r = Role(
            name='dummy',
            description='dummy'
        )
        db.session.add(r)
        db.session.commit()

        u = User(
            username='john',
            email='john@example.com',
            password='cat',
        )
        db.session.add(u)
        db.session.commit()


