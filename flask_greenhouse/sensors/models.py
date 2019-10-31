
from flask_greenhouse import db
from datetime import datetime
import json


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

class City(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	state = db.Column(db.String(2))
	name = db.Column(db.String(20))
	
class Sensor(db.Model):
	__tablename__ = 'sensors'
	id = db.Column(db.Integer, primary_key=True)
	owner = db.Column(db.String(20))
	name = db.Column(db.String(20))
	units = db.Column(db.String(20))

class SensorDataEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True) #the id number of the entry itself.
	date_posted = db.Column(db.DateTime(100), nullable=False, default=datetime.utcnow())  # the date when it came.
	JSON_content = db.Column(JsonEncodedDict) #the actual content.
	sensor_id = db.Column(db.Integer, db.ForeignKey('Sensor.id'),nullable=False) # the id number of the sensor that the data entry came from.
