from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
