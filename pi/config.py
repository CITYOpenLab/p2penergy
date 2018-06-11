###########
# imports #
###########

import os
basedir = os.path.abspath(os.path.dirname(__file__))

##################
# configurations #
##################

class Config():
    # celery
    CELERY_RESULT_BACKEND = "redis://localhost:6379"
    CELERY_BROKER_URL = "redis://localhost:6379"
    # particle
    PARTICLE_ACCESS_TOKEN = os.environ.get("PARTICLE_ACCESS_TOKEN")
    # sqlalchemy database
    SQLALCHEMY_DATABASE_URI = (os.environ.get("DATABASE_URL") or
                               "sqlite:///" + os.path.join(basedir, "database.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # mqtt
    MQTT_BROKER_URL = os.environ.get("MQTT_BROKER_URL") or "broker.hivemq.com"
    MQTT_BROKER_PORT = os.environ.get("MQTT_BROKER_PORT") or 1883               # default port for non-TLS
    MQTT_TLS_ENABLED = os.environ.get("MQTT_TLS_ENABLED") or False
    MQTT_KEEPALIVE = os.environ.get("MQTT_KEEPALIVE") or 5                      # ping broker 5 seconds
    MQTT_USERNAME = os.environ.get("MQTT_USERNAME") or ''
    MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD") or ''
    # other
    THREADED = True
    
