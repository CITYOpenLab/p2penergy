###########
# imports #
###########

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from flask_migrate import Migrate
from flask_mqtt import Mqtt
from config import Config

# Create the instances of the Flask extensions in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.
db = SQLAlchemy()
migrate = Migrate()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
mqtt = Mqtt()

######################################
#### application factory function ####
######################################

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    initialize_extensions(app)
    register_blueprints(app)
    return app

##########################
#### helper functions ####
##########################

def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    mqtt.init_app(app)
    # celery.conf.update(app.config)

def register_blueprints(app):
    from .admin import bp as admin_blueprint
    app.register_blueprint(admin_blueprint)
