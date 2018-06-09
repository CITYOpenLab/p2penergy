from . import models

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import Schema, fields, pprint

class User(ModelSchema):
    class Meta:
        model = models.User

class Event(ModelSchema):
    class Meta:
        model = models.Event
