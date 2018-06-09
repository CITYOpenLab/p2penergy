import os

class developmentConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

class productionConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    THREADED = True
