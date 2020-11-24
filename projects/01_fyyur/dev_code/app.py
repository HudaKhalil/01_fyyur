#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
# import json
# import dateutil.parser
from datetime import datetime
from threading import Event
import babel
from flask import (render_template, 
                   request, 
                   flash, 
                   redirect, 
                   url_for,
                   jsonify)
from flask_wtf.csrf import validate_csrf
# from flask_wtf import Form
from sqlalchemy import (func, 
                        inspect)
import logging
from logging import (Formatter, 
                     FileHandler, 
                     error)
# from flask_inputs import Inputs
# from wtforms.validators import DataRequired
# from sqlalchemy.sql.schema import PrimaryKeyConstraint
from wtforms import Form
from forms import *
from models import (Venue, 
                    Show, 
                    Artist, 
                    app, 
                    db)
 #----------------------------------------------------------------------------#
 # New Functions
 #----------------------------------------------------------------------------#
 # Convert Single Object as Dictionary
 # Advantage of usage:"http://www.compciv.org/guides/python/fundamentals/dictionaries-overview/"
 # Func. Source:"https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict"
def object_as_dict(obj):
  return {c.key: getattr(obj, c.key)
          for c in inspect(obj).mapper.column_attrs}
  
# Deal with Collection Results
# Func. Source:"https://stackoverflow.com/questions/48232222/how-to-deal-with-sqlalchemy-util-collections-result"
def get_dict_list_from_result(result):
  list_dict = []
  for i in result:
      i_dict = i._asdict()
      list_dict.append(i_dict)
  return list_dict

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  # date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(value, format)

app.jinja_env.filters['datetime'] = format_datetime

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
  # TODO: replace with real venues data.<Done>
  # num_shows should be aggregated based on number of upcoming shows per venue.
  # Get City & State in Venues  
  groupby_venues_result = (db.session.query(
    Venue.city,
    Venue.state
)
    .group_by(
    Venue.city,
    Venue.state
)
)
  # Create dictionary list for the query
  data = get_dict_list_from_result(groupby_venues_result)

  # Loop through Query List and append Venue data
  for area in data:  
      # ist of venues that are in the same city, and add it to new dictionary-key 'venues'
      area['venues'] = [object_as_dict(
          ven) for ven in Venue.query.filter_by(city=area['city']).all()]
      # Append num_shows
      for ven in area['venues']:
        # counts how many upcoming shows the venue has.
        ven['num_shows'] = db.session.query(func.count(Show.c.venue_id)).filter(
            Show.c.venue_id == ven['id']).filter(Show.c.start_time > datetime.now()).all()[0][0]
  return render_template('pages/venues.html', areas=data)

# Search Venue
#----------------------------------------------------------------------------#


@app.route('/venues/search', methods=['POST','GET'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.<Done>
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # Using ilike for case-insensitive
  # "https://stackoverflow.com/questions/40412034/flask-sqlalchemy-contains-ilike-producing-different-results#:~:text=Therefore%2C%20to%20match%20a%20sequence,sensitive%2C%20while%20ilike%20is%20insensitive."
    search = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike('%{}%'.format(search))).all()
    count_venues=len(venues)

    response = {
    'count': count_venues,
    'data': venues
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id <Done>
   # Get Venue Data
  venue_query = Venue.query.get(venue_id)
  # Get Past Shows Data
  venue_query.past_shows = (db.session.query(
      Artist.id.label("artist_id"),
      Artist.name.label("artist_name"),
      Artist.image_link.label("artist_image_link"),Show)
      .filter(Show.c.venue_id == venue_id)
      .filter(Show.c.artist_id == Artist.id)
      .filter(Show.c.start_time <= datetime.now())
      .all())

  # Get Upcomming Shows
  venue_query.upcoming_shows = (db.session.query(
      Artist.id.label("artist_id"),
      Artist.name.label("artist_name"),
      Artist.image_link.label("artist_image_link"),Show)
      .filter(Show.c.venue_id == venue_id)
      .filter(Show.c.artist_id == Artist.id)
      .filter(Show.c.start_time > datetime.now())
      .all())

  # Get Number of Upcoming Shows
  venue_query.upcoming_shows_count = (db.session.query(
      func.count(Show.c.venue_id))
      .filter(Show.c.venue_id == venue_id)
      .filter(Show.c.start_time > datetime.now())
      .all())[0][0]
  
  # Get Number of past Shows
  venue_query.past_shows_count = (db.session.query(
      func.count(Show.c.venue_id))
      .filter(Show.c.venue_id == venue_id)
      .filter(Show.c.start_time < datetime.now())
      .all())[0][0]


  return render_template('pages/show_venue.html', venue=venue_query)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead<Done>
  # TODO: modify data to be the data object returned from db insertion<Done>
  form = VenueForm(request.form)
  if form.validate():
    try:
      # Data from VenueForm
      newVenue = Venue(
        name=request.form['name'],
        city=request.form['city'],
        state=request.form['state'],
        address=request.form['address'],
        phone=request.form['phone'],
        genres=request.form.getlist('genres'),
        website=request.form['website'],
        facebook_link=request.form['facebook_link'],
        image_link=request.form['image_link'],
        seeking_talent= False
        )
      db.session.add(newVenue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue {} was successfully listed!'.format(newVenue.name))
    except:
      # TODO DONE: on unsuccessful db insert, flash an error instead.<Done>
      flash('An error occurred due to database insertion error. Venue {} could not be listed.'.format(
          request.form['name']))
    finally:
      db.session.close()
  else:
    flash(form.errors)
    flash('An error occurred due to form validation. Venue {} could not be listed.'.format(request.form['name']))
  
  return render_template('pages/home.html')

# Delete Venue
#-----------------------------------------------------------------------------------------#
@app.route('/venues/<venue_id>/delete', methods=['GET','DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using<Done>
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage  
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # venue_id = request.form.get('venue_id')

  deleted_venue = Venue.query.get(venue_id)
  deleted_venue_name = deleted_venue.name
  try:
    db.session.delete(deleted_venue)
    db.session.commit()
    flash('Venue ' + deleted_venue_name + ' was successfully deleted!')
  except:
    db.session.rollback()
    flash('Please try again. Venue ' + deleted_venue_name + ' could not be deleted, there are still shows attached.')
    return render_template('pages/show_venue.html')
  finally:
    db.session.close()  
  return render_template('pages/home.html')


# Update Venue
#--------------------------------------------------------------------------------------------------#

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.filter_by(id=venue_id).one()
  form = VenueForm(obj=venue)
  form.populate_obj(venue)
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  form.website.data = venue.website
  form.image_link.data = venue.image_link
  return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    venue = Venue.query.get(venue_id)
    updated_venue_name = venue.name
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form['facebook_link']
    venue.image_link = request.form['image_link']
    venue.website = request.form['website']
    db.session.add(venue)
    db.session.commit()
    flash('Venue: ' + updated_venue_name + ' was successfully Updated!')
  except:
    db.session.rollback()
    flash('Please try again. Someting went wrong')
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  
  # TODO: replace with real data returned from querying the database <Done>
  
  artist_data = Artist.query.with_entities(Artist.id, Artist.name).all()
  
  return render_template('pages/artists.html', artists=artist_data)


@app.route('/artists/search', methods=['POST', 'GET'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. <Done>
  search = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike('%{}%'.format(search))).all()
  count_artists = len(artists)
  response = {
      'count': count_artists,
      'data': artists
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

# Show Artist  
#---------------------------------------------------------------------------------------------------# 
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist_query = Artist.query.get(artist_id)
  # Past Shows
  artist_query.past_shows = (db.session.query(
      Venue.id.label("venue_id"),
      Venue.name.label("venue_name"),
      Venue.image_link.label("venue_image_link"),
      Show)
      .filter(Show.c.artist_id == artist_id)
      .filter(Show.c.venue_id == Venue.id)
      .filter(Show.c.start_time <= datetime.now())
      .all())

  # Upcomming Shows
  artist_query.upcoming_shows = (db.session.query(
      Venue.id.label("venue_id"),
      Venue.name.label("venue_name"),
      Venue.image_link.label("venue_image_link"),
      Show)
      .filter(Show.c.artist_id == artist_id)
      .filter(Show.c.venue_id == Venue.id)
      .filter(Show.c.start_time > datetime.now())
      .all())

  # Number of past Shows
  artist_query.past_shows_count = (db.session.query(
      func.count(Show.c.artist_id))
      .filter(Show.c.artist_id == artist_id)
      .filter(Show.c.start_time < datetime.now())
      .all())[0][0]

  # Number of Upcoming Shows
  artist_query.past_shows_count = (db.session.query(
      func.count(Show.c.artist_id))
      .filter(Show.c.artist_id == artist_id)
      .filter(Show.c.start_time < datetime.now())
      .all())[0][0]

  return render_template('pages/show_artist.html', artist=artist_query)

#  Update Artist
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_id = request.args.get('artist_id')
  artist = Artist.query.get(artist_id)
  artist_info = {
      "id": artist.id,
      "name": artist.name,
      "genres": artist.genres.split(','),
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.website,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.seeking_venue,
      "seeking_description": artist.seeking_description,
      "image_link": artist.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  artist.name = request.form['name'],
  artist.city = request.form['city'],
  artist.state = request.form['state'],
  artist.phone = request.form['phone'],
  artist.genres = request.form.getlist('genres'),
  artist.facebook_link = request.form['facebook_link']
  artist.website = request.form['website']
  db.session.add(artist)
  db.session.commit()
  db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead<Done>
  # TODO: modify data to be the data object returned from db insertion<Done>
  form = ArtistForm()
  if form.validate():
    try:
      # New Artist
      newArtist = Artist(
          name=request.form['name'],
          city=request.form['city'],
          state=request.form['state'],
          phone=request.form['phone'],
          facebook_link=request.form['facebook_link'],
          genres=request.form.getlist('genres'),
          website=request.form['website'],
          seeking_venue= False
      )
      db.session.add(newArtist)
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist {} was successfully listed!'.format(newArtist.name))
      # TODO: on unsuccessful db insert, flash an error instead.<Done>
    except:
      flash('An error occurred due to database insertion error. Artist {} could not be listed.'.format(
          request.form['name']))
    finally:
      db.session.close()
  else:
    flash(form.errors)
    flash('An error occurred due to form validation. Artist {} could not be listed.'.format(request.form['name']))
    
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = (db.session.query(
      Venue.id.label("venue_id"),
      Venue.name.label("venue_name"),
      Artist.id.label("artist_id"),
      Artist.name.label("artist_name"),
      Artist.image_link.label("artist_image_link"),
      Show)
      .filter(Show.c.venue_id == Venue.id)
      .filter(Show.c.artist_id == Artist.id)
      .all())
  return render_template('pages/shows.html', shows=data)


@app.route('/shows/create',  methods=['GET'])
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  if form.validate():
    try:     
      newShow = Show.insert().values(
          venue_id=request.form['venue_id'],
          artist_id=request.form['artist_id'],
          start_time=request.form['start_time']
      )
      db.session.execute(newShow)
      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    except:
      flash('An error occurred. Show could not be listed.')
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:     
      db.session.close()
  else:
    flash(form.errors)
    flash('An error occurred due to form validation. Show could not be listed.')
  return render_template('pages/home.html')


@app.errorhandler(401)
def not_found_error(error):
    return render_template('errors/401.html'), 401


@app.errorhandler(403)
def not_found_error(error):
    return render_template('errors/403.html'), 403
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404
 

@app.errorhandler(405)
def not_found_error(error):
    return render_template('errors/405.html'), 405


@app.errorhandler(409)
def not_found_error(error):
    return render_template('errors/409.html'), 409


@app.errorhandler(422)
def not_found_error(error):
    return render_template('errors/422.html'), 422
  

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
