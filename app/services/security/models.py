from datetime import datetime

from app import db


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class User(db.Model):
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
        backref=db.backref('user', lazy='dynamic'),
        lazy='dynamic'
    )

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return '<User %s>' % self.id


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(80), unique=True)
    catalog = db.Column(db.Unicode(80), unique=True)
    description = db.Column(db.UnicodeText(256))
    permissions = db.Column(db.Integer())
    users = db.relationship(
        'User', secondary=roles_users,
        backref=db.backref('role', lazy='dynamic'),
        lazy='dynamic'
    )

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return '<Role %s>' % self.id
