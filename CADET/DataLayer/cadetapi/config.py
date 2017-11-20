""" This is the config file for this web server. the Flask 'app' can used any
    of the configs below by using:
    app.config.from_object(config_name)
    More information on configuration files can be found at:
    http://flask-sqlalchemy.pocoo.org/2.3/config/
    http://flask.pocoo.org/docs/0.12/config/
"""

from os import path
import tempfile

class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        path.join(path.pardir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SERVER_NAME = 'www.cadet.api'
    DEBUG = True

class TestConfig(Config):
    db_file = tempfile.NamedTemporaryFile()

    DEBUG = True
    DEBUG_TB_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + db_file.name

class MysqlConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://cadet:cadet@localhost/cadet'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SERVER_NAME = 'localhost'
    DEBUG = True