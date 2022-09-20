from unittest.loader import VALID_MODULE_NAME
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    """Register User Form"""

    username = StringField("Username", validators=[InputRequired(), Length(max=20, message="Should not exceed 20 characters")])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Length(max=50, message="Should not exceed 50 characters")])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30, message="Should not exceed 30 characters")])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30, message="Should not exceed 30 characters")])


class LoginForm(FlaskForm):
    """Login User Form"""
    
    username = StringField("Username", validators=[InputRequired(), Length(max=20, message="Should not exceed 20 characters")])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Feedback Form"""

    title = StringField("Title", validators=[InputRequired(), Length(max=100, message="Should not exceed 100 characters")])
    content = StringField("Content", validators=[InputRequired()])