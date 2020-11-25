
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask import Flask
from sqlalchemy import Integer, ForeignKey, Column, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
# Import local database URI from Config File
from config import SQLALCHEMY_DATABASE_URI
from extensions import csrf
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
csrf.init_app(app)
db = SQLAlchemy(app)
# Creating an instance of the Migrate class
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database <Done>
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.<Done>
# Association table Show Definition
Show = db.Table('show', db.Model.metadata,
                db.Column('venue_id', db.Integer, db.ForeignKey(
                    'venue.id'), primary_key=True),
                db.Column('artist_id', db.Integer, db.ForeignKey(
                    'artist.id'), primary_key=True),
                db.Column('start_time', db.DateTime, primary_key=True))
# ondelete = "CASCADE"

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate <Done>
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    genres = db.Column(db.ARRAY(db.String()))
    seeking_description = db.Column(db.String(500))
    show_artist = db.relationship('Artist', secondary=Show, backref=db.backref(
        'venues', lazy='dynamic', cascade="all, delete"))
    # Venue = relationship('Venue', backref=backref(
    #     "shows", cascade="all,delete"))

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))  # To query and add data easier
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate <Done>
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))



