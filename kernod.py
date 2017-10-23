import os
from flask_migrate import Migrate

from app import create_app, db
from app.models import User, Role, RoleUser

app = create_app(os.getenv('KERNOD_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Role=Role,
        RoleUser=RoleUser
    )


@app.cli.command()
def test():
    import unittest
    tests = unittest.defaultTestLoader.discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
