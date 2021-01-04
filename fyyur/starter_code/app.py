#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#


import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_wtf import FlaskForm as BaseForm
from forms import *
import sys
from flask_migrate import Migrate

#from dictutil import func
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

from models import *
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  # return babel.dates.format_datetime(date, format)
  return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


def search_artist_name(cls, search_words):
  #convert  the search words to lower case
  search_words= str(search_words).lower()
  #compare between Venue.name and search_words after  converting  the Venue.name to lower case
  results = cls.query.filter(cls.name.ilike(f'%{search_words}%')).all()
  return [{
            "id": result.id,
            "name": result.name,
            "num_upcoming_shows": db.session.query(Show).filter(Show.artists_id==result.id, Show.start_time >= datetime.now()).count()
  } for result in results]


def search_venue_name(cls, search_words):
  #convert  the search words to lower case
  search_words= str(search_words).lower()
  #compare between Venue.name and search_words after  converting  the Venue.name to lower case
  results = cls.query.filter(cls.name.ilike(f'%{search_words}%')).all()
  return [{
            "id": result.id,
            "name": result.name,
            "num_upcoming_shows": db.session.query(Show).filter(Show.venue_id==result.id, Show.start_time >= datetime.now()).count()
  } for result in results]



#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.   
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[]
  #venuesi= db.session.query(Venue.id, Venue.name, Venue.city, Venue.state).group_by(Venue.city).all()
  data=[]
  # retraive all the cities and states in the venues
  Venue_Cities= db.session.query(Venue.city, Venue.state).distinct().all()
  for Cityi in Venue_Cities:
    # group the data depond on the  venues cities and states .
    venuesi= db.session.query(Venue.id, Venue.name).filter(Venue.city==Cityi.city, Venue.state==Cityi.state).all()
    venuesiSET=[]
    for v in venuesi:
      venuesiSET.append({
        "id": v.id,
        "name": v.name, 
          #      the num_shows aggregated based on number of upcoming shows per venue
        "num_upcoming_shows": db.session.query(Show).filter(Show.venue_id==v.id, Show.start_time >= datetime.now()).count()
      })
    data.append({
      "city": Cityi.city,
      "state": Cityi.state, 
      "venues": venuesiSET
    })



  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
   # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  data=[] 
  search_words=request.form.get('search_term', '')
  data=search_venue_name(Venue, search_words)
  response={
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data=[]
  # retraive only the passing venue_id 
  VenueI= db.session.query(Venue).filter(Venue.id==venue_id).first()
  # retraive info of the show obj of the passing venue_id and the venue's past shows 
  past_shows_Venues= db.session.query(Show).filter(Show.venue_id==venue_id, Show.start_time <= datetime.now()).all()
  # count the past shows
  past_shows_count= db.session.query(Show).filter(Show.venue_id==venue_id, Show.start_time <= datetime.now()).count()
  # retraive info of the show obj of the passing venue_id and the venue's upcoming shows 
  upcoming_shows_Venues= db.session.query(Show).filter(Show.venue_id==venue_id, Show.start_time >= datetime.now()).all()
  # count the upcoming shows
  upcoming_shows_count=db.session.query(Show).filter(Show.venue_id==venue_id, Show.start_time >= datetime.now()).count()
  #  build the artists where their shows played in the past 
  past_shows_SET=[]
  for past_shows in past_shows_Venues:
    Artisti=db.session.query(Artist).filter(Artist.id==past_shows.artists_id).first()
    past_shows_SET.append({
      "artist_id": Artisti.id,
      "artist_name": Artisti.name, 
      "artist_image_link": Artisti.image_link,
      "start_time": past_shows.start_time.strftime("%Y-%m-%d %H:%M:%S") 
    })
    #  build the artists where their shows consider as  upcoming shows
  upcoming_shows_SET=[]
  for upcoming_shows in upcoming_shows_Venues:
    Artisti2=db.session.query(Artist).filter(Artist.id==upcoming_shows.artists_id).first()
    upcoming_shows_SET.append({
      "artist_id": Artisti2.id,
      "artist_name": Artisti2.name, 
      "artist_image_link": Artisti2.image_link,
      "start_time": upcoming_shows.start_time.strftime("%Y-%m-%d %H:%M:%S") 
    })

  data = {
    "id": VenueI.id,
    "name": VenueI.name,
    "genres": VenueI.genres, 
    "address": VenueI.address,
    "city": VenueI.city,
    "state": VenueI.state,
    "phone": VenueI.phone,
    "website": VenueI.website,
    "facebook_link": VenueI.facebook_link,
    "seeking_talent": VenueI.seeking_talent,
    "seeking_description": VenueI.seeking_description,
    "image_link": VenueI.image_link,
    "past_shows": past_shows_SET,
    "upcoming_shows": upcoming_shows_SET,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm()
  error = False
  # build the venuei to insert as a new Venue 
  try:
    venuei = Venue()
    venuei.name= request.form.get('name')
    venuei.city= request.form.get('city')
    venuei.state= request.form.get('state')
    venuei.address= request.form.get('address')
    venuei.phone= request.form.get('phone')
    venuei.image_link= request.form.get('image_link')
    venuei.facebook_link= request.form.get('facebook_link')
    get_genres = request.form.getlist('genres')
    venuei.genres = ','.join(get_genres)
    db.session.add(venuei)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
            flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
    else:
            # on successful db insert, flash success
            flash('Venue ' + request.form.get('name') + ' was successfully listed!')
    return render_template('pages/home.html')
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    db.session.query.filter_by(Venue.id==venue_id).delete()
    db.session.commit()
  except:
    error = False
    db.session.rollback()
  finally:
    db.session.close()
    if error:
      flash('An error occurred. Venue ' + venue_id+ ' could not be deleted.')
    else:
      flash('Venue ' + venue_id + ' was successfully deleted!')
      # return jsonify({ 'success': True })
  return render_template('pages/home.html')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  #return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  data=[]
  artistSet= db.session.query(Artist.id,Artist.name).all()
  for artistI in artistSet:
   data.append ({
     "id": artistI.id,
     "name": artistI.name,
   })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
 # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  data=[] 
  search_words=request.form.get('search_term', '')
  data=search_artist_name(Artist, search_words)
  response={
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data=[]
  # retraive only the passing venue_id 
  ArtistI= db.session.query(Artist).filter(Artist.id==artist_id).first()
    # retraive info of the show obj of the passing venue_id and the venue's past shows 
  past_shows_Artist= db.session.query(Show).filter(Show.artists_id==artist_id, Show.start_time <= datetime.now()).all()
    # count the past shows
  past_shows_count= db.session.query(Show).filter(Show.artists_id==artist_id, Show.start_time <= datetime.now()).count()
    # retraive info of the show obj of the passing venue_id and the venue's upcoming shows 
  upcoming_shows_Artist= db.session.query(Show).filter(Show.artists_id==artist_id, Show.start_time >= datetime.now()).all()
    # count the upcoming shows
  upcoming_shows_count=db.session.query(Show).filter(Show.artists_id==artist_id, Show.start_time >= datetime.now()).count()
  #  build the artists where their shows played in the past 
  past_shows_SET=[]
  for past_shows in past_shows_Artist:
    Venuei=db.session.query(Venue).filter(Venue.id==past_shows.venue_id).first()
    past_shows_SET.append({
      "venue_id": Venuei.id,
      "venue_name": Venuei.name, 
      "venue_image_link": Venuei.image_link,
      "start_time": past_shows.start_time.strftime("%Y-%m-%d %H:%M:%S") 
    })
    #  build the artists where their shows WILL PLAY IN THE FUTURE
  upcoming_shows_SET=[]
  for upcoming_shows in upcoming_shows_Artist:
    Venuei2=db.session.query(Venue).filter(Venue.id==upcoming_shows.venue_id).first()
    upcoming_shows_SET.append({
      "venue_id": Venuei2.id,
      "venue_name": Venuei2.name, 
      "venue_image_link": Venuei2.image_link,
      "start_time": upcoming_shows.start_time.strftime("%Y-%m-%d %H:%M:%S") 
    })

  data = {
    "id": ArtistI.id,
    "name": ArtistI.name,
    "genres": ArtistI.genres,
    "city": ArtistI.city,
    "state": ArtistI.state,
    "phone": ArtistI.phone,
    "website": ArtistI.website,
    "facebook_link": ArtistI.facebook_link,
    "seeking_description": ArtistI.seeking_description,
    "image_link": ArtistI.image_link,
    "past_shows": past_shows_SET,
    "upcoming_shows": upcoming_shows_SET,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
  }  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  form = VenueForm()
  artist= db.session.query(Artist).filter(Artist.id==artist_id).first()
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  try:
    artisti = db.session.query(Artist).filter(Artist.id==artist_id).first()
    artisti.name= request.form.get('name')
    artisti.city= request.form.get('city')
    artisti.state= request.form.get('state')
    artisti.phone= request.form.get('phone')
    artisti.image_link= request.form.get('image_link')
    artisti.facebook_link= request.form.get('facebook_link')
    artisti.website= request.form.get('website')
    artisti.seeking_description= request.form.get('seeking_description')
    get_genres = request.form.getlist('genres')
    artisti.genres = ','.join(get_genres)
    db.session.add(artisti)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
            flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
    else:
            # on successful db insert, flash success
            flash('Venue ' + request.form.get('name') + ' was successfully listed!')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue= db.session.query(Venue).filter(Venue.id==venue_id).first()

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  error = False
  try:
    venuei = db.session.query(Venue).filter(Venue.id==venue_id).first()
    venuei.name= request.form.get('name')
    venuei.city= request.form.get('city')
    venuei.state= request.form.get('state')
    venuei.address= request.form.get('address')
    venuei.phone= request.form.get('phone')
    venuei.image_link= request.form.get('image_link')
    venuei.facebook_link= request.form.get('facebook_link')
    venuei.website= request.form.get('website')
    venuei.seeking_talent= False
    venuei.seeking_description= request.form.get('seeking_description')
    venuei.genres= request.form.get('genres')
    db.session.add(venuei)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
            flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
    else:
            # on successful db insert, flash success
            flash('Venue ' + request.form.get('name') + ' was successfully listed!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # build the venuei to insert as a new Venue 
  form = VenueForm()
  error = False
  try: 
    artisti = Artist()
    artisti.name= request.form.get('name')
    artisti.city= request.form.get('city')
    artisti.state= request.form.get('state')
    artisti.phone= request.form.get('phone')
    artisti.facebook_link= request.form.get('facebook_link')
    artisti.genres= request.form.get('genres')
    db.session.add(artisti)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
    else:
      # on successful db insert, flash success
      flash('Artist ' + request.form.get('name') + ' was successfully listed!')
    return render_template('pages/home.html')
  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  #return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue
  data=[]
  query_join = db.session.query(Show,Venue ,Artist).join(Venue, Venue.id == Show.venue_id).join(Artist, Artist.id == Show.artists_id).all()
  #sys.stdout.write(str(query_join))
  for v in query_join:
    data.append({
      "venue_id": v.Venue.id,
      "venue_name": v.Venue.name,
      "artist_id": v.Artist.id,
      "artist_name": v.Artist.name,
      "artist_image_link": v.Artist.image_link,
      "start_time": v.Show.start_time.strftime("%Y-%m-%d %H:%M:%S") 
    })
  #sys.stdout.write(str(data))
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = VenueForm()
  error = False
  showi = Show()
  try: 
    showi.start_time= request.form.get('start_time')
    showi.venue_id= request.form.get('venue_id')
    showi.artists_id= request.form.get('artist_id')
    db.session.add(showi)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
            flash('Show was successfully listed!')
    else:
            # on successful db insert, flash success
            flash('An error occurred. Show could not be listed.')
    return render_template('pages/home.html')

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
