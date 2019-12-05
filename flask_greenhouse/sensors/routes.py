#############################################################################################################################
#								IMPORTS																						#
#############################################################################################################################
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

#############################################################################################################################
# 								LOGIN DECORATORS																			#
#############################################################################################################################
#tells the login manager how to load users.
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


#############################################################################################################################
#								ROUTE DECORATORS																			#
#############################################################################################################################


#############################################################################################################################
#								MAIN GRAPHING ROUTE																			#
#############################################################################################################################

# main route decorator for sensor data retrieval form.
# this one's written in JavaScript. see sensors.js for details.
# only works if the user is logged in.

@login_required
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

#############################################################################################################################
#								SENSOR REGISTRATION FORM																	#
#############################################################################################################################

# Requires you to be logged in.
# Automatically ties the sensor to the logged in user.
# 

@sensor_nodes.route("/sensors/register", methods=["POST","GET"])
@login_required
def register_sensor():
	form = SensorRegistrationForm()
	if form.validate_on_submit():
		flash("Your sensor has been registered", "success")
		# create new sensor, and tie it to the current user.
		new_sensor_entry = Sensor(user_id = current_user.id,name=form.sensor_name.data, units=form.units.data)
		# add new sensor to database.
		db.session.add(new_sensor_entry)
		db.session.commit()
		return redirect(url_for('sensor_nodes.sensors'))
	return render_template("register.html", title="Register",form=form)
	
#############################################################################################################################
# 								USER REGISTRATION FORM																		#
#############################################################################################################################

# Registers a new user.
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

#############################################################################################################################
#								USER LOGIN FORM																				#
#############################################################################################################################

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

#############################################################################################################################
#									USER LOGOUT ROUTE																			#
#############################################################################################################################

# Navigating to this URL logs out a user.

@sensor_nodes.route("/logout")
def user_logout():
	logout_user()
	return redirect(url_for('main.home'))
	
#############################################################################################################################	
#									POST ROUTE																				#
#############################################################################################################################
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
	
#############################################################################################################################
#									DATA RETRIEVAL API																		#
#############################################################################################################################


#############################################################################################################################
#									RETRIEVE ALL DATAPOINTS BY SENSOR_ID ROUTE												#
#############################################################################################################################

# get ALL data by sensor ID number in JSON format.
# mostly for debugging.

@sensor_nodes.route("/sensors/get-data-by-sensor-id/<int:sensor_id>")
def get_all_sensor_data(sensor_id):
	sensor = Sensor.query.filter_by(id=sensor_id).first() # find the sensor in the database by ID number.
	dataset = sensor.dataset # SensorDataEntry.query.filter_by(author=sensor).order_by(SensorDataEntry.date_posted.desc())
	print(dataset) # debugging statement.
	return render_template("get_all.html", sensor=sensor, dataset=dataset)

#############################################################################################################################
#									RETRIEVE DATAPOINT BY SENSOR_ID AND DATE ROUTE											#
#############################################################################################################################

# get data point by date and sensor_id

@sensor_nodes.route("/sensors/get-sensor-json-data-by-id/<int:sensor_id>/<string:date>")
def sensor_id_JSON(sensor_id,date):
	sensor = Sensor.query.filter_by(id=sensor_id).first() # find the sensor in the database by ID number.
	dataset = sensor.dataset #SensorDataEntry.query.filter_by(author=sensor).order_by(SensorDataEntry.date_posted.desc())
	# extrapolate a Datetime object from the string.
	date_requested = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
	for data in dataset:
		if inRange(data.date_posted,date_requested):
			return data.JSON_content
	return jsonify("{\"lux\": 1234}")

#############################################################################################################################
#									RETRIEVE DATAPOINTS BY SENSOR_ID BETWEEN START_DATE AND END_DATE ROUTE					#
#############################################################################################################################
@sensor_nodes.route("/sensors/get-sensor-json-data-range/<int:sensor_id>/<string:start_date>/<string:end_date>/<int:interval>", methods=["GET"])
def sensor_id_JSON_range(sensor_id, start_date, end_date, interval):
	# extrapolate dates requested.
	s = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
	e = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
	dates = []
	while(s < e):
		dates.append(s)
		s = s + timedelta(minutes=interval)
	
	# start querying the database.
	Table = SensorDataEntry
	buffer = timedelta(minutes=interval)
	data = {}
	# iterate throughout all dates.
	for date in dates:
		value = None
		entry = Table.query \
			.filter( 
				sensor_id = sensor_id,
				Table.date_posted \
				.between(date - buffer, 
						 date + buffer))\
				.first()
		# only add a new entry into the data dict() if there's an entry.
		try:
			dict = entry.JSON_content
			data[entry.date_posted.strftime("%Y-%m-%d %H:%M:%S")] = dict
		except:
			pass
	return data
	
	
#############################################################################################################################
#									HELPER FUNCTIONS																		#		
#############################################################################################################################	

# inRange:
# determines whether or not a date requested is in range of the date posted.
# 	Arguments:
#		date_posted: what date was the data point actually posted?
#		date_requested: what date are you requesting from?
# 		interval: what interval do you want? 
#			Type: timedelta class
#	Returns:
# 		True if in Range
#		False otherwise
def inRange(date_posted, date_requested, interval=timedelta(minutes=10)):
	if date_requested > (date_posted + interval):
		return True
	elif date_requested < (date_posted - interval):
		return True
	else:
		return False 
	
	
	
	
	
	
	
	
	
	
	
#############################################################################################################################
#												TESTING AREA																#
#############################################################################################################################	
	
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