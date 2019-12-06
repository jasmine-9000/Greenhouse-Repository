#!/usr/bin/python
#https://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi
#http://tightdev.net/SpiDev_Doc.pdf

#add the following line to /boot/config.txt:
#dtoverlay=w1-gpio
#there is only 1 1-wire sensor we really need: a temperature sensor.
#there are no others.
#connect the DQ line to GPIO 4.
import os
import time

import spidev
#enable SPI on the raspberry pi configuration settings.

from smbus2 import SMBus
# enable I2C on the raspberry pi configuration settings.
import onewire
import serial

import bluetooth


class i2c:
	def __init__(self, DEVICE_ADDRESS, DEVICE_REG_MODE1=0x00,DEVICE_REG_LEDOUT0=0x1d):
		self.address = DEVICE_ADDRESS
		self.reg_mode = DEVICE_REG_MODE1
		self.ledout = DEVICE_REG_LEDOUT0
	def read_data(self,number_of_bytes,offset):
		block = i2c_smbus_read_block_data(self.address, offset, number_of_bytes)
		return block

class one_wire:
	def __init__(self,serial_number='28-000005e2fdc3'):
		#load our 1-wire drivers.
		os.system('modprobe w1-gpio')
		os.system('modprobe w1-therm')
		#define our sensor's output file.
		self.temp_sensor = 'sys/bus/w1/devices/'+str(serial_number)+'/w1_slave'
	def data_raw():
		f = open(temp_sensor, 'r')
		lines = f.readlines()
		f.close()
		return lines
	def read_temp():
		lines = data_raw()
		while lines[0].strip()[-3] != 'YES':
			time.sleep(0.2)
			lines = data_raw()
		temp_output = lines[1].find('t=')
		if temp_output != -1:
			temp_string = lines[1].strip()[temp_output+2:]
			temp_c = float(temp_string) / 1000.0
			temp_f = temp_c * 9.0 / 5.0 + 32.0
			return temp_c
		else:
			return 0
class UART:
	def __init__(self, port, baudrate,bytesize=8,parity='N',stopbits=1,timeout=100,xonxoff=False, rtscts=False,dsrdtr=False,write_timeout=100,inter_byte_timeout=100,exclusive):
		self.ser = serial.Serial(port,baudrate,bytesize,parity,stopbits,timeout,rtscts,dsrdtr,write_timeout)
	def read_data(self,encoding='ascii'):
		response = self.ser.readline()
		data = response.decode(encoding)
		return data
class SPI:
	def __init__(self,port=0,device=1):
		self.spi = spidev.SpiDev()
		self.spi.open(port,device)
	def read_bytes(self,len):
		data = self.spi.read(len):
		return data
	def write_bytes(self,values):
		self.spi.write(values)

class SLAVE:
	def __init__(self):
		pass
	def start_server(self):
		self.server_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
		self.server_sock.bind(("",0x1001))
		self.server_sock.listen(1)
# ---   network events
	def incoming_connection(self, source, condition):
		sock, info = self.server_sock.accept()
		address, psm = info
		
		print("Accepted connection from %s" % str(address))
		
		self.peers[address] = sock
		self.addresses[sock] = address
		
		self.sources[address] = source
		return True
	def data_ready(self,sock,condition):
		address = self.addresses[sock]
		data = sock.recv(1024)
	
		if len(data) == 0:
			print("Lost connection with %s" % address )
			del self.sources[address]
			del self.peers[address]
			del self.addresses[sock]
			sock.close()
		else:
			print(self.data)
		return True
		
if __name__ == "__main__":
	temp_sensor_1 = one_wire('28-000005e2fdc3')
	temp_data = temp_sensor_1.read_temp()
	
	light_sensor = i2c(address=0x1B, 0,0x1d)
	light_data = light_sensor.read_data(0x00,1)
	
	master_bluetooth_address = "xx:xx:xx:xx:xx:xx"
	port = 1
	sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	sock.connect((master_bluetooth_address,port))
	
	sock.send(str(light_data))
	sock.send(str(temp_sensor_1.read_data()))
	
	sock.close()