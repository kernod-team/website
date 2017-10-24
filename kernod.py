import os

from app import create_app, db
from app.services.security import UserService, RoleService
from app.services.security.models import User, Role

app = create_app(os.getenv('KERNOD_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        UserService=UserService,
        RoleService=RoleService,
        User=User,
        Role=Role
    )


@app.cli.command()
def test():
    import unittest
    tests = unittest.defaultTestLoader.discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
