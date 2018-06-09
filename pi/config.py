import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    SQLALCHEMY_DATABASE_URI = (os.environ.get("DATABASE_URL") or
                               "sqlite:///" + os.path.join(basedir, "database.db"))
    PARTICLE_ACCESS_TOKEN = os.environ.get("PARTICLE_ACCESS_TOKEN")

class developmentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class productionConfig(Config):
    THREADED = True
