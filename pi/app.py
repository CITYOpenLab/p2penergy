###########
# imports #
###########

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, desc, asc, text
from flask import (jsonify, render_template, request,
                   redirect, url_for, current_app)
from flask_migrate import Migrate
from flask_mqtt import Mqtt
from flask_rq2 import RQ
from config import Config

##############
# initialize #
##############

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mqtt = Mqtt(app)
rq = RQ(app)

##################
# delayed import #
##################

from models import Event, EventSchema
from helpers import save_event_from_dict

#########
# views #
#########

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/events", methods=["GET"])
def get_events():
    query = Event.query
    query = query.order_by(desc(text("published_at")))
    items = query.all()
    if items:
        schema = EventSchema()
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
    save_event_from_dict(data)
    
