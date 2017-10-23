import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(64)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.elasticemail.com'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    KERNOD_MAIL_SUBJECT_PREFIX = '[Kernod]'
    KERNOD_ADMIN = os.environ.get('KERNOD_ADMIN')
    KERNOD_POSTS_PER_PAGE = 20
    KERNOD_FOLLOWERS_PER_PAGE = 50
    KERNOD_COMMENTS_PER_PAGE = 30
    KERNOD_CATALOGS = [
        'Mathematics',
        'Computer Science',
        'Statistics'
    ]

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECURITY_TOKEN_MAX_AGE = 30 * 24 * 3600
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
