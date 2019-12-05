#########################################################################################################################
#							IMPORTS																						#
#########################################################################################################################
from flask import render_template, request, Blueprint, jsonify
from flask_greenhouse import db
from flask_greenhouse.forms import Tristar_Form
from flask_greenhouse.models import TristarDataEntry, TristarDailyDataEntry
from datetime import datetime, timedelta
import json
tristar = Blueprint("tristar", __name__)

#########################################################################################################################
#							MAIN TRISTAR GRAPHING ROUTE																	#
#########################################################################################################################

@tristar.route("/Tristar", methods=["POST", "GET"])
@tristar.route("/tristar", methods=["POST", "GET"])
def Tristar():
	form = Tristar_Form()
	return render_template('Tristar.html', title="Tristar Data", form=form)


#########################################################################################################################
#							FILE VIEWING ROUTES																			#
#########################################################################################################################
# navigate to http://<hostname>/Tristar/ChargeSettings to view current charge settings.
# there will be a link in http://<hostname>/Tristar to this page.
@tristar.route("/Tristar/ChargeSettings", methods=["GET"])
def ViewChargeSettings():
	#right now, just load test data.
	filepath = "flask_greenhouse/Tristar_test_file.json"
	with open(filepath, "r") as fp:
		data = json.load(fp)
		charge_settings = data['Charge Settings']
	
	return render_template('charge_settings.html', title="Charge Settings", charge_settings=charge_settings)
@tristar.route("/Tristar/DailyValues", methods=["GET"])
def ViewDailyValues():
	filepath = "flask_greenhouse/Tristar_daily_file.json"
	with open(filepath, "r") as fp:
		data = json.load(fp)
		daily_values = data['Daily Logger Values']
	return render_template('todays_values.html', title="Charge Settings", daily_values=daily_values)

@tristar.route("/Tristar/Instantaneous", methods=["GET"])
def ViewInstantaneous():
	filepath = "flask_greenhouse/Tristar_instantaneous_file.json"
	with open(filepath, "r") as fp:
		data = json.load(fp)
	return render_template('instantaneous_values.html', title="Tristar Values Now", data=data)


#########################################################################################################################
#							POST ROUTES																				#
#########################################################################################################################

# post Instantaneous  JSON data to this address:
# http://<hostname>/Tristar/post-json
@tristar.route("/Tristar/post-json", methods=["POST"]) #get requests will be blocked.
def Tristar_Post():
	try:
		req_data = request.get_json()
		new_Tristar_entry = TristarDataEntry(JSON_content=req_data)
		# write latest data to Tristar_Instantaneous_File.json
		# overwrite previous file at that location.
		# use json.dump()
		with open("flask_greenhouse/Tristar_instantaneous_file.json", "w") as fp:
			json.dump(req_data, fp)
		db.session.add(new_Tristar_entry)
		db.session.commit()
		return "your data has been received."
	except IOError:
		return "Internal server error", 500
	except Exception:
		# return a 500 error
		return "Data could not be processed.", 500
		
# post Daily JSON data to this address:
# http://<hostname>/Tristar/post-json/daily
@tristar.route("/Tristar/post-json/daily", methods=["POST"])
def Tristar_Daily_Post():
	try:
		req_data = request.get_json()
		new_Tristar_entry = TristarDailyDataEntry(JSON_content=req_data)
		db.session.add(new_Tristar_entry)
		db.session.commit()
		return "your data has been received."
	except:
		return "data could not be processed."
		
		
#########################################################################################################################
#							DATA RETRIEVAL METHODS																		#
#########################################################################################################################		
		
@tristar.route("/Tristar/api/single_data_point/<string:date>/<string:parameter>", methods=["GET"])
def Tristar_data_retrieval(date, parameter):
	"""
		Returns a single data point.
		
		Arguments:
			date: what date do you want to request?
			parameter: what parameter do you want?
		Returns:
			A JSON file. 
			Example:
			{
				"x": 1,
				"date": "2019-10-31 10:30:30",
				"parameter": "battery charge"
			}
		
	"""
	# parse the input datestring. strptime() should do the trick.
	datetime_from_JS = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
	Table = None
	buffer = None
	if parameter in ["Battery Voltage Minimum Daily",
						"Battery Voltage Maximum Daily",
						"Input Voltage Maximum Daily",
						"Amp Hours accumulated daily",
						"Watt Hours accumulated daily",
						"Maximum power output daily",
						"Minimum temperature daily",
						"Minimum temperature daily",
						"time_ab_daily",
						"time_eq_daily",
						"time_fl_daily"]:
		Table = TristarDailyDataEntry
		buffer = timedelta(hours=11)
	else:
		Table = TristarDataEntry
		buffer = timedelta(minutes=10)
	# Search for BMS entries with a buffer of 30 seconds.
	entry = Table.query \
			.filter( Table.date_posted \
				.between(datetime_from_JS - buffer, 
						 datetime_from_JS + buffer))\
				.first_or_404()
	# extract final entry date, JSON dictionary, and value. 
	final_entry_date = entry.date_posted
	dict = entry.JSON_content
	value = None
	try:
		value = dictionary_translator(dict, parameter)
	except:
		parameter = "error"
		value = None
	JSON_response = {
		
		"date": final_entry_date.strftime("%Y-%m-%d %H:%M:%S"),
		"parameter": parameter,
		"value": value
	}

	return jsonify(JSON_response)
@tristar.route("/Tristar/api/<string:start_date>/<string:end_date>/<int:interval>/<string:parameter>", methods=["GET"])
def Tristar_multi_data_retrieval(start_date, end_date, interval, parameter):
	"""
		A server-side multi-data-point retrieval system.
		Arguments:
			start_date, end_date: from what date to what date do you want your points?
			interval (in minutes).
			parameter: what parameter do you want JSON data from?
		Returns:
			A JSON file.
			Example:
			{
				"parameter": "Battery Charge",
				"data": {
					"2019-10-31 10:30:44": 1,
					"2019-10-31 10:40:44": 2,
					"2019-10-31 10:50:44": 3,
					"2019-10-31 11:00:44": 4,
					"2019-10-31 11:10:44": 5,
					"2019-10-31 11:20:44": 5,
					"2019-10-31 11:30:44": 6
				}
			}
	"""
	# extrapolate dates from start, end, and interval.
	s = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
	e = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
	dates = []
	while(s < e):
		dates.append(s)
		s = s + timedelta(minutes=interval)
	
	# retrieve data from database based on date for all dates.
	data = {}
	Table = None
	buffer = None
	# choose which table to query. If we're requesting daily values, then choose the daily table.
	# otherwise, use the regular table. 
	if parameter in ["Battery Voltage Minimum Daily",
						"Battery Voltage Maximum Daily",
						"Input Voltage Maximum Daily",
						"Amp Hours accumulated daily",
						"Watt Hours accumulated daily",
						"Maximum power output daily",
						"Minimum temperature daily",
						"Minimum temperature daily",
						"time_ab_daily",
						"time_eq_daily",
						"time_fl_daily"]:
		Table = TristarDailyDataEntry
		buffer = timedelta(hours=11)
	else:
		Table = TristarDataEntry
		buffer = timedelta(minutes=10)
	for date in dates:
		value = None
		entry = Table.query \
			.filter( Table.date_posted \
				.between(date - buffer, 
						 date + buffer))\
				.first()
		# once the entry is retrieved, (if there's an entry), extract the JSON content, 
		# try to find the parameter using dictionary translation, then if it's found, add it to the dataset.
		try:
			dict = entry.JSON_content
			value = dictionary_translator(dict, parameter)
			data[date.strftime("%Y-%m-%d %H:%M:%S")] = value
		except:
			pass
	# construct JSON response. 
	JSON_response = {
		"parameter": parameter,
		"data": data
	}
	return jsonify(JSON_response)


def dictionary_translator(dict, parameter):
	print(dict, parameter)
	# ADC data
	if parameter == 'bat_voltage':
		return dict["ADC_data"]["Battery Voltage"]
	elif parameter == 'bat_terminal_voltage':
		return dict["ADC_data"]["battery terminal voltage"]
	elif parameter == 'bat_sense_voltage':
		return dict["ADC_data"]["battery sense voltage"]
	elif parameter == 'array_voltage':
		return dict["ADC_data"]["array voltage"]
	elif parameter == 'bat_current':
		return dict["ADC_data"]["battery current"]
	elif parameter == 'array_current':
		return dict["ADC_data"]["array current"]
	elif parameter == '12V_supply':
		return dict["ADC_data"]["12V supply"]
	elif parameter == '3V_supply':
		return dict["ADC_data"]["3V supply"]
	elif parameter == 'meterbus_voltage':
		return dict["ADC_data"]["meterbus voltage"]
	elif parameter == '1_8V_supply':
		return dict["ADC_data"]["1.8V supply"]
	elif parameter == 'v_ref':
		return dict["ADC_data"]["reference voltage"]
				
				# Temperature readings
	elif parameter == "temp_h":
		return dict["Temperature data"]["heatsink temperature"]
	elif parameter == "temp_rts":
		return dict["Temperature data"]["RTS temperature"]
	elif parameter == "temp_bat_reg":
		return dict["Temperature data"]["battery regulation temperature"]
				
				#status
	elif parameter == "charging_current":
		return dict["Status"]["charging_current"]
	elif parameter == "min_bat_voltage":
		return dict["Status"]["minimum battery voltage"]
	elif parameter == "max_bat_voltage":
		return dict["Status"]["maximum battery voltage"]
				
				#Charger Data
	elif parameter == "ah_resettable":
		return dict["Charger Data"]["Ah Charge Resettable"]
	elif parameter == "ah_total":
		return dict["Charger Data"]["Ah Charge Total"]
	elif parameter == "kwhr_resettable":
		return dict["Charger Data"]["kWhr Charge Resettable"]
	elif parameter == "kwhr_total":
		return dict["Charger Data"]["kWhr Charge Total"],
				
				#MPPT data
	elif parameter == "p_out":
		return dict["MPPT Data"]["output power"]
	elif parameter == "p_in":
		return dict["MPPT Data"]["input power"]
	elif parameter == "V_max_power":
		return dict["MPPT Data"]["max power of last sweep"]
	elif parameter == "V_mp":
		return dict["MPPT Data"]["Vmp of last sweep"]
	elif parameter == "V_oc":
		return dict["MPPT Data"]["Voc of last sweep"]
				
				#Daily Logger Values
	elif parameter == "bat_min_voltage_daily":
		return dict["Daily Logger Values"]["Battery Voltage Minimum Daily"]
	elif parameter == "bat_max_voltage_daily":
		return dict["Daily Logger Values"]["Battery Voltage Maximum Daily"]
	elif parameter == "input_voltage_max_daily":
		return dict["Daily Logger Values"]["Input Voltage Maximum Daily"]
	elif parameter == "Ah_daily":
		return dict["Daily Logger Values"]["Amp Hours accumulated daily"]
	elif parameter == "Wh_daily":
		return dict["Daily Logger Values"]["Watt Hours accumulated daily"]
	elif parameter == "P_max_daily":
		return dict["Daily Logger Values"]["Maximum power output daily"]
	elif parameter == "min_temp_daily":
		return dict["Daily Logger Values"]["Minimum temperature daily"]
	elif parameter == "max_temp_daily":
		return dict["Daily Logger Values"]["Minimum temperature daily"]
	elif parameter == "time_ab_daily":
		return dict["Daily Logger Values"]["time_ab_daily"]
	elif parameter == "time_eq_daily":
		return dict["Daily Logger Values"]["time_eq_daily"]
	elif parameter == "time_fl_daily":
		return dict["Daily Logger Values"]["time_fl_daily"]
	else:
		print("lame")
		return None

	
	