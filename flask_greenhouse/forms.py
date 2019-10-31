from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms_components import DateTimeField, DateRange
from werkzeug.datastructures import MultiDict
from wtforms.fields import SubmitField, DateField, StringField, SelectField, IntegerField
from datetime import datetime
from wtforms.fields.html5 import DateTimeLocalField

bms_options = [ ('b_voltage', 'Battery Voltage'),
			('a_voltage', 'PV array Voltage'),
			('b_current', 'Battery Current'),
			('a_current', 'PV array Current'),
			('battery_charge', 'Battery Charge')]

class Date_Form(FlaskForm):
	y_axis = SelectField('Value', choices = bms_options)
	
	start_date= DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M', default=datetime.today())
	end_date = 	DateTimeLocalField('End Date', format='%Y-%m-%dT%H:%M', default=datetime.today())
	
	title = StringField('Title')
	
	def validate_end_date(form, field):
		if field.data < form.start_date.data:
			raise ValidationError("Start date must be before end date.")
	interval = IntegerField('Interval (minutes)', validators=[DataRequired()], default=10)
	def validate_interval(form, interval):	
		if (interval.data % 10): 
			raise ValidationError("Values must be a multiple of 10.")
	submit = SubmitField('Request Graph')
	
# sources:

#https://stackoverflow.com/questions/49697545/flask-wtform-datetimefield-rendering-issue
#https://stackoverflow.com/questions/52825708/wtforms-datetimelocalfield-data-is-none-after-submit
#https://stackoverflow.com/questions/56185306/how-to-validate-a-datefield-in-wtforms
#favorite_date = DateTimeLocalField('Which date is your favorite?', format='%Y-%m-%dT%H:%M')