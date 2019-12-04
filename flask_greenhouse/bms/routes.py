# imports
from flask import render_template, request, Blueprint,flash, url_for, jsonify
from flask_greenhouse.forms import Date_Form
from flask_greenhouse.models import BMSDataentry
from flask_greenhouse.utils.plot import plot_graph, plot_date
from flask_greenhouse import db
import os
import json
from datetime import datetime, timedelta

# export this blueprint as "bms". Will be imported at __init__.py in the main folder.
bms = Blueprint("bms", __name__, static_folder='flask_greenhouse/static')

@bms.route("/BMS", methods=["POST", "GET"])
def BMS_JS():
	return render_template("BMS.html", title="JS BMS data loader")

@bms.route("/BMS/serverside", methods=["POST", "GET"])
def BMS():
	form = Date_Form()
	if form.validate_on_submit():	
		#flash arguments; message, HTML class of message
		# flash this message when you submit this page.
		flash("Your request has been handled. Scroll down for your graph", 'success')
		
		# retrieve the start date and the end date from the form.
		# because it came from an HTML5 date form, it will automatically come in a datetime object.
		start_date = form.start_date.data
		end_date = form.end_date.data
		
		#request all data points from the BMS table that were posted after the start date, and before the end date.
		data_request = BMSDataentry.query.filter(BMSDataentry.date_posted < end_date).filter(BMSDataentry.date_posted > start_date)
		
		#filter the data request by making sure the dates are in intervals of the form interval. 
		#the form has a validator that says the integer must be a multiple of 10.
		
		interval = form.interval.data
		
		intervaled_data_request = [];
		


# create a unit test.
		#if it's the battery charge:
		if form.y_axis.data == 'test':
				# fill in the x_data range with dummy values, starting from now to 40 minutes from now in steps of 10.
			# this guarantees 4 date points which the dummy y data will automatically correlate.
			x_data = [(datetime.now() + timedelta(minutes=step)) for step in range(0,40,10)]
			y_data = [4,6,8,10]
			x_label = "x-axis dummy data"
			y_label = "y-axis dummy data"
			title = "Hello world"
			style = form.style.data
			marker = form.marker.data
			tight_layout = True
			logarithmic_scale = False
			linestyle='solid'
			date_format = "%H:%M"
		else:
			#retrieve the data, and put it into x_data and y_data.
			x_data = []
			y_data = []
			for entry in data_request:
				x_data.append(entry.date_posted)
				y_data.append(entry.JSON_content["Battery Charge"]["battery charge"])
			x_label = form.xlabel.data
			y_label = form.ylabel.data
			title = form.title.data
			style = form.style.data
			marker = form.marker.data
			tight_layout = form.tight_layout.data
			logarithmic_scale = form.logarithmic_scale.data
			date_format = form.date_format.data
			linestyle='solid'
		
		#build the filepath.
		filepath = "flask_greenhouse/static/graphs/"#os.path.join(app.root_path, 'static/graphs/')	
		filename = "plot.png"
		
		# delete existing graph just in case. might change later this later and just rename it for every sensor.
		if os.path.exists(filepath+filename):
			os.remove(filepath+filename)
		
		#saves a graph to the filepath. (root/static/graphs/plot.png)
		plot_date(x_data, y_data, x_label, y_label, title, filepath, filename,
					style=style, marker=marker, logarithmic_scale=logarithmic_scale,
					tight_layout=tight_layout, linestyle=linestyle,
					date_format=date_format)
		
		return render_template('BMS_Server_side.html', form=form, graph=filename)
	return render_template('BMS_Server_side.html', form=form)

#################################################################################################
#								Miscellaneous 
#################################################################################################

@bms.route("/BMS/instantaneous", methods=["GET"])
@bms.route("/BMS/Instantaneous", methods=["GET"])
def BMS_Instantaneous():
	"""
		The Route to see Instantaneous BMS data.
		
		At the moment, it just loads a test file.
	"""
	filepath = "flask_greenhouse/BMS_test_file.json"
	with open(filepath, "r") as fp:	
		data = json.load(fp)
	return render_template("BMS_Instantaneous.html", data=data)

@bms.route("/BMS/pins", methods=["GET"])
def BMS_pins():
	"""
		The Route to see what Pins are currently attached.
		
		Reads from the current instantantous file.  
	"""
	filepath = "flask_greenhouse/BMS_test_file.json"
	with open(filepath, "r") as fp:	
		data = json.load(fp)
		pins = data["BMS Status"]["Pins Connected"]
	p = pins.split(',')
	return render_template("BMS_pins.html", pins=p)

# post BMS JSON data to this address.
@bms.route("/BMS/post-json", methods=["POST"]) #get requests will be blocked.
def BMS_Post():
	"""
		The route for which BMS JSON data is posted. Will be sent by the Raspberry Pi we have on site.
	"""
	req_data = request.get_json() #extract JSON data from your request
	new_BMS_entry = BMSDataentry(JSON_content=req_data) # create new instance of 
	db.session.add(new_BMS_entry)
	db.session.commit()
	return "your data has been received."
	
#################################################################################################
#									APIs
#								Getting BMS Data.
#################################################################################################
i = 1
@bms.route("/BMS/api/single_point/<string:date>/<string:parameter>", methods=["GET"])
def BMS_data_retrieval(date, parameter):
	"""
		Returns a single data point.
		
		Arguments:
			date: what date do you want to request?
			parameter: what parameter do you want?
		Returns:
			A JSON file. 
			Example:
			{
				"x": 1,
				"date": "2019-10-31 10:30:30",
				"parameter": "battery charge"
			}
		
	"""
	global i
	#####print(date)
	datetime_from_JS = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
	#####print(datetime_from_JS)
	#####print(parameter)
	# Search for BMS entries with a buffer of 10 minutes
	entry = BMSDataentry.query \
			.filter( BMSDataentry.date_posted \
				.between(datetime_from_JS - timedelta(seconds=30), 
						 datetime_from_JS + timedelta(minutes=30)))\
				.first_or_404()
	final_entry_date = entry.date_posted
	j = entry.JSON_content
	return j
	
	#####print(entry)
	JSON_response = {
		
		"date": final_entry_date.strftime("%Y-%m-%d %H:%M:%S"),
		"parameter": parameter,
		"value": i
	}
	i += 1
	return jsonify(JSON_response)
	
@bms.route("/BMS/api/<string:start_date>/<string:end_date>/<int:interval>/<string:parameter>", methods=["GET"])
def BMS_multi_data_retrieval(start_date, end_date, interval, parameter):
	"""
		A server-side multi-data-point retrieval system.
		Arguments:
			start_date, end_date: from what date to what date do you want your points?
			interval (in minutes).
			parameter: what parameter do you want JSON data from?
		Returns:
			A JSON file.
			Example:
			{
				"parameter": "Battery Charge",
				"data": {
					"2019-10-31 10:30:44": 1,
					"2019-10-31 10:40:44": 2,
					"2019-10-31 10:50:44": 3,
					"2019-10-31 11:00:44": 4,
					"2019-10-31 11:10:44": 5,
					"2019-10-31 11:20:44": 5,
					"2019-10-31 11:30:44": 6
				}
			}
	"""
	
	global i
	# extrapolate dates from start, end, and interval.
	s = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
	e = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
	dates = []
	while(s < e):
		dates.append(s)
		s = s + timedelta(minutes=interval)
	
	# retrieve data from database based on date for all dates.
	data = {}
	for date in dates:
		data[date.strftime("%Y-%m-%d %H:%M:%S")] = i
		i += 1
	
	# construct JSON response. 
	JSON_response = {
		"parameter": parameter,
		"data": data
	}
	return jsonify(JSON_response)