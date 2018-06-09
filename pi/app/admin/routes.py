###########
# imports #
###########

# blueprint for routing
from app.admin import bp

# core
import os
import pprint
import json

# database models and schemas
from app import db
import app.models
from app.models import models

# parse requests
from webargs import validate, fields, ValidationError
from webargs.flaskparser import parser, abort, use_args
import requests
import sseclient

# flask extensions
from flask import jsonify, render_template, session, g, request, redirect, url_for, current_app

##########
# routes #
##########

@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

