# imports 
from flask import render_template, request, Blueprint,flash, url_for, jsonify, redirect

from flask_greenhouse.forms import Date_Form
from flask_greenhouse.models import BMSDataentry
from flask_greenhouse.utils.plot import plot_graph
from flask_greenhouse import db, login_manager, bcrypt
from flask_greenhouse.sensors.forms import CityForm
from flask_greenhouse.sensors.forms import UserRegistrationForm, UserLoginForm, SensorRequestForm, SensorRegistrationForm
from flask_greenhouse.sensors.models import City, User, Sensor, SensorDataEntry

from flask_login import login_required, login_user, current_user, logout_user


import os
from datetime import datetime, timedelta

#export our Blueprint as "sensor_nodes".
sensor_nodes = Blueprint("sensor_nodes", __name__, static_folder='flask_greenhouse/static')

#tells the login manager how to load users.
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# our route decorators
# main route decorator for sensor data retrieval form.
# this one's written in JavaScript. see sensors.js for details.
# only works if the user is logged in.
#@login_required
@sensor_nodes.route("/sensors/", methods=["POST", "GET"])
@sensor_nodes.route("/sensors", methods=["POST", "GET"])
def sensors():
	# if you're not logged in, redirect to the login page.
	if not current_user.is_authenticated:
		return redirect(url_for('sensor_nodes.user_login'))
	# retrieve sensor choices from database, then add them to the form.
	sensor_results = Sensor.query.filter_by(user_id = current_user.id).all()
	# one line for loop warning.
	# returns a tuple with 
	sensor_list = [(sensor.id, sensor.name) for sensor in sensor_results]
	print(sensor_list)
	form = SensorRequestForm()
	form.sensors_owned.choices = sensor_list
	if form.validate_on_submit():	
		flash(f"Your request has been receieved. Scroll down for your graph.")
		
	return render_template("sensors.html", title="sensors", form=form)



# @sensor_nodes.route("/sensors/users/<string:username>")
# def sensors_by_username(username):
	# user = User.query.filter_by(username=username).first()
	
# junk code:
# This route only returns a JSON file containing the sensor id, the name, and the units in which the sensors store information.
# It retrives data from our SQLite database (automatically grabs it from our Sensor class table).
# It retrives all sensors owned by a specified owner (e.g. Bob).
# All sensors owned by Bob are contained in sObj.
# returns a JSON object with 'sensors': sObj as its content.
# @sensor_nodes.route("/sensors/users/<owner>", methods=["POST", "GET"])
# def retrive_sensors(owner):
	# sensors = Sensor.query.filter_by(owner=owner).all()
	# sensorArray = []
	# for sensor in sensors: 
		# sObj = {}
		# sObj['id'] = sensor.id;
		# sObj['name'] = sensor.name;
		# sObj['units'] = sensor.units;
		# sensorArray.append(sObj)
	# return jsonify({'sensors': sensorArray})

# Sensor Registration Form.
# allows you to register a sensor. 
@sensor_nodes.route("/sensors/register", methods=["POST","GET"])
@login_required
def register_sensor():
	form = SensorRegistrationForm()
	# I couldn't get the form to validate_on_submit, so I'm just making it take all POST requests, regardless of
	# whether or not they're valid. It's not secure, but it needs to work NOW. I'M TIRED.
	if form.validate_on_submit():
		flash("Your sensor has been registered", "success")
		new_sensor_entry = Sensor(user_id = current_user.id,name=form.sensor_name.data, units=form.units.data)
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

# registers a user into the database.
# hashes a password from our password field. 
@sensor_nodes.route("/sensors/users/register", methods=["POST", "GET"])
def register_user():
	if current_user.is_authenticated: 
		return redirect(url_for('sensor_nodes.sensors'))
	form = UserRegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data)
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash("You have been registered", 'success')	
		return redirect(url_for('sensor_nodes.user_login'))
	return render_template('user_register.html', form=form)

# logs in a user
# checks password using bcrypt.check_password_hash()
@sensor_nodes.route("/sensors/users/login", methods=["POST", "GET"])
def user_login():
	form = UserLoginForm();
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember = form.remember.data)
			flash("You have been logged in", 'success')
			return redirect(url_for('sensor_nodes.sensors'))
		flash('Login attempt unsuccessful. Check username or password.', 'danger')
	return render_template('user_login.html', title="Login", form=form)

# logs out a user.
@sensor_nodes.route("/logout")
def user_logout():
	logout_user()
	return redirect(url_for('main.home'))
	
	

# this is the route where you post JSON data to from your Sensor.
@sensor_nodes.route("/sensors/post-json/<string:username>/<string:sensor_name>", methods=["POST"])
def sensor_json(username, sensor_name):
	user = User.query.filter_by(username=username).first()
	if not user:
		return "Username is incorrect."
	sensor = Sensor.query.filter_by(name=sensor_name).first()
	print(sensor)
	sensorlist = user.sensorlist
	print(sensorlist)
	if sensor not in sensorlist: 
		return "Sensor not found."
	req_data = request.get_json() # extract JSON data from POST request.
	
	new_sensor_data_entry = SensorDataEntry(JSON_content=req_data, sensor_id=sensor.id)
			#create new instance of Sensor Data entry, link it to sensor
	db.session.add(new_sensor_data_entry) # post it to the database
	db.session.commit()
	return "your data has been received."

# get all data by sensor ID number.
@sensor_nodes.route("/sensors/get-data-by-sensor-id/<int:sensor_id>")
def get_all_sensor_data(sensor_id):
	sensor = Sensor.query.filter_by(id=sensor_id).first() # find the sensor in the database by ID number.
	dataset = sensor.dataset #SensorDataEntry.query.filter_by(author=sensor).order_by(SensorDataEntry.date_posted.desc())
	print(dataset)
	#HTML_template = query.toHTML()
	return render_template("get_all.html", sensor=sensor, dataset=dataset)
	
@sensor_nodes.route("/sensors/get-sensor-json-data-by-id/<int:sensor_id>/<string:date>")
def sensor_id_JSON(sensor_id,date):
	sensor = Sensor.query.filter_by(id=sensor_id).first() # find the sensor in the database by ID number.
	dataset = sensor.dataset #SensorDataEntry.query.filter_by(author=sensor).order_by(SensorDataEntry.date_posted.desc())
	
	date_requested = datetime.strptime(date, "%M-%d-%Y")
	
	for data in dataset:
		if inRange(data.date_posted,date_requested):
			return data.JSON_content
	return "{\"lux\": 1234}"
	
		
	
def inRange(date_posted, date_requested, interval=timedelta(minutes=10)):
	if date_requested > (date_posted + interval):
		return True
	elif date_requested < (date_posted - interval):
		return True
	else:
		return False 
	
	
	
	
	
	
	
	
	
	
	
	
	
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