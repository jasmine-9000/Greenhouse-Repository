#############################################################################################################################
#					IMPORTS																									#
#############################################################################################################################

from flask_wtf import FlaskForm

from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, NumberRange
from wtforms_components import DateTimeField, DateRange
from wtforms_sqlalchemy.fields import QuerySelectField

from werkzeug.datastructures import MultiDict

from wtforms.fields import SubmitField, DateField, StringField, SelectField, IntegerField, PasswordField, BooleanField
from datetime import datetime
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime
from flask_greenhouse.sensors.models import User, Sensor, SensorDataEntry

# login manager. It must be here to interact with things. 
from flask_login import login_required, login_user, current_user, logout_user
from flask_greenhouse import login_manager


#############################################################################################################################
#						LOGIN MANAGER DECORATORS																			#
#############################################################################################################################
@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))
	
#############################################################################################################################
#											FORMS																			#
#############################################################################################################################


#############################################################################################################################
#									USER REGISTRATION FORM																	#
#############################################################################################################################
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
			
#############################################################################################################################
#									USER LOGIN FORM																			#
#############################################################################################################################
class UserLoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')
	
#############################################################################################################################
#									SENSOR DATA REQUEST FORM																#
#############################################################################################################################
	
class SensorRequestForm(FlaskForm):
	sensors_owned = SelectField('Sensors owned', coerce=int, validators=[DataRequired()])
	start_date = DateTimeLocalField('Start Date', default=datetime.now())
	end_date = DateTimeLocalField('End Date', default=datetime.now())
	interval = IntegerField('Time Interval', default=10, validators=[DataRequired(), NumberRange(10,1000)])
	title = StringField('Title');
	x_axis = StringField('X axis')
	y_axis = StringField('Y axis')
	
	def validate_interval(form, interval):	# custom validators must be named "validate_<name of variable>".
		if (interval.data % 10): 
			raise ValidationError("Values must be a multiple of 10.")
			
	submit = SubmitField('Request Data') 

#############################################################################################################################
#									SENSOR REGISTRATION FORM																#
#############################################################################################################################	

class SensorRegistrationForm(FlaskForm):
	sensor_name = StringField('Enter The Name of the Sensor')
	units = StringField('Enter what units this sensor is measuring')
	protocol = StringField('Enter what protocol this sensor is using (optional at the moment)')
	type = StringField('Enter what your sensor is measuring')
	submit = SubmitField('Register your sensor')
	
	
#############################################################################################################################
#									SOURCES																					#
#############################################################################################################################

# https://stackoverflow.com/questions/46921823/dynamic-choices-wtforms-flask-selectfield
















#############################################################################################################################
#									TESTING AREA
#############################################################################################################################
class CityForm(FlaskForm):
	state = SelectField('state', choices=[('CA', 'California'), ('NV', 'Nevada')])
	city = SelectField('city', choices=[])