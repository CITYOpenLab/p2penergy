###########
# imports #
###########

import os
import json
import arrow
import requests
import sseclient
from celery import Celery
from models import db, Event
from flask import current_app as app

#############
# functions #
#############

def save_event_from_dict(dict):
    event = Event()
    for key, value in dict.items():
        if key == "published_at":
            setattr(event, key, arrow.get(value).datetime)
        else:
            setattr(event, key, value)
    db.session.add(event)
    db.session.commit()

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
