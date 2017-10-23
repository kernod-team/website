from itertools import accumulate
from operator import or_
from enum import IntFlag, auto
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError

from app import db, login_manager


class RoleUser(db.Model):
    __tablename__ = 'roles_users'
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('users.id'),
        primary_key=True
    )
    role_id = db.Column(
        db.Integer(),
        db.ForeignKey('roles.id'),
        primary_key=True
    )
    operator = db.Column(db.Integer(), db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(80), index=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    roles = db.relationship(
        'RoleUser', foreign_keys=[RoleUser.user_id],
        backref=db.backref('user', lazy='joined'),
        lazy='dynamic'
    )

    def can(self, permission):
        return

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def verify(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %d>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class NobodyPermission(IntFlag):
    ASK = auto()
    ANSWER = auto()
    COMMENT = auto()
    FOLLOW = auto()
    VOTE_UP = auto()
    VOTE_DOWN = auto()


class CommentModPermission(IntFlag):
    EDIT_COMMENT = auto()
    DELETE_COMMENT = auto()


class PostModPermission(IntFlag):
    EDIT_POST = auto()
    DELETE_POST = auto()


class AdminPermission(IntFlag):
    SUSPEND_USER = auto()
    GRANT_MOD = auto()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(80), unique=True)
    catalog = db.Column(db.Unicode(80), unique=True)
    description = db.Column(db.UnicodeText(256))
    permissions = db.Column(db.Integer())
    users = db.relationship(
        'RoleUser', foreign_keys=[RoleUser.role_id],
        backref=db.backref('role', lazy='joined'),
        lazy='dynamic'
    )

    @staticmethod
    def insert_roles():
        for catalog in current_app.config['KERNOD_CATALOGS']:
            nobody = Role(
                name='nobody',
                catalog=catalog,
                description='nobody',
                permissions=accumulate(NobodyPermission, or_)
            )
            mod = Role(
                name='mod',
                catalog=catalog,
                description='moderator',
                permissions=accumulate(ModPermission, or_)
            )
            admin = Role(
                name='admin',
                catalog=catalog,
                description='administrator',
                permissions=accumulate(AdminPermission, or_)
            )
            db.session.add_all([nobody, mod, admin])
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Role %d>' % self.id
