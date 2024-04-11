from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email
import email_validator
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    # def validate(self, username):
    #     #to do
    #     return True
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    checkPassword = PasswordField('Check Password', validators=[DataRequired(), EqualTo
                                                                ('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')


    def __repr__(self):
        return f"RegisterForm('{self.username}', '{self.email}')"