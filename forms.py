from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, URL, Length, Optional
from constants import STATES, GENRES


class ShowForm(FlaskForm):
    artist_id = StringField('artist_id')
    venue_id = StringField('venue_id')
    start_time = DateTimeField('start_time',
                               validators=[DataRequired()],
                               default=datetime.today())


class VenueForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()], choices=STATES)
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone')
    image_link = StringField('image_link')
    genres = SelectMultipleField('genres',
                                 validators=[DataRequired(),
                                             Length(max=4)],
                                 choices=GENRES)
    facebook_link = StringField('facebook_link', validators=[URL()])
    website = StringField('website', validators=[URL()])
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = TextAreaField('seeking_description',
                                        validators=[Optional()])


class ArtistForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()], choices=STATES)
    phone = StringField('phone')
    image_link = StringField('image_link', validators=[URL()])
    genres = SelectMultipleField('genres',
                                 validators=[DataRequired()],
                                 choices=GENRES)
    facebook_link = StringField('facebook_link', validators=[URL()])
    website = StringField('website')
    seeking_venue = BooleanField('seeking_venue')
    seeking_description = StringField('seeking_description')
