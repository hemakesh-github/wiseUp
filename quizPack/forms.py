from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
import email_validator
from .models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

   
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user == None:
            raise ValidationError('No user exits with this username')

    def __repr__(self):
        return f"username: {self.username}"
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    checkPassword = PasswordField('Check Password', validators=[DataRequired(), EqualTo
                                                                ('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user != None:
            raise ValidationError('The email is already registered')
        
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user != None:
            raise ValidationError('The username is already taken')

    def __repr__(self):
        return f"RegisterForm('{self.username}', '{self.email}')"
    
    