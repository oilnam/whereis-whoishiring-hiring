import os

class BaseConfiguration(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # sqlite
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    # mysql
    SQLALCHEMY_DATABASE_URI = 'mysql://whoishiring:your-passwd-here@localhost/whoishiring'

    DEBUG = False
    SECRET_KEY = 'iwhishyouwherehere'
    CACHE_TYPE = 'simple'

class TestConfiguration(BaseConfiguration):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
