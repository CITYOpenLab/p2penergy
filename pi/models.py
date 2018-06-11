###########
# imports #
###########

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import Schema, fields
db = SQLAlchemy()

##########
# models #
##########

class Event(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    coreid = db.Column(db.String())
    data = db.Column(db.String())
    productID = db.Column(db.String())
    public = db.Column(db.Boolean())
    published_at = db.Column(db.DateTime(), default=datetime.utcnow)
    ttl = db.Column(db.Integer())
    userid = db.Column(db.String())
    version = db.Column(db.Integer())

    def __repr__(self):
        return '<Event {} {}>'.format(self.name, self.id)

class EventSchema(ModelSchema):
    class Meta:
        model = Event
