"""
SQLAlchemy models for TwitOff.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Fire(db.Model):
    """Twitter users that we pull and analyze Tweets for."""
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.NUMERIC(6,3))
    longitude = db.Column(db.NUMERIC(6,3))
    fire = db.Column(db.SmallInteger)
    # timestamp = db.Column(db.TIMESTAMP)
    

    def __repr__(self):
        return "<lat/long/fire {},{}, {}>".format(self.latitude, 
        self.longitude, self.fire)


