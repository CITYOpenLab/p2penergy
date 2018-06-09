from app import db
from datetime import datetime

class User(db.Model):
    ## basic
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), index=True,
                         unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    admin = db.Column(db.Boolean(), default=False, nullable=False)

    def __repr__(self):
        return '<User {} {}>'.format(self.username, self.id)

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
