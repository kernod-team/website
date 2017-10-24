from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security

from config import config


mail = Mail()
db = SQLAlchemy()
migrate = Migrate(db=db)
security = Security()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app)

    from app.services.security import user_datastore
    security.init_app(app, datastore=user_datastore)

    from app.main import main
    app.register_blueprint(main)

    return app
