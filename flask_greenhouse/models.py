#########################################################################################################################
#							IMPORTS																						#
#########################################################################################################################

from flask_greenhouse import db, admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
import json

#########################################################################################################################
#							CLASS TEMPLATES																				#
#########################################################################################################################

# this class enables JSON storage.
# it inherits the TypeDecorator class, so we need to redefine process_bind_param and process_result_value.
# It needs to save to a SQLlite database as a string. We can pass in a dictionary, and it will convert to string.
# When we load the value, it will automatically convert it back to dictionary format with json.loads().

class JsonEncodedDict(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
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

# inheritable class for BMS data, Tristar data, Sensor Data, etc.
class JSONDataEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True) # a unique ID for our JSON data entry. Every object must have one. It's unique, and it's the primary way the database sorts our JSON data.
	date_posted = db.Column(db.DateTime(100), nullable=False, default=datetime.utcnow()) # we will keep track of when we received each piece of data. If the method does not have a way of retrieving a date, the default is today.
	JSON_content = db.Column(JsonEncodedDict)
	def __repr__(self):
		return f"JSONDataEntry('Data Entry #{self.id}', '{self.JSON_content}', 'Date Posted: {self.date_posted}')"

#########################################################################################################################
#							ACTUAL ENTRIES																				#
#########################################################################################################################

# same as JSONDataEntry, but tablename is different for every one.

class BMSDataentry(JSONDataEntry):
	__tablename__ = 'BMS Data'
	
class TristarDataEntry(JSONDataEntry):
	__tablename__ = 'Tristar Data'

class TristarDailyDataEntry(JSONDataEntry):
	__tablename__ = 'Tristar Daily Data'
	
	
#############################################################################################################################
#									ADMIN MODEL VIEWS																		#
#############################################################################################################################
admin.add_view(ModelView(BMSDataentry, db.session))
admin.add_view(ModelView(TristarDataEntry, db.session))
admin.add_view(ModelView(TristarDailyDataEntry, db.session))

#############################################################################################################################
#									SOURCES																					#
#############################################################################################################################

# source: https://www.michaelcho.me/article/json-field-type-in-sqlalchemy-flask-python