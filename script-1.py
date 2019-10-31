from datetime import datetime, timedelta
from flask_greenhouse import db
from flask_greenhouse.models import BMSDataentry
import json

charge = 0.0
place = 0

all_entries = BMSDataentry.query.all()

for entry in all_entries:
	#json_received = entry.JSON_content
	#json_received["Battery Charge"]["battery charge"] = charge
	#entry.JSON_content
	entry.JSON_content["Battery Charge"]["battery charge"] = charge
	charge += 0.1
	db.session.commit()


	
	