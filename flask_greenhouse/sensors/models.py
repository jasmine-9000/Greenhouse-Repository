# imports.
from flask_greenhouse import db
from datetime import datetime
import json

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

# This is a Sensor Class.
# If it's a faculty sensor, owner="Admin"
# if it's a student sensor, owner="<name of student>"
# Name is the name of the sensor (e.g. VEML7700, light_sensor_1, etc.)
# units is the name of the unit it measures.
class Sensor(db.Model):
	__tablename__ = 'sensors'
	id = db.Column(db.Integer, primary_key=True)
	owner = db.Column(db.String(20))
	name = db.Column(db.String(20))
	type = db.Column(db.String(20))
	units = db.Column(db.String(20))
	dataset = db.relationship('SensorDataEntry', backref='author', lazy=True) # Sensors can have many entries, but entries can only have 1 creator.
							# lazy argument means that SQLAlchemy will load the data as necessary in 1 go.
							# backref allows us to access the Sensor who created the data entry. I set it to "author" because we probably won't be using it.
							# This relationship will get all Sensor Data Entries based on 1 Sensor.
							
	def __repr__(self): # how we print this out on the console:
		return f"{self.name}: {self.type}({self.units}), owned by {self.owner}, id {self.id}"

# this is a Sensor Data Entry Class.
# Every Sensor Data Entry is attached to a Sensor class (i.e. every piece of data has to be produced by a physical sensor)
# Each Sensor Data Entry has a date received by server, and the JSON content it received. 
# we can process it as necessary.
class SensorDataEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True) #the id number of the entry itself.
	date_posted = db.Column(db.DateTime(100), nullable=False, default=datetime.utcnow())  # the date when it came.
	JSON_content = db.Column(JsonEncodedDict) #the actual content.
	sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'),nullable=False) # the id number of the sensor that the data entry came from.
						#Specifies that we have a foreign relationship with a Sensor class.
						#db.ForeignKey references the table name, not the class name. so, we read from the sensors table. 
						
	def __repr__(self): # how do we print this to the console?
		return f"{self.author} at {self.date_posted}: {self.JSON_content}"

#test class.
class City(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	state = db.Column(db.String(2))
	name = db.Column(db.String(20))
