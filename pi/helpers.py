###########
# imports #
###########

import os
import json
import arrow
import requests
import sseclient
from app import app
from app import db
from app import rq
from models import Event

#############
# functions #
#############

def save_event_from_json(json):
    data = json.loads(json)
    save_event_from_dict(data)

def save_event_from_dict(dict):
    event = Event()
    for key, value in dict.items():
        if key == "published_at":
            setattr(event, key, arrow.get(value).datetime)
        else:
            setattr(event, key, value)
    db.session.add(event)
    db.session.commit()

####################
# background tasks #
####################

@rq.job
def get_particle_event_stream(product_slug):
    url = "https://api.particle.io/v1/products/{}/events?access_token={}".format(
        product_slug, app.config["PARTICLE_ACCESS_TOKEN"])
    response = requests.get(url, stream=True)
    client = sseclient.SSEClient(response)
    for event in client.events():
        # event_name = event.event
        save_event_from_json(event.data)
