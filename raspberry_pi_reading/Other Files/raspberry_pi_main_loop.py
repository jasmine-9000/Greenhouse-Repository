#Hello, and welcome to the main source code for the raspberry pi.
#This will execute upon powering the Raspberry Pi.
#I will need to configure my Raspberry Pi to do this, though.



#imports:
import asyncio
import morningstar_async
import bms_async
import slave_r_pi_async
import FONA	

from MorningStar_v3 import Morningstar
from BMS_v1 import BMS
	
async def greenhouse_data_collection():
	tristar_data = loop.create_task(morningstar_async.read_data())
	bms_data = loop.create_task(bms_async.read_data())
	slave_raspberry_pi_data = loop.create_task(slave_r_pi_async.read_data())
	await asyncio.wait([tristar_data,bms_data,slave_raspberry_pi_data])
	return tristar_data,bms_data,slave_raspberry_pi_data
	
def main():
	pv_string_1 = Morningstar("COM3", 9600,1)
	pv_string_2 = Morningstar("COM4", 9600,1)
	battery_pack = BMS("COM5", 57600)
	r_pi_slave = Raspberry_PI()
	fona = FONA("COM6")
	
	while 1:
		#tristar, bms, and slave raspberry pi data must be harvested before being sent.
		tristar,bms,r_pi = run_until_complete(greenhouse_data_collection())
		#send the data through the FONA library.
		FONA.send(tristar.result(),bms.result(),r_pi.result())
		
		#see if the FONA is being sent any data. if so, parse the data.
		incoming = FONA.receive()
		if incoming:
			if hasattr(incoming, 'sensorscript'):
				incoming.sensorscript.
		