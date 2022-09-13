from ast import Num
from lib2to3.pgen2.token import OP
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SelectField, IntegerField
from wtforms.validators import InputRequired, Optional, DataRequired, URL, NumberRange

class PetForm(FlaskForm):
    """Add Pet Form Model"""

    name = StringField("Pet Name", validators=[InputRequired(message="Please input pet's name")])
    species = SelectField("Species", choices=[("", "-------------Please Select Pet's Species-------------"), ('cat', 'Cat'), ('dog', 'Dog'), ('porpupine', 'Porcupine')], validators=[InputRequired(message="Pet species is required"), DataRequired()]) 
    photo_url = StringField("Photo URL", validators=[Optional(), URL(message="Please enter a valid URL")])
    age = IntegerField("Pet's Age", validators=[Optional(), NumberRange(min=0,max=30,message="Age must be between 0-30 years old")])
    notes = StringField("Notes")
    available = BooleanField("Available for adoption?")
