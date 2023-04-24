from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, FileField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class RegisterForm(FlaskForm):
    login = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat password', validators=[DataRequired()])
    name = StringField('Display name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    about = TextAreaField("About me")
    avatar = FileField('Load your profile picture',
                       validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'You can only use jpg ot png files as avatars')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    login = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

class EditForm(FlaskForm):
    name = StringField('Display name', validators=[DataRequired()])
    about = TextAreaField("About me")
    avatar = FileField('Profile picture',
                       validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'You can only use jpg ot png files as avatars')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')
