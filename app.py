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
from flask_wtf import FlaskForm
from forms import *

from flask_migrate import Migrate
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
migrate = Migrate(app, db)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(250))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(250))

    shows = db.relationship('Show', backref='venue', lazy=True)
    def __repr__(self):
        return f'<Venue: {self.id}, {self.name}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(250))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(250))

    shows = db.relationship('Show', backref='artist', lazy=True)
    def __repr__(self):
        return f'<Artist: {self.id}, {self.name}>'

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
      return f'<Show {self.id}, Artist {self.artist_id}, Venue {self.venue_id}>'


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

@app.template_filter('format_datetime')
def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


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
    
    venues = Venue.query.all()

    # If there are duplicates
    locations = set()

    # Add the city/state to the new location variable
    for venue in venues:
        locations.add((venue.city, venue.state))

    # Append all venues in each city/state
    data = []
    for location in locations:
        data.append({
            "city": location[0],
            "state": location[1],
            "venues": []
        })

    for venue in venues:

        shows = Show.query.filter_by(venue_id=venue.id).all()
        current_date = datetime.now()
        num_upcoming_shows = 0

        # Compare if show time is earlier than current time
        for show in shows:
            if show.start_time > current_date:
                num_upcoming_shows += 1

        # Append all locations into data to show on the page
        for venue_location in data:
            if venue.state == venue_location['state'] and venue.city == venue_location['city']:
                venue_location['venues'].append({
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": num_upcoming_shows
                })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))

    response={
        "count": result.count(),
        "data": result
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    shows = Show.query.filter_by(venue_id=venue_id).all()
    venue.genres = venue.genres.split(',')

    past_shows = []
    upcoming_shows = []
    current_time = datetime.now()

    for show in shows:
        data = {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": format_datetime(str(show.start_time))
            }
        if show.start_time > current_time:
            upcoming_shows.append(data)
        else:
            past_shows.append(data)

    data = {
        "id": venue.id,
        "name": venue.name,
        "city": venue.city,
        "state": venue.state,
        "address": venue.address,
        "phone": venue.phone,
        "genres": venue.genres,
        "image_link": venue.image_link,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description":venue.seeking_description,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template(
        'pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)
    try:
        seeking_talent = False
        seeking_description = ''
        if 'seeking_talent' in request.form:
            seeking_talent = request.form['seeking_talent'] == 'y'
        if 'seeking_description' in request.form:
            seeking_description = request.form['seeking_description']

        venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            genres=form.genres.data, 
            image_link=form.image_link.data,
            website=form.website.data,
            facebook_link=form.facebook_link.data,
            seeking_talent=form.seeking_talent.data,
            seeking_description=form.seeking_description.data)

        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue was successfully created!')
    except:
        flash('an error occured and Venue ' + venue_name + ' was not created.')
        db.session.rollback()
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        venue_name = venue.name

        db.session.delete(venue)
        db.session.commit()

        flash('Venue ' + venue_name + ' was deleted')
    except:
        flash('an error occured and Venue ' + venue_name + ' was not deleted')
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    return render_template('pages/artists.html', artists=Artist.query.all())


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))

    response={
        "count": result.count(),
        "data": result
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)
   


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):        
    artist = Artist.query.get(artist_id)
    shows = Show.query.filter_by(artist_id=artist_id).all()
    artist.genres = artist.genres.split(',')

    past_shows = []
    upcoming_shows = []
    current_time = datetime.now()

    for show in shows:
        data = {
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": format_datetime(str(show.start_time))
            }
        if show.start_time > current_time:
            upcoming_shows.append(data)
        else:
            past_shows.append(data)

    data = {
        "id": artist.id,
        "name": artist.name,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "genres": artist.genres,
        "image_link": artist.image_link,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    
    data = Artist.query.filter(Artist.id == artist_id).one()
    artist={
        "id": data.id,
        "name": data.name,
        "city": data.city,
        "state": data.state,
        "phone": data.phone,
        "genres":  data.genres,
        "image_link": data.image_link,
        "website": data.website,
        "facebook_link": data.facebook_link,
        "seeking_venue": data.seeking_venue,
        "seeking_description": data.seeking_description,
    }
    
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try: 
        form = ArtistForm()
        artist = Artist.query.get(artist_id)
        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.genres = form.genres.data
        artist.facebook_link = form.facebook_link.data
        artist.website = form.website.data
        artist.image_link = form.image_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data

        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully edited')
    except:
        flash('An error occured and artist ' + request.form['name'] + ' was not edit.')
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    data = Venue.query.filter(Venue.id == venue_id).one()
    venue={
        "id": data.id,
        "name": data.name,
        "city": data.city,
        "state": data.state,
        "address": data.address,
        "phone": data.phone,
        "genres": data.genres,
        "image_link": data.image_link,
        "website": data.website,
        "facebook_link": data.facebook_link,
        "seeking_talent": data.seeking_talent,
        "seeking_description": data.seeking_description
    }
    
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        form = VenueForm()
        venue = Venue.query.get(venue_id)
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.genres = form.genres.data
        venue.facebook_link = form.facebook_link.data
        venue.website = form.website.data
        venue.image_link = form.image_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data

        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully edited.')
    except:
        db.session.rollback()
        flash('An error occured and venue ' + request.form['name'] + ' was not edit.')
        print(sys.exc_info())
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)
    
    try:
        seeking_venue = False
        seeking_description = ''
        if 'seeking_venue' in request.form:
            seeking_venue = request.form['seeking_venue'] == 'y'
        if 'seeking_description' in request.form:
            seeking_description = request.form['seeking_description']

        artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            genres= form.genres.data,
            image_link=form.image_link.data,
            website=form.website.data,
            facebook_link=form.facebook_link.data,
            seeking_venue=form.seeking_venue.data,
            seeking_description=form.seeking_description.data,
        )
        db.session.add(artist)
        db.session.commit()
        
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
        print(sys.exc_info())
    finally:
        db.session.close()

    return render_template('pages/home.html')

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        artist = Artist.query.filter_by(id=artist_id).one()
        artist_name = artist.name

        db.session.delete(artist)
        db.session.commit()

        flash('Artist ' + artist_name + ' was deleted')
    except:
        flash('An error occured and Artist ' + artist_name + ' was not deleted.')
        db.session.rollback()

    return redirect(url_for('index'))

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    shows = Show.query.all()
    data = []
    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        })
    

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    
    venue_id = request.form.get('venue_id', '')
    artist_id = request.form.get('artist_id', '')
    start_time = request.form.get('start_time', '')
    show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
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
