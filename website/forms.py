from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, FloatField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, NumberRange

class sign_up_form(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    fullname = StringField('Enter your fullname', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Your Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class login_form(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired()])
    submit = SubmitField('Login')