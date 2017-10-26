import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') \
                 or 'The-Platinum-Yendorian-Express-Card'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.elasticemail.com'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = 'no-reply@kernod.cn'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    SECURITY_BLUEPRINT_NAME = 'auth'
    SECURITY_PASSWORD_SALT = SECRET_KEY
    SECURITY_EMAIL_SENDER = 'no-reply@kernod.cn'
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_TOKEN_MAX_AGE = 30 * 24 * 3600

    KERNOD_MAIL_SUBJECT_PREFIX = '[Kernod]'
    KERNOD_ADMIN = os.environ.get('KERNOD_ADMIN')
    KERNOD_POSTS_PER_PAGE = 20
    KERNOD_FOLLOWERS_PER_PAGE = 50
    KERNOD_COMMENTS_PER_PAGE = 30
    KERNOD_CATALOGS = {
        'math': 'Mathematics',
        'cs': 'Computer Science',
        'stat': 'Statistics',
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECURITY_CONFIRMABLE = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SERVER_NAME = 'test-server-name'
    SECURITY_CONFIRMABLE = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'prod-data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
