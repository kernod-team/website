from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask import current_app
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore

from app import db


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.Unicode(80), index=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    roles = db.relationship(
        'Role', secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'),
    )

    def add_role(self, role):
        user_datastore.add_role_to_user(self, role)
        db.session.add_all([self, role])
        db.session.commit()

    @staticmethod
    def create_user(**kwargs):
        u = user_datastore.create_user(**kwargs)
        db.session.add(u)
        db.session.commit()
        return u

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):  # pragma: no cover
        return '<User %s>' % self.id


class Role(RoleMixin, db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(80), unique=True)
    catalog = db.Column(db.Unicode(80))
    description = db.Column(db.UnicodeText(256))

    def add_user(self, user):
        user_datastore.add_role_to_user(user, self)
        db.session.add_all([self, user])
        db.session.commit()

    @staticmethod
    def create_role(**kwargs):
        r = user_datastore.create_role(**kwargs)
        db.session.add(r)
        db.session.commit()
        return r

    @staticmethod
    def insert_roles():
        catalogs = current_app.config['KERNOD_CATALOGS']
        for catalog_abbr in catalogs:
            member = user_datastore.create_role(
                name='%s_member' % catalog_abbr,
                catalog=catalog_abbr,
                description='member on %s' % catalogs[catalog_abbr]
            )
            mod = user_datastore.create_role(
                name='%s_mod' % catalog_abbr,
                catalog=catalog_abbr,
                description='moderator on %s' % catalogs[catalog_abbr]
            )
            admin = user_datastore.create_role(
                name='%s_admin' % catalog_abbr,
                catalog=catalog_abbr,
                description='administrator on %s' % catalogs[catalog_abbr]
            )
            db.session.add_all([member, mod, admin])
            try:
                db.session.commit()
            except IntegrityError as e:  # pragma: no cover
                import warnings
                warnings.warn(str(e))
                db.session.rollback()

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):  # pragma: no cover
        return '<Role %s>' % self.id


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
