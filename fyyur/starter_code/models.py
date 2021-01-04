
from app import db
from datetime import datetime
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website=db.Column(db.String(120))
    seeking_talent=db.Column(db.Boolean, nullable=False, default=False)
    seeking_description=db.Column(db.String())
    genres = db.Column(db.ARRAY(db.String()))
    shows = db.relationship('Show', backref='Venue', lazy=True)

    def __repr__(self):
       return f'<Venue: {self.id}, name: {self.name}, city: {self.city}, state: {self.state}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website=db.Column(db.String(120))
    seeking_description=db.Column(db.String())
    shows = db.relationship('Show', backref='artists', lazy=True)
    def __repr__(self):
       return f'<Artist: {self.id}, name: {self.name}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artists_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
 
    def __repr__(self):
       return f'<Show: {self.id}, venue_id: {self.venue_id}, artists_id: {self.artists_id}, start_time: {self.start_time}>'



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.