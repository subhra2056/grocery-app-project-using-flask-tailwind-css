from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, FloatField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, NumberRange

class sign_up_form(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    fullname = StringField('Enter your fullname', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired(), length(min=6)])
    confirm_password = PasswordField('Confirm Your Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')


class login_form(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class passwordchangeform(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Save Changes')