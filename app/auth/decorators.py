from flask_security.decorators import roles_required, roles_accepted


def catalog_roles_required(catalog, roles):
    """Decorator which specifies that a user must have all the specified roles
    in the specified catalog. Example::

        @app.route('/dashboard')
        @catalog_roles_required('news', ['admin', 'editor'])
        def dashboard():
            return 'Dashboard - News'

    The current user must have both the `admin` role and `editor` role in the
    `news` catalog in order to view the page.

    :param catalog: The catalog to which roles belong.
    :param roles: The required roles.
    """
    def wrapper(fn):
        catalog_roles = ['%s_%s' % (catalog, r) for r in roles]
        return roles_required(*catalog_roles)(fn)
    return wrapper


def catalog_roles_accepted(catalog, roles):

    """Decorator which specifies that a user must have at least one of the
    specified roles in the specified catalog. Example::

        @app.route('/create_post')
        @catalog_roles_required('news', ['editor', 'author'])
        def create_post():
            return 'Create Post - News'

    The current user must have either the `editor` role or `author` role in
    the `news` catalog in order to view the page.

    :param catalog: The catalog to which roles belong.
    :param roles: The possible roles.
    """
    def wrapper(fn):
        catalog_roles = ['%s_%s' % (catalog, r) for r in roles]
        return roles_accepted(*catalog_roles)(fn)
    return wrapper
