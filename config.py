import os

class BaseConfiguration(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    DEBUG = True


class TestConfiguration(BaseConfiguration):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
