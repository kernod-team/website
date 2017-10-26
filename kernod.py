import os

from app import create_app, db
from app.auth.models import User, Role, user_datastore

app = create_app(os.getenv('KERNOD_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Role=Role,
        user_datastore=user_datastore,
    )


@app.cli.command()
def test():
    import unittest
    tests = unittest.defaultTestLoader.discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
