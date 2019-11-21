from flask import render_template, request, Blueprint
from flask_greenhouse.forms import Date_Form

import json
tristar = Blueprint("tristar", __name__)



@tristar.route("/Tristar", methods=["POST", "GET"])
def Tristar():
	form = Date_Form()
	return render_template('Tristar.html', title="Tristar Data", form=form)

# navigate to http://<hostname>/Tristar/ChargeSettings to view current charge settings.
# there will be a link in http://<hostname>/Tristar to this page.



@tristar.route("/Tristar/ChargeSettings", methods=["GET"])
def ViewChargeSettings():
	#right now, just load test data.
	filepath = "flask_greenhouse/Tristar_daily_test_file.json"
	with open(filepath, "r") as fp:
		data = json.load(fp)
		charge_settings = data['Charge Settings']
	
	return render_template('charge_settings.html', title="Charge Settings", charge_settings=charge_settings)




@tristar.route("/Tristar/DailyValues", methods=["GET"])
def ViewDailyValues():
	filepath = "flask_greenhouse/Tristar_daily_test_file.json"
	with open(filepath, "r") as fp:
		data = json.load(fp)
		daily_values = data['Daily Logger Values']
	return render_template('todays_values.html', title="Charge Settings", daily_values=daily_values)

@tristar.route("/Tristar/Instantaneous", methods=["GET"])
def ViewInstantaneous():
	filepath = "flask_greenhouse/Tristar_instantaneous_test_file.json"
	with open(filepath, "r") as fp:
		data = json.load(fp)
	return render_template('instantaneous_values.html', title="Tristar Values Now", data=data)



#post BMS JSON data to this address.
@tristar.route("/Tristar/post-json", methods=["POST"]) #get requests will be blocked.
def Tristar_Post():
	req_data = request.get_json()
	new_Tristar_entry = TristarDataentry(JSON_data=req_data)
	db.session.add(new_Tristar_entry)
	db.session.commit()
	# this is a comment for git
	# this is another comment
	return "your data has been received."