import os
import sys
import requests

# database models (later)
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import joinedload
# from flask_migrate import Migrate

# parse requests (looks inside query, form and JSON data)
from datetime import date, datetime
from webargs import validate, fields, ValidationError
from webargs.flaskparser import parser, abort, use_args

# Flask web framework
from flask import Flask, g, request, jsonify, render_template

# CONNECTIONS
app = Flask(__name__)                   # Flask
# app.config.from_object(Config)          # config

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(threaded=True, port=80)
