from flask import current_app
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from sqlalchemy.exc import IntegrityError

from app import db
from app.services import Service
from app.services.security.models import User, Role


class UserService(Service, User, UserMixin):
    @staticmethod
    def create_user(**kwargs):
        u = user_datastore.create_user(**kwargs)
        db.session.add(u)
        db.session.commit()
        return u


class RoleService(Service, Role, RoleMixin):
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
            nobody = user_datastore.create_role(
                name='%s_nobody' % catalog_abbr,
                catalog=catalog_abbr,
                description='nobody on %s' % catalogs[catalog_abbr]
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
            db.session.add_all([nobody, mod, admin])
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
