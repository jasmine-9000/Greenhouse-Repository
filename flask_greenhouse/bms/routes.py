from flask import render_template, request, Blueprint,flash, url_for
from flask_greenhouse.forms import Date_Form
from flask_greenhouse.models import BMSDataentry
from flask_greenhouse.utils.plot import plot_graph, plot_date
from flask_greenhouse import db
import os
from datetime import datetime, timedelta

bms = Blueprint("bms", __name__, static_folder='flask_greenhouse/static')

@bms.route("/BMS", methods=["POST", "GET"])
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
		

		#if it's the battery charge:
		if form.y_axis.data == 'battery_charge':
			x_data = []
			y_data = []
			for entry in data_request:
				x_data.append(entry.date_posted)
				y_data.append(entry.JSON_content["Battery Charge"]["battery charge"])
			x_label = "Time"
			y_label = "Charge (A)"
			title = form.title.data
			
		else:
			# fill in the x_data range with dummy values, starting from now to 40 minutes from now in steps of 10.
			# this guarantees 4 date points which the dummy y data will automatically correlate.
			x_data = [(datetime.now() + timedelta(minutes=step)) for step in range(0,40,10)]
			y_data = [4,6,8,10]
			x_label = "x-axis dummy data"
			y_label = "y-axis dummy data"
			title = "Hello world"
		
		#build the filepath.
		filepath = "flask_greenhouse/static/graphs/"#os.path.join(app.root_path, 'static/graphs/')	
		filename = "plot.png"
		
		# delete existing graph just in case. might change later this later and just rename it for every sensor.
		if os.path.exists(filepath+filename):
			os.remove(filepath+filename)
		
		#saves a graph to the filepath. (root/static/graphs/plot.png)
		plot_date(x_data, y_data, x_label, y_label, title, filepath, filename)
		
		return render_template('BMS.html', form=form, graph=filename)
	return render_template('BMS.html', form=form)
#post BMS JSON data to this address.
@bms.route("/BMS/post-json", methods=["POST"]) #get requests will be blocked.
def BMS_Post():
	req_data = request.get_json()
	new_BMS_entry = BMSDataentry(JSON_content=req_data)
	db.session.add(new_BMS_entry)
	db.session.commit()
	return "your data has been received."