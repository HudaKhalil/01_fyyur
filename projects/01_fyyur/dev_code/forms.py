from collections import namedtuple
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, FieldList
from wtforms.validators import DataRequired, AnyOf, URL
from enum import Enum, auto
from types import *


# def get_dic_list(enum_type):
#   create_dic = []
#   for i in enum_type:
#       i_dic = i.value
#       create_dic.append(i_dic)
#   return create_dic


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )



# class Genres (Enum):
#     1= 'Alternative'
#     2= 'Blues'
#     3= 'Classical'
   
   
#                         #  ('Country', 'Country'),
#                         #  ('Electronic', 'Electronic'),
#                         #  ('Folk', 'Folk'),
#                         #  ('Funk', 'Funk'),
#                         #  ('Hip-Hop', 'Hip-Hop'),
#                         #  ('Heavy Metal', 'Heavy Metal'),
#                         #  ('Instrumental', 'Instrumental'),
#                         #  ('Jazz', 'Jazz'),
#                         #  ('Musical Theatre', 'Musical Theatre'),
#                         #  ('Pop', 'Pop'),
#                         #  ('Punk', 'Punk'),
#                         #  ('R&B', 'R&B'),
#                         #  ('Reggae', 'Reggae'),
#                         #  ('Rock n Roll', 'Rock n Roll'),
#                         #  ('Soul', 'Soul'),
#                         #  ('Other', 'Other')])

# States = Enum('States',
#                [('AL', 'AL'),
#                 ('AK', 'AK'),
#                 ('AZ', 'AZ'),
#                 ('AR', 'AR'),
#                 ('CA', 'CA'),
#                 ('CO', 'CO'),
#                 ('CT', 'CT'),
#                 ('DE', 'DE'),
#                 ('DC', 'DC'),
#                 ('FL', 'FL'),
#                 ('GA', 'GA'),
#                 ('HI', 'HI'),
#                 ('ID', 'ID'),
#                 ('IL', 'IL'),
#                 ('IN', 'IN'),
#                 ('IA', 'IA'),
#                 ('KS', 'KS'),
#                 ('KY', 'KY'),
#                 ('LA', 'LA'),
#                 ('ME', 'ME'),
#                 ('MT', 'MT'),
#                 ('NE', 'NE'),
#                 ('NV', 'NV'),
#                 ('NH', 'NH'),
#                 ('NJ', 'NJ'),
#                 ('NM', 'NM'),
#                 ('NY', 'NY'),
#                 ('NC', 'NC'),
#                 ('ND', 'ND'),
#                 ('OH', 'OH'),
#                 ('OK', 'OK'),
#                 ('OR', 'OR'),
#                 ('MD', 'MD'),
#                 ('MA', 'MA'),
#                 ('MI', 'MI'),
#                 ('MN', 'MN'),
#                 ('MS', 'MS'),
#                 ('MO', 'MO'),
#                 ('PA', 'PA'),
#                 ('RI', 'RI'),
#                 ('SC', 'SC'),
#                 ('SD', 'SD'),
#                 ('TN', 'TN'),
#                 ('TX', 'TX'),
#                 ('UT', 'UT'),
#                 ('VT', 'VT'),
#                 ('VA', 'VA'),
#                 ('WA', 'WA'),
#                 ('WV', 'WV'),
#                 ('WI', 'WI'),
#                 ('WY', 'WY')
#               ])


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        # choices= get_dic_list(States)
        choices=[('AL', 'AL'),
                ('AK', 'AK'),
                ('AZ', 'AZ'),
                ('AR', 'AR'),
                ('CA', 'CA'),
                ('CO', 'CO'),
                ('CT', 'CT'),
                ('DE', 'DE'),
                ('DC', 'DC'),
                ('FL', 'FL'),
                ('GA', 'GA'),
                ('HI', 'HI'),
                ('ID', 'ID'),
                ('IL', 'IL'),
                ('IN', 'IN'),
                ('IA', 'IA'),
                ('KS', 'KS'),
                ('KY', 'KY'),
                ('LA', 'LA'),
                ('ME', 'ME'),
                ('MT', 'MT'),
                ('NE', 'NE'),
                ('NV', 'NV'),
                ('NH', 'NH'),
                ('NJ', 'NJ'),
                ('NM', 'NM'),
                ('NY', 'NY'),
                ('NC', 'NC'),
                ('ND', 'ND'),
                ('OH', 'OH'),
                ('OK', 'OK'),
                ('OR', 'OR'),
                ('MD', 'MD'),
                ('MA', 'MA'),
                ('MI', 'MI'),
                ('MN', 'MN'),
                ('MS', 'MS'),
                ('MO', 'MO'),
                ('PA', 'PA'),
                ('RI', 'RI'),
                ('SC', 'SC'),
                ('SD', 'SD'),
                ('TN', 'TN'),
                ('TX', 'TX'),
                ('UT', 'UT'),
                ('VT', 'VT'),
                ('VA', 'VA'),
                ('WA', 'WA'),
                ('WV', 'WV'),
                ('WI', 'WI'),
                ('WY', 'WY')
            ])
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction 
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    # Added for Venue Image link
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    # Added for Venue Website
    website = StringField(
        'website', validators=[URL()]
    )


class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        # choices= enumerate(States)
        choices=[('AL', 'AL'),
                 ('AK', 'AK'),
                 ('AZ', 'AZ'),
                 ('AR', 'AR'),
                 ('CA', 'CA'),
                 ('CO', 'CO'),
                 ('CT', 'CT'),
                 ('DE', 'DE'),
                 ('DC', 'DC'),
                 ('FL', 'FL'),
                 ('GA', 'GA'),
                 ('HI', 'HI'),
                 ('ID', 'ID'),
                 ('IL', 'IL'),
                 ('IN', 'IN'),
                 ('IA', 'IA'),
                 ('KS', 'KS'),
                 ('KY', 'KY'),
                 ('LA', 'LA'),
                 ('ME', 'ME'),
                 ('MT', 'MT'),
                 ('NE', 'NE'),
                 ('NV', 'NV'),
                 ('NH', 'NH'),
                 ('NJ', 'NJ'),
                 ('NM', 'NM'),
                 ('NY', 'NY'),
                 ('NC', 'NC'),
                 ('ND', 'ND'),
                 ('OH', 'OH'),
                 ('OK', 'OK'),
                 ('OR', 'OR'),
                 ('MD', 'MD'),
                 ('MA', 'MA'),
                 ('MI', 'MI'),
                 ('MN', 'MN'),
                 ('MS', 'MS'),
                 ('MO', 'MO'),
                 ('PA', 'PA'),
                 ('RI', 'RI'),
                 ('SC', 'SC'),
                 ('SD', 'SD'),
                 ('TN', 'TN'),
                 ('TX', 'TX'),
                 ('UT', 'UT'),
                 ('VT', 'VT'),
                 ('VA', 'VA'),
                 ('WA', 'WA'),
                 ('WV', 'WV'),
                 ('WI', 'WI'),
                 ('WY', 'WY')
                 ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        # choices=enumerate(Genres)
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )
    # Added for Artist Website
    website = StringField(
        'website', validators=[URL()]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
