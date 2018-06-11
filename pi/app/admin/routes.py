###########
# imports #
###########

import os
import json
import requests
import sseclient                                            # server sent events
import app.models                                           # database models
from app.admin import bp                                    # blueprint
from app import db                                          # database
from app.models import models, schemas
from sqlalchemy import or_, and_, desc, asc, text
from webargs import validate, fields, ValidationError       # parsing requests
from webargs.flaskparser import parser, abort, use_args
from flask import (jsonify, render_template, request,       # flask functions
                   redirect, url_for, current_app)
from app import mqtt                                        # mqtt
from .helpers import get_sse                                # helper functions

##########
# routes #
##########

@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@bp.route("/collect", methods=["GET"])
def collect():
    get_sse.delay("p2p-energy-v100")
    return "started collection"

@bp.route("/get-events", methods=["GET"])
def get_events():
    query = models.Event.query
    query = query.order_by(desc(text("published_at")))
    items = query.all()
    if items:
        schema = schemas.Event()
        result = schema.dump(items[0:5], many=True)
        return jsonify(result.data)
    else:
        return jsonify([])

########
# mqtt #
########

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('testtopic/hello')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)
    print(message)
