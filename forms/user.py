from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat password', validators=[DataRequired()])
    name = StringField('Display name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    about = TextAreaField("About me")
    submit = SubmitField('Register')