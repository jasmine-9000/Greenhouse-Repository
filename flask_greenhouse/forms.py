# imports
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms_components import DateTimeField, DateRange
from werkzeug.datastructures import MultiDict
from wtforms.fields import SubmitField, DateField, StringField, SelectField, IntegerField, BooleanField
from datetime import datetime
from wtforms.fields.html5 import DateTimeLocalField

# global variables 
# our options that our BMS can have.
bms_options = [ ('b_voltage', 'Battery Voltage'),
			('a_voltage', 'PV array Voltage'),
			('b_current', 'Battery Current'),
			('a_current', 'PV array Current'),
			('battery_charge', 'Battery Charge'),
			('test', 'Test Option (don\'t pick this one)')]
# the ways we can style our Graph
style_options = [
			('bmh', "BMH"),
			('classic',  'classic'),
			('dark_background', 'dark_background'),
			('fast','fast'),
			('fivethirtyeight','fivethirtyeight'),
			('ggplot', 'ggplot'),
			('grayscale','grayscale'),
			('seaborn-bright', 'seaborn-bright'), 
			('seaborn-colorblind','seaborn-colorblind'),
			('seaborn-dark-palette','seaborn-dark-palette'),
			('seaborn-dark', 'seaborn-dark' ),
			('seaborn-darkgrid', 'seaborn-darkgrid'),
			('seaborn-deep','seaborn-deep'),
			('seaborn-muted','seaborn-muted'),
			('seaborn-notebook','seaborn-notebook'),
			('seaborn-paper', 'seaborn-paper'), 
			('seaborn-pastel','seaborn-pastel'),
			('seaborn-poster','seaborn-poster'),
			('seaborn-talk', 'seaborn-talk'),
			('seaborn-ticks','seaborn-ticks'),
			('seaborn-white', 'seaborn-white'),
			('seaborn-whitegrid', 'seaborn-whitegrid'),
			('seaborn', 'seaborn'),
			('Solarize_Light2', 'Solarize_Light2'),
			('tableau-colorblind10', 'tableau-colorblind10'),
			('_classic_test', '_classic_test') 
			]
# the ways we can style our marker.
marker_options = [(".", "point"),
				(",", "pixel"),
				("o", "circle"),
				("v", "triangle down"),
				("^", "triangle up"),
				("<", "triangle left"),
				(">", "triangle right"),
				("None", "No Marker")]
					

# The form we use to request BMS data.
class Date_Form(FlaskForm):
	
	# type of data to be graphed 
	y_axis = SelectField('Value', choices = bms_options, default="battery_charge")
	
	#from what date
	start_date= DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M', default=datetime.today())
	#to what date
	end_date = 	DateTimeLocalField('End Date', format='%Y-%m-%dT%H:%M', default=datetime.today())
	

	# date validators.
	# start date must be before end date. or else, matplotlib complains.
	def validate_end_date(form, field):
		if field.data < form.start_date.data:
			raise ValidationError("Start date must be before end date.")
	
	# interval (must be a multiple of 10 minutes. Minimum is 10 minutes.)
	interval = IntegerField('Interval (minutes)', validators=[DataRequired()], default=10)
	def validate_interval(form, interval):	
		if (interval.data % 10): 
			raise ValidationError("Values must be a multiple of 10.")
		if (interval.data <= 0): 
			raise ValidationError("Value must be greater than 0.")
	
	# data about the graph (title, xlabel, ylabel, date format)
	title = StringField('Title', default = "Untitled Graph")
	xlabel = StringField('X-axis title', default = "")
	ylabel = StringField('Y-axis title', default = "")
	date_format = StringField('Date Format (optional)')
	
	# graph style options
	style = SelectField('Style', choices = style_options, default='fivethirtyeight')
	tight_layout = BooleanField('Tight Layout', default=False)
	logarithmic_scale = BooleanField('Logarithmic Scale (Y-axis)', default=False)
	marker = SelectField('Marker', choices=marker_options, default="None")
	submit = SubmitField('Request Graph')
	
# sources:

#https://stackoverflow.com/questions/49697545/flask-wtform-datetimefield-rendering-issue
#https://stackoverflow.com/questions/52825708/wtforms-datetimelocalfield-data-is-none-after-submit
#https://stackoverflow.com/questions/56185306/how-to-validate-a-datefield-in-wtforms
#favorite_date = DateTimeLocalField('Which date is your favorite?', format='%Y-%m-%dT%H:%M')
# https://matplotlib.org/3.1.1/api/markers_api.html
