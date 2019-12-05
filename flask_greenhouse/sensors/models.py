#############################################################################################################################
#							IMPORTS																							#
#############################################################################################################################
from flask_greenhouse import db, admin
from datetime import datetime
import json
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_admin.contrib.sqla import ModelView





 
#############################################################################################################################
#							INHERITABLE MODELS																				#
#############################################################################################################################

# this class enables JSON storage.
# it inherits the TypeDecorator class, so we need to redefine process_bind_param and process_result_value.
# It needs to save to a SQLlite database as a string. We can pass in a dictionary, and it will convert to string.
# When we load the value, it will automatically convert it back to dictionary format with json.loads().

class JsonEncodedDict(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly.
	source: https://www.michaelcho.me/article/json-field-type-in-sqlalchemy-flask-python"""
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)
		

#############################################################################################################################		
# 						LOGIN REQUIRED MODELS																				#
#############################################################################################################################

#############################################################################################################################
# 						USER MODEL																							#
#############################################################################################################################

# username:
# 	If it's a faculty sensor, name="Admin"
# 	if it's a student sensor, name="<name of student>"
# email:
# 	used for password resets
# password:
# 	encrypted using SHA-256 encryption. the login route hashes it against a secret key defined in config.json.
# sensorlist:
#	a list of sensors this user has. We are back-referenced by our sensors as 'master'.
class User(db.Model, UserMixin):
	__tablename__ = 'User'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(60), unique=True, nullable=False)
	email = db.Column(db.String(60), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	sensorlist = db.relationship('Sensor', backref='master', lazy=True)
	
	def __repr__(self):
		return f"User('{self.username}, '{self.sensorlist}')"
		
#############################################################################################################################
# 						SENSOR MODEL 																						#
#############################################################################################################################

# Name:
# 	Name of the sensor (e.g. VEML7700, light_sensor_1, etc.)
# Units
#	What unit it measures (e.g. lux, Degrees C)
# Type:
# 	What type of sensor is it (e.g. light sensor, temperature sensor, etc.)
# user_id:
# 	Who is the master? (e.g. admin: user_id=2)
# dataset:
# 	A list of data that this sensor produced.
# 	We are back-referenced by each entry as 'author'
class Sensor(db.Model):
	__tablename__ = 'Sensor'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
	name = db.Column(db.String(20))
	type = db.Column(db.String(20))
	units = db.Column(db.String(20))
	dataset = db.relationship('SensorDataEntry', backref='author', lazy=True) # Sensors can have many entries, but entries can only have 1 creator.
							# lazy argument means that SQLAlchemy will load the data as necessary in 1 go.
							# backref allows us to access the Sensor who created the data entry. I set it to "author" because we probably won't be using it.
							# This relationship will get all Sensor Data Entries based on 1 Sensor.
							# source: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
	def __repr__(self): # how we print this out on the console:
		#return f"{self.name}: {self.type}({self.units}), owned by {self.master.username}, id {self.id}"
		return self.name
#############################################################################################################################
#			SENSOR DATA ENTRY CLASS																							#
#############################################################################################################################

# Every Sensor Data Entry is attached to a Sensor class (i.e. every piece of data has to be produced by a physical sensor)
# Each Sensor Data Entry has a date received by server, and the JSON content it received. 
# Will be processed as necessary by the front-end.

class SensorDataEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True) #the id number of the entry itself.
	date_posted = db.Column(db.DateTime(100), nullable=False, default=datetime.utcnow())  # the date when it came.
	JSON_content = db.Column(JsonEncodedDict) #the actual content.
	sensor_id = db.Column(db.Integer, db.ForeignKey('Sensor.id'),nullable=False) # the id number of the sensor that the data entry came from.
						#Specifies that we have a foreign relationship with a Sensor class.
						#db.ForeignKey references the table name, not the class name. so, we read from the sensors table. 
						
	def __repr__(self): # how do we print this to the console?
		return f"{self.author} at {self.date_posted}: {self.JSON_content}"

#############################################################################################################################
#					ADMIN MODEL VIEWS																						#
#############################################################################################################################

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Sensor, db.session))
admin.add_view(ModelView(SensorDataEntry, db.session))
















#############################################################################################################################
#					TESTING AREA																							#
#############################################################################################################################


class City(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	state = db.Column(db.String(2))
	name = db.Column(db.String(20))
