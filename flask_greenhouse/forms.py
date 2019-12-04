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
bms_options = [ 
				# Voltage Data
				('average_cell_voltage', 'Average Cell Voltage'),
				('maximum_cell_voltage', 'Maximum Cell Voltage'),
				('minimum_cell_voltage', 'Minimum Cell Voltage'),
				('total_voltage', 'Total Voltage'),
				
				# Current Data
				('total_current', 'Total Battery Current'),
				('a_current', 'PV array Current'),

				# Balancing Rate Choices
				('a_cell_b_rate', 'Average Cell Balancing Rate'),
				
				# Temperature Data Choices
				('a_cell_temperature', 'Average Cell Temperature'),
				('max_cell_temperature', 'Maximum Cell Temperature'),
				('min_cell_temperature', 'Minimum Cell Temperature'),
				('a_cell_m_temperature', 'Average Cell Module Temperature'),
				('max_cell_m_temperature', 'Maximum Cell Module Temperature'),
				('min_cell_m_temperature', 'Minimum Cell Module Temperature'),
				
				# Battery Charge Data
				('battery_capacity', 'Battery Capacity'),
				('battery_charge', 'Battery Charge'),
				('state_of_charge', 'State of Charge'),
				
				# Miscellaneous
				('test', 'Test Option (don\'t pick this one)')
			]
tristar_options = [
				#ADC readings
				('bat_voltage', "Battery Voltage"),
				('bat_terminal_voltage', "battery terminal voltage"),
				('bat_sense_voltage', "battery sense voltage"),
				('array_voltage', "array voltage"),
				('bat_current', "battery current"),
				('array_current', "array current"),
				('12V_supply', "12V supply"),
				('3V_supply',"3V supply"),
				('meterbus_voltage', "meterbus voltage"),
				('1_8V_supply', "1.8V supply"),
				('v_ref', "reference voltage"),
				
				# Temperature readings
				("temp_h","heatsink temperature"),
				("temp_rts","RTS temperature"),
				("temp_bat_reg","battery regulation temperature"),
				
				#status
				("charging_current","charging_current"),
				("min_bat_voltage","minimum battery voltage"),
				("max_bat_voltage","maximum battery voltage"),
				
				#Charger Data
				("ah_resettable","Ah Charge Resettable"),
				("ah_total","Ah Charge Total"),
				("kwhr_resettable","kWhr Charge Resettable"),
				("kwhr_total","kWhr Charge Total"),
				
				#MPPT data
				("p_out","output power"),
				("p_in","input power"),
				("V_max_power","max power of last sweep"),
				("V_mp","Vmp of last sweep"),
				("V_oc","Voc of last sweep"),
				
				#Daily Logger Values
				("bat_min_voltage_daily","Battery Voltage Minimum Daily"),
				("bat_max_voltage_daily","Battery Voltage Maximum Daily"),
				("input_voltage_max_daily","Input Voltage Maximum Daily"),
				("Ah_daily","Amp Hours accumulated daily"),
				("Wh_daily","Watt Hours accumulated daily"),
				("P_max_daily","Maximum power output daily"),
				("min_temp_daily","Minimum temperature daily"),
				("max_temp_daily","Minimum temperature daily"),
				("time_ab_daily","time_ab_daily"),
				("time_eq_daily","time_eq_daily"),
				("time_fl_daily","time_fl_daily")
	
			]
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
	units = SelectField('Units', choices = bms_options, default="battery_charge")
	
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


# The form we use to request BMS data.
class Tristar_Form(FlaskForm):
	
	# type of data to be graphed 
	units = SelectField('Units', choices = tristar_options, default="battery_charge")
	
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