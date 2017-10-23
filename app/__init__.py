from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config


mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from app.main import main
    app.register_blueprint(main)

    return app
