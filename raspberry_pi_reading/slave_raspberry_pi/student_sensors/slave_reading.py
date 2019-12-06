import bluetooth
from bluetooth.ble import DiscoveryService

import json

class slave:
	def __init__(self,name,uuid,sensor_list=None):
		self.name = name
		self.uuid = uuid
		sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
		sock.connect((uuid,port))

		service = DiscoveryService()
		devices = service.discover(2)
		if (uuid, name) in devices.items():	
			self.
		else:
			print("Something went wrong.")
		self.sensor_list = sensor_list
	
	def retrieveData(self):
		self.name = name
		 
	def DumpToJSON_File(self,JSON_File_Pointer):	
		data = self.retrieveData()
		json.dump(data, JSON_File_Pointer)
		
if __name__ == "__main__":	
	#testing grounds
	temperatureReader = slave('PI_1','1234',["water_temp","air_temp"])
	fp = open("x.json","rw")
	slave.DumpToJSON_File(fp)
	