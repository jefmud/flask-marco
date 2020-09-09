# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SelectField
from wtforms.validators import InputRequired
import config

class SpeciesQueryForm(FlaskForm):
    detection_threshold = FloatField('Detection Confidence Threshold',  validators=[InputRequired()])
    #species_prediction = StringField('Species Prediction', validators=[InputRequired()])
    species_select = SelectField('Species Select', choices=config.species_choices())
    species_confidence = FloatField('Confidence Threshold',  validators=[InputRequired()])


class SiteQueryForm(FlaskForm):
    start_date = StringField()
    end_date = StringField()
    site = StringField()

class GeneralQueryForm(FlaskForm):
    season_select = SelectField('Season Select', choices=config.select_choices(config.seasons))
    detection_threshold = FloatField('Detection Confidence Threshold', default=0.9, validators=[InputRequired()])
    species_select = SelectField('Species Select', choices=config.species_choices())
    species_confidence = FloatField('Species Confidence Threshold',  default=0.9, validators=[InputRequired()])

class RegisterForm(FlaskForm):
    first = StringField('First Name')
    last = StringField('Last Name')