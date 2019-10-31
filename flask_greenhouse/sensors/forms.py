from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms_components import DateTimeField, DateRange
from werkzeug.datastructures import MultiDict
from wtforms.fields import SubmitField, DateField, StringField, SelectField, IntegerField
from datetime import datetime
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime

class CityForm(FlaskForm):
	state = SelectField('state', choices=[('CA', 'California'), ('NV', 'Nevada')])
	city = SelectField('city', choices=[])
	
	
class SensorForm(FlaskForm):
	owner = StringField('Enter Your Name')
	sensors_owned = SelectField('Sensor List', choices=[])
	start_date = DateTimeLocalField('Start Date', default=datetime.now())
	end_date = DateTimeLocalField('End Date', default=datetime.now())
	interval = IntegerField('Time Interval (must be a multiple of 10 minutes)')
	def validate_interval(form, interval):	# custom validators must be named "validate_<name of variable>".
		if (interval.data % 10): 
			raise ValidationError("Values must be a multiple of 10.")
		
class SensorRegistrationForm(FlaskForm):
	owner = StringField('Enter Your Name', validators=[DataRequired()])
	sensor_name = StringField('Enter The Name of the Sensor')
	units = StringField('Enter what units this sensor is measuring')
	protocol = IntegerField('Enter what protocol this sensor is using (optional at the moment)')
	submit = SubmitField('Register your sensor')

