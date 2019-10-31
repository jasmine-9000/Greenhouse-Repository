from datetime import datetime, timedelta
from flask_greenhouse import db
from flask_greenhouse.models import BMSDataentry
import json
today = datetime.now()
current_time = today
step = timedelta(minutes = 10)
tomorrow = today + timedelta(days = 1)

charge = 0.0
step = 0.05
while current_time < tomorrow:
	file = open("flask_greenhouse/BMS_test_file.json")
	# json_received = file.readlines()
	bms = json.load(file)
	#dumped = json.dumps(json_received)
	#dumped = dumped.replace('\n', '')
	#dumped = dumped.replace('\\n', '')
	#dumped = dumped.replace('\t', '')
	#dumped = dumped.replace('\\t', '')
	#dumped = dumped.replace('\\', '')
	bms["Battery Charge"]["battery charge"] = charge
	new_data = BMSDataentry(date_posted=current_time, JSON_content=bms)
	db.session.add(new_data)
	db.session.commit()
	file.close()
	charge += step
	current_time = current_time + step
	
	