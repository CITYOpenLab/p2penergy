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
        return '<User {}>'.format(self.username)
