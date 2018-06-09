###########
# imports #
###########

# blueprint for routing
from app.admin import bp

# core
import os
import json

# database models and schemas
from app import db
import app.models
from app.models import models, schemas
from sqlalchemy import or_, and_, desc, asc, text

# parse requests
from webargs import validate, fields, ValidationError
from webargs.flaskparser import parser, abort, use_args
import requests
import sseclient

# flask extensions
from flask import (
    jsonify, render_template, request, redirect, url_for, current_app)

# helper functions
from .helpers import get_sse

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
