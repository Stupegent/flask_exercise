class Config(object):
 pass
class ProdConfig(Config):
 pass
class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///achour.db"
    SQLALCHEMY_ECHO = True