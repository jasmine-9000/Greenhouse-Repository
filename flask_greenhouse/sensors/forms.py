from flask_wtf import FlaskForm

from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from wtforms_components import DateTimeField, DateRange
from wtforms_sqlalchemy.fields import QuerySelectField

from werkzeug.datastructures import MultiDict

from wtforms.fields import SubmitField, DateField, StringField, SelectField, IntegerField, PasswordField, BooleanField
from datetime import datetime
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime
from flask_greenhouse.sensors.models import User, Sensor, SensorDataEntry
#from flask_greenhouse.sensors.routes import current_user

# login manager. It must be here to interact with things. 
from flask_login import login_required, login_user, current_user, logout_user
from flask_greenhouse import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))
	


class CityForm(FlaskForm):
	state = SelectField('state', choices=[('CA', 'California'), ('NV', 'Nevada')])
	city = SelectField('city', choices=[])

class UserRegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one.')
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one.')

class UserLoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')
	
	
class SensorRequestForm(FlaskForm):
	sensors_owned = SelectField('Sensors owned', coerce=int, validators=[DataRequired()])
	#https://stackoverflow.com/questions/46921823/dynamic-choices-wtforms-flask-selectfield
	start_date = DateTimeLocalField('Start Date', default=datetime.now())
	end_date = DateTimeLocalField('End Date', default=datetime.now())
	interval = IntegerField('Time Interval')
	def validate_interval(form, interval):	# custom validators must be named "validate_<name of variable>".
		if (interval.data % 10): 
			raise ValidationError("Values must be a multiple of 10.")
	submit = SubmitField('Request Data') 

		
class SensorRegistrationForm(FlaskForm):
	sensor_name = StringField('Enter The Name of the Sensor')
	units = StringField('Enter what units this sensor is measuring')
	protocol = StringField('Enter what protocol this sensor is using (optional at the moment)')
	submit = SubmitField('Register your sensor')

