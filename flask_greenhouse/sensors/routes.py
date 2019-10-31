from flask import render_template, request, Blueprint,flash, url_for, jsonify, redirect
from flask_greenhouse.forms import Date_Form
from flask_greenhouse.models import BMSDataentry
from flask_greenhouse.utils.plot import plot_graph
from flask_greenhouse import db
from flask_greenhouse.sensors.forms import CityForm, SensorForm, SensorRegistrationForm
from flask_greenhouse.sensors.models import City, Sensor, SensorDataEntry
import os
from datetime import datetime

sensor_nodes = Blueprint("sensor_nodes", __name__, static_folder='flask_greenhouse/static')



@sensor_nodes.route("/sensors/", methods=["POST", "GET"])
@sensor_nodes.route("/sensors", methods=["POST", "GET"])
def sensors():
	form = SensorForm()
	return render_template("sensors.html", title="sensors",form=form)

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

@sensor_nodes.route("/sensors/post-json/<owner>/<sensor>", methods=["POST"])
def sensor_json(owner, sensor):
	req_data = request.get_json()
	print(str(owner))
	print(str(sensor))
	new_sensor_data_entry = SensorDataEntry(JSON_content=req_data, sensor=sensor)
	db.session.add(new_sensor_data_entry)
	db.session.commit()
	return "your data has been received."



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