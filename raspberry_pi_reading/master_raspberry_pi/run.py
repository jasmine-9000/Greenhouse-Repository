#main loop for master raspberry pi:
#parts of code from from https://github.com/sixfab/Sixfab_RPi_CellularIoT_App_Shield/blob/master/sample/basicUDP.py

#imports
from morningstar.morningstar import Morningstar 
from bms.bms import BMS
from gsm.cellulariot import CellularIoT
from gsm.FONA import FONA
from faculty_sensors.sensors import SI7020_A20, BH1745NUC, VEML7700

import time,sys

import json

#methods

def sendJSONdata(phone, file_name,URL=""):
	"""
		phone is a CellularIoT app class.
		
		file name passed in cannot be used by another program. close it first.
		
		server_location is a folder name (where in the server do you want it to go?)
	"""
	#open the file.
	fp = open(file_name, "r")
	#read the only line there. json.dump() only writes 1 line.
	data = fp.readline()
	#try to send it.
	#it needs 1/2 a second to send the data.
	success = phone.sendDataUDP(URL, data)
	time.sleep(0.5)
	return success
	

#global variables
ip_address = '2600:1700:ccd0:37d0:9d6a:dd43:7fd5:d946'
port = 80

slave_rpi_1_address = 'xx:xx:xx:xx:xx'
slave_rpi_2_address = 'xx:xx:xx:xx:xx'

# private server address
private_server_IP_address = "arboretum-backend.soe.ucsc.edu"
private_URL = "http://" + private_server_IP_address

# locations to send data to
BMS_destination = private_URL + "/BMS/post-json"
Tristar_destination = private_URL + "/Tristar/post-json"
Tristar_daily_destination = private_URL + "/Tristar/post-json/daily"
Faculty_destination = private_URL + "/sensors/post-json/admin/<sensor_name>"
Student_destination = private_URL + "/sensors/post-json/<username>/<sensor_name>"

#folders to send JSON falues
ts_daily_values = "tristar_daily_values"
ts_instantaneous_values = "tristar_inst_values"
bms_values = "bms_values"

# this is the init() in an Arduino.
# find the ports on the system your system.
# windows uses virtual COM ports.
# Raspberry Pi uses /dev/USB ports.
# on our raspberry Pi, I will be making use of 3 USB ports on the system.
ports = []
if sys.platform.startswith('win'):
	ports = ['COM%s' % (i+1) for i in range(256)]
elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
	import glob
	ports = glob.glob('/dev/ttyUSB*')
elif sys.platform.startswith('darwin'):
	import glob
	ports = glob.glob('/dev/tty.usbserial*')
else:
	raise EnvironmentError('Error finding ports on your operating system')
	
# class inits(). they automatically create themselves.
# try every port that's activated. in a Raspberry Pi, the glob library tells you which ports are active.
#in windows, there are always 255 ports active for use.
string_1,string_2,bms = "","",""
#for every system we connect to, we try every port until we find it, then remove that port.
for port in ports:
	try:
		#port number, baudrate, MODBUS slave address
		string_1 = Morningstar(port, 9600, 0x1)
		del ports[port]
	except:
		pass
for port in ports:
	try:
		#port number, baudrate, MODBUS slave address
		string_2 = Morningstar(port, 9600,0x1)
		del ports[port]
	except:
		pass
for port in ports:
	try:
		#port number, baudrate
		bms = BMS(port, 57600)
		del ports[port]
	except:
		pass
#FONA is always connected to UART.
#always enable UART on the Raspberry Pi.
fona = CellularIoT(serial_port="/dev/ttyS0", serial_baudrate=115200, board="Sixfab Raspberry Pi Cellular IoT Shield")

#activate the shield
fona.setupGPIO()
fona.disable()
time.sleep(1)
fona.enable()
time.sleep(1)
fona.powerUp()

fona.sendATComm("ATE1", "OK\r\n")

#print out IMEI number , firmware and hardware info

fona.getIMEI()
time.sleep(0.5)
fona.getFirmwareInfo()
time.sleep(0.5)
fona.getHardwareInfo()
time.sleep(0.5)

#where do we want to send it to, and what port are we connecting to?

fona.setIPAddress(ip_address)
time.sleep(0.5)
fona.setPort(port)
time.sleep(0.5)

#set GSM band, CATM1Band, NBIoT band, 
fona.setGSMBand(fona.GSM_900)
time.sleep(0.5)
fona.setCATM1Band(fona.LTE_B5)
time.sleep(0.5)
fona.setNBIoTBand(fona.LTE_B20)
time.sleep(0.5)
fona.getBandConfiguration()
time.sleep(0.5)  
fona.setMode(fona.GSM_MODE)
time.sleep(0.5)

#get network info by asking the operator
fona.connectToOperator()
time.sleep(0.5)
fona.getSignalQuality()
time.sleep(0.5)
fona.getQueryNetworkInfo()
time.sleep(0.5)

#activate context
fona.deactivateContext()
time.sleep(0.5)
fona.activateContext()
time.sleep(0.5)

#start UDP service
fona.closeConnection()
time.sleep(0.5)
fona.startUDPService()
time.sleep(0.5)

#initialize water, light, and temperature sensors.

water = SI7020_A20()
light = VEML7700()
temperature = BH1745NUC()

# import bluetooth

# bluetooth_port = 1
# server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# server_sock.bind(("",bluetooth_port))
# server_sock.listen(1)

# client_sock,address = server_sock.accept()

# data  


# this is the loop in an arduino
while 1:
	#at 11:58pm of every day, read the daily values, and send it to a different area than the rest of the data.
	time_now = time.localtime()
	month = time_now.tm_mon
	year = time_now.tm_year
	day = time_now.tm_mday
	hr = time_now.tm_hour
	min = time_now.tm_min 
	
	#file names
	string_1_JSON_name  = f'tristar_1_{month}-{day}_{hour}-{min}.json'
	string_2_JSON_name  = f'tristar_2_{month}-{day}_{hour}-{min}.json'
	BMS_JSON_name 		= f'bms_{month}-{day}-{year}.json'
	TS_JSON_name 		= f'ts_{month}-{day}-{year}.json'
	water_JSON_name 	= 'water.json'
	light_JSON_name		= 'light.json'
	temp_JSON_name 		= 'temp.json'
	water_destination   = Faculty_destination.replace('<sensor_name>', 'SI7020_A20')
	light_destination 	= Faculty_destination.replace('<sensor_name>', 'VEML7700')
	temp_destination 	= Faculty_destination.replace('<sensor_name>', 'BH1745NUC')
	
	#file pointers
	string_1_JSON_fp = open(string_1_JSON_name, "w")
	string_2_JSON_fp = open(string_2_JSON_name, "w")
	BMS_JSON_fp = open(BMS_JSON_name, "w")
	water_fp = open(water_JSON_name, "w")
	light_JSON_fp = open(light_JSON_name, "w")
	temp_JSON_fp = open(temp_JSON_name, "w")
	
	# every day, ask for Daily file.
	if hr == 23 and min == 58: #23:58 is 11:58pm in international time.
		#create a unique name for the JSON file of that day.
		string_1_name = f'tristar_string_1_daily_{month}_{day}_{year}.json'
		string_2_name = f'tristar_string_2_daily_{month}_{day}_{year}.json'
		
		#create the file, 
		s1_fp = open(string_1_name, "w+")
		s2_fp = open(string_2_name, "w+")
		
		#reads the daily values, then dumps it to our uniquely named JSON file
		string_1.DumpDailyDataToJSONFile(s1_fp)
		string_2.DumpDailyDataToJSONFile(s2_fp)
		
		#close the file pointer, so we can send the data.
		s1_fp.close()
		s2_fp.close()
		
		#send the data.
		sendJSONdata(fona, string_1_name, Tristar_daily_destination)
		sendJSONdata(fona, string_2_name, Tristar_daily_destination)
		
	#dump all the instantaneous data to an external file.
	string_1.DumpInstantenousDataToJSONFile(string_1_JSON_fp)
	string_2.DumpInstantenousDataToJSONFile(string_2_JSON_fp)
	BMS.DumpToJSONfile(BMS_JSON_fp)
	json.dump(water.read_data(), water_JSON_fp)
	json.dump(light.read_data(), light_JSON_fp)
	json.dump(temp.read_data(), temp_JSON_fp)
	

	#close file pointers in preparation for sending to database.
	string_1_JSON_fp.close()
	string_2_JSON_fp.close()
	BMS_JSON_fp.close()
	water_JSON_fp.close()
	light_JSON_fp.close()
	temp_JSON_fp.close()
	
	#send JSON files to database.
	sendJSONdata(fona, string_1_JSON_name, Tristar_destination)
	sendJSONdata(fona, string_2_JSON_name, Tristar_destination)
	sendJSONdata(fona, BMS_JSON_name, BMS_destination)
	sendJSONdata(fona, water_JSON_name, water_destination)
	sendJSONdata(fona, light_JSON_name, light_destination)
	sendJSONdata(fona, temp_JSON_name, temp_destination)
	
	#end of while loop. repeat again.
