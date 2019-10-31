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

class JSONDataEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True) # a unique ID for our JSON data entry. Every object must have one. It's unique, and it's the primary way the database sorts our JSON data.
	date_posted = db.Column(db.DateTime(100), nullable=False, default=datetime.utcnow()) # we will keep track of when we received each piece of data. If the method does not have a way of retrieving a date, the default is today.
	JSON_content = db.Column(JsonEncodedDict)
	def __repr__(self):
		return f"JSONDataEntry('Data Entry #{self.id}', '{self.JSON_content}', 'Date Posted: {self.date_posted}')"
	
	
class BMSDataentry(JSONDataEntry):
	__tablename__ = 'BMS Data'
	
class TristarDataEntry(JSONDataEntry):
	__tablename__ = 'Tristar Data'

class SensorDataEntry(JSONDataEntry):
	__tablename__ = 'Sensor Data'
	