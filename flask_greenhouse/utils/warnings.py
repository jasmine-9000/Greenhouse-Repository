#########################################################################
#			WARNINGS													#
#########################################################################
import json 
from flask import flash

#########################################################################
#			WARNINGS													#
#########################################################################
# open a file, process it, then flash the warnings.
# all arguments are filepaths.
def flash_ts_warnings(ts_filepath):
	alarms_message = None
	faults_message = None
	with open(ts_filepath, "r") as fp:
		data = json.load(fp)
		faults = data["Status"]["faults"]
		alarms = data["Status"]["alarms"]
		print("Tristar Faults and alarms detected: ", faults, alarms)
		if faults: faults_message = "Tristar Faults: " + faults
		if alarms: alarms_message = "Tristar Alarms: " + alarms
	if alarms_message:
		flash(alarms_message, 'warning')
	if faults_message:
		flash(faults_message, 'danger')

def flash_bms_warnings(bms_filepath):
	status_message = None 
	protection_message = None
	power_message = None
	with open(bms_filepath, "r") as fp:
		data = json.load(fp)
		# retrive all error sentences. If they're Null, ignore them.
		MainStatus = data["BMS Status"]
		StatusErrors = MainStatus["Status Errors"]
		ProtectionErrors = MainStatus["Protection Errors"]
		PowerErrors = MainStatus["Power Errors"]
		if StatusErrors: status_message = "BMS ERROR: " + StatusErrors
		if ProtectionErrors: protection_message = "BMS ERROR: " + ProtectionErrors
		if PowerErrors: power_message = "BMS ERROR: " + PowerErrors
	if status_message:	
		flash(status_message, 'warning')
	if power_message:
		flash(power_message, 'danger')
	if protection_message:
		flash(protection_message, 'danger')
			