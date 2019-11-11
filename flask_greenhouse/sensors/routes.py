# imports 
from flask import render_template, request, Blueprint,flash, url_for, jsonify, redirect

from flask_greenhouse.forms import Date_Form
from flask_greenhouse.models import BMSDataentry
from flask_greenhouse.utils.plot import plot_graph
from flask_greenhouse import db
from flask_greenhouse.sensors.forms import CityForm, SensorForm, SensorRegistrationForm
from flask_greenhouse.sensors.models import City, Sensor, SensorDataEntry

import os
from datetime import datetime

#export our Blueprint as "sensor_nodes".
sensor_nodes = Blueprint("sensor_nodes", __name__, static_folder='flask_greenhouse/static')


# our route decorators
# main route decorator for sensor data retrieval form.
# this one's written in JavaScript. see sensors.js for details.
@sensor_nodes.route("/sensors/", methods=["POST", "GET"])
@sensor_nodes.route("/sensors", methods=["POST", "GET"])
def sensors():
	form = SensorForm()
	if form.validate_on_submit():	
		flash(f"Your request has been receieved. Scroll down for your graph.")
		
	return render_template("sensors.html", title="sensors",form=form)

# This route only returns a JSON file containing the sensor id, the name, and the units in which the sensors store information.
# It retrives data from our SQLite database (automatically grabs it from our Sensor class table).
# It retrives all sensors owned by a specified owner (e.g. Bob).
# All sensors owned by Bob are contained in sObj.
# returns a JSON object with 'sensors': sObj as its content.
@sensor_nodes.route("/sensors/people/<owner>", methods=["POST", "GET"])
def retrive_sensors(owner):
	sensors = Sensor.query.filter_by(owner=owner).all()
	sensorArray = []
	for sensor in sensors: 
		sObj = {}
		sObj['id'] = sensor.id;
		sObj['name'] = sensor.name;
		sObj['units'] = sensor.units;
		sensorArray.append(sObj)
	return jsonify({'sensors': sensorArray})

# Sensor Registration Form.
# allows you to register a sensor. 
@sensor_nodes.route("/sensors/register", methods=["POST","GET"])
def register():
	form = SensorRegistrationForm()
	
	# I couldn't get the form to validate_on_submit, so I'm just making it take all POST requests, regardless of
	# whether or not they're valid. It's not secure, but it needs to work NOW. I'M TIRED.
	if request.method=="POST":
		flash("Your sensor has been registered", "success")
		new_sensor_entry = Sensor(owner=form.owner.data, name=form.sensor_name.data, units=form.units.data)
		db.session.add(new_sensor_entry)
		db.session.commit()
		return redirect(url_for('sensor_nodes.sensors'))
		# if form.validate_on_submit():
		# flash("Your sensor has been registered", "success")
		# new_sensor_entry = Sensor(owner=form.owner.data, name=form.sensor_name.data, units=form.units.data)
		# db.session.add(new_sensor_entry)
		# db.session.commit()
		# return redirect(url_for('sensor_nodes.sensors'))
	return render_template("register.html", title="Register",form=form)

# this is the route where you post JSON data to from your Sensor.
@sensor_nodes.route("/sensors/post-json/<int:owner_id>/<int:sensor>", methods=["POST"])
def sensor_json(owner, sensor):
	req_data = request.get_json() # extract JSON data from POST request.
	print(str(owner)) # print for debugging
	print(str(sensor))
	new_sensor_data_entry = SensorDataEntry(JSON_content=req_data, sensor=sensor)
			#create new instance of Sensor Data entry, link it to sensor
	db.session.add(new_sensor_data_entry) # post it to the database
	db.session.commit()
	return "your data has been received."

@sensor_nodes.route("/sensors/<int:sensor_id>/getall")
def get_all_sensor_data(sensor_id):
	sensor = Sensor.query.filter_by(id=sensor_id) # find the sensor in the database by ID number.
	dataset = SensorDataEntry.query.filter_by(author=sensor)\
				.order_by(SensorDataEntry.date_posted.desc())
	#HTML_template = query.toHTML()
	return render_template("get_all.html", sensor=sensor, dataset=dataset)
	
	
	
	
	
	
	
	
	
	
	
	
	
#test 
@sensor_nodes.route("/sensors/cities", methods=["POST", "GET"])
def city_listing():
	form = CityForm()
	form.city.choices = [(city.id, city.name) for city in City.query.filter_by(state='CA').all()]
	return render_template("cities.html", title="City Monitoring", form=form)
	

@sensor_nodes.route("/sensors/cities/<state>")
def city(state):
	cities = City.query.filter_by(state=state).all()
	cityArray = []
	for city in cities:
		cityObj = {}
		cityObj['id'] = city.id
		cityObj['name'] = city.name
		cityArray.append(cityObj)
	return jsonify({'cities':cityArray})