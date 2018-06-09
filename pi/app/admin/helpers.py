###########
# imports #
###########

import os
import json
import arrow

# making requests
import requests
import sseclient

# background jobs
from app import celery

# database
from app import db
import app.models
from app.models import models

# flask extensions
from flask import current_app

@celery.task
def get_sse(product_slug):
    url = "https://api.particle.io/v1/products/{}/events?access_token={}".format(product_slug, current_app.config["PARTICLE_ACCESS_TOKEN"])
    response = requests.get(url, stream=True)
    client = sseclient.SSEClient(response)
    for event in client.events():
        event_name = event.event
        event_data = json.loads(event.data)
        db_event = models.Event(name=event_name)
        for key, value in event_data.items():
            if key != "published_at":
                setattr(db_event, key, value)
            else:
                published_at = arrow.get(value).datetime
                setattr(db_event, key, published_at)
        db.session.add(db_event)
        db.session.commit()
