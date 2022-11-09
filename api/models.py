from api import db
from datetime import datetime
from sqlalchemy.sql import func


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    update_on = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"username: {self.username}, email: {self.email}"


class Museum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    established = db.Column(db.String(10), nullable=False)
    paintings = db.relationship("Painting", backref="place", lazy=True)
    sculptures = db.relationship("Sculpture", backref="place", lazy=True)
    jewelries = db.relationship("Jewelry", backref="place", lazy=True)

    def __repr__(self):
        return f"Museum('{self.name}', '{self.country}', '{self.city}')"


class Painting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    artist = db.Column(db.String(150), nullable=False)
    created = db.Column(db.String(10))
    object_place = db.Column(db.String(250))
    medium = db.Column(db.String(150))
    genre = db.Column(db.String(150))
    museum_id = db.Column(db.Integer, db.ForeignKey("museum.id"))

    def __repr__(self):
        return f"Painting('{self.title}' by '{self.artist}')"


class Sculpture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    artist = db.Column(db.String(150), nullable=False)
    created = db.Column(db.String(10))
    object_place = db.Column(db.String(250))
    material = db.Column(db.String(150))
    museum_id = db.Column(db.Integer, db.ForeignKey("museum.id"))

    def __repr__(self):
        return f"Sculpture('{self.title}' by '{self.artist}')"


class Jewelry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    created = db.Column(db.String(10))
    country = db.Column(db.String(100))
    object_place = db.Column(db.String(250))
    medium = db.Column(db.String(150))
    museum_id = db.Column(db.Integer, db.ForeignKey("museum.id"))

    def __repr__(self):
        return f"Jewelry('{self.title}' from '{self.made_in}')"
