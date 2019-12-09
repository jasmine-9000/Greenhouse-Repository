import smbus
import time

# from micropython import const
# import adafruit_bus_device.i2c_device as i2cdevice
# from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
# from adafruit_register.i2c_bits import RWBits
# from adafruit_register.i2c_bit import RWBit, ROBit




bus = smbus.SMBus(1)
		
class SI7020_A20:
	""" 
	datasheet: https://www.silabs.com/documents/public/data-sheets/Si7020-A20.pdf
	code source: https://github.com/ControlEverythingCommunity/SI7020-A20/blob/master/python/SI7020_A20.py
	this is a temperature and humidity sensor. 
	Methods:
	
	def read_data().
		Arguments: None
		Returns: (Temperature in Celsius, Relative Humidity) in dictionary format
	"""
	def __init__(self):
		slave_address = 0x40
		return
	def read_data(self):  
		# SI7020_A20 address, 0x40(64)
		# 0xF5(245)	Select Relative Humidity NO HOLD MASTER mode
		bus.write_byte(0x40, 0xF5) 
		time.sleep(0.5)
		# SI7020_A20 address, 0x40(64)
		# Read data back, 2 bytes, Humidity MSB first
		data0 = bus.read_byte(0x40)
		data1 = bus.read_byte(0x40)
		# convert the data
		humidity = (125.0 * (data0 * 256.0 + data1) / 65536.0) - 6.0
		# SI7020_A20 address, 0x40(64) 
		# 0xF3(243)	Select temperature NO HOLD MASTER mode
		bus.write_byte(0x40, 0xF3)
		time.sleep(0.5)
		# SI7020_A20 address, 0x40(64)
		# Read data back, 2 bytes, Temperature MSB first
		data0 = bus.read_byte(0x40)
		data1 = bus.read_byte(0x40)
		# Convert the data
		cTemp = (175.72 * (data0 * 256.0 + data1) / 65536.0) - 46.85
		return {"temperature": {"value": cTemp, "units": "C"}, "humidity": {"value": humidity, "units": "% RH"} }
class BH1745NUC:
	"""
	This is a light value.
	Methods:
	read_data()
		Arguments: None
		Returns: (red light value, green light value, blue light value, clear light value)
	datasheet: https://www.mouser.co.uk/datasheet/2/348/bh1745nuc-e-519994.pdf
	code source:https://github.com/ControlEverythingCommunity/BH1745NUC/blob/master/Python/BH1745NUC.py
	"""
	addr = 0x38
	def __init__(self):
		return
	def read_data(self):
		# BH1745NUC address, 0x38(56)
		# Select mode control register1, 0x41(65)
		#	0x00(00)	RGBC measurement time = 160 ms
		bus.write_byte_data(self.addr, 0x41, 0x00)
		# BH1745NUC address, 0x38(56)
		# Select mode control register2, 0x42(66)
		#	0x90(144)	RGBC measurement active, Gain = 1X
		bus.write_byte_data(self.addr, 0x42, 0x90)
		# BH1745NUC address, 0x38(56)
		# Select mode control register3, 0x44(68)
		#		0x02(02)	Default value
		bus.write_byte_data(self.addr, 0x44, 0x02)

		time.sleep(0.5)

		# BH1745NUC address 0x38(56)
		# Read data back from 0x50(80), 8 bytes
		# Red LSB, Red MSB, Green LSB, Green MSB, Blue LSB, Blue MSB
		# cData LSB, cData MSB 
		data = bus.read_i2c_block_data(self.addr, 0x50, 8)

		# Convert the data
		red = data[1] * 256 + data[0]
		green = data[3] * 256 + data[2]
		blue = data[5] * 256 + data[4]
		cData = data[7] * 256 + data[6]

		#return red, green, blue, cData
		return {"red_light": {"value": red, "unit": "lux"},
				"green_light": {"value": green, "unit": "lux"},
				"blue_light": {"value": blue, "unit": "lux"},
				"clear_light": {"value": cData, "unit": "lux"}
				}
				


class VEML7700:
	"""
	datasheet:
	code source: https://www.raspberrypi.org/forums/viewtopic.php?t=198082
	
	methods:
	
	get_data()
		Arguments: None
		Returns: IR light, light ( in dictionary form )
	"""
	addr = 0x10
	#Write registers
	als_conf_0 = 0x00
	als_WH = 0x01
	als_WL = 0x02
	pow_sav = 0x03

	#Read registers
	als = 0x04
	white = 0x05
	interrupt = 0x06


	# These settings will provide the range for the sensor: (0 - 15099 lx)
	#
	# LSB MSB
	confValues = [0x00, 0x18] # 1/4 gain, 100ms IT (Integration Time)


	#Reference data sheet Table 1 for configuration settings
	#MSB = 00011000 = 18 in hexadecimal ( als gain = 1/4, bits 12:11 = 11 )
	#LSB = 00000000 = 00 ( integration time = 100ms, bits 9:6 = 0000 )

	interrupt_high = [0x00, 0x00] # Clear values
	#Reference data sheet Table 2 for High Threshold

	interrupt_low = [0x00, 0x00] # Clear values
	#Reference data sheet Table 3 for Low Threshold

	power_save_mode = [0x00, 0x00] # Clear values
	#Reference data sheet Table 4 for Power Saving Modes
	def __init__(self):
		bus.write_i2c_block_data(self.addr, self.als_conf_0, self.confValues)
		bus.write_i2c_block_data(self.addr, self.als_WH, self.interrupt_high)
		bus.write_i2c_block_data(self.addr, self.als_WL, self.interrupt_low)
		bus.write_i2c_block_data(self.addr, self.pow_sav, self.power_save_mode)
	def read_data(self):
		#The frequency to read the sensor should be set greater than
		# the integration time (and the power saving delay if set).
		# Reading at a faster frequency will not cause an error, but
		# will result in reading the previous data
		time.sleep(.04) # 40ms
		word = bus.read_word_data(addr,als)
		wordIR = bus.read_word_data(addr,white)
		gain = 0.2304 # gain=1/4 and int time=100ms, max lux=15099 lux
		#Reference www.vishay.com/docs/84367/designingveml6030.pdf
		# 'Calculating the LUX Level'

		val = word * gain
		valIR = wordIR * gain
		#val = round(val,1)
		#valIR = round(valIR,1)

		# Reference www.vishay.com/docs/84367/designingveml6030.pdf
		# 'Calculating the LUX Level'

		valcorr = (6.0135E-13*val**4)-(9.392E-9*val**3)+(8.1488E-5*val**2)+(1.0023E0*val)
		valcorr = round(valcorr,1) #Round corrected value for presentation
		val = round(val,1) #Round value for presentation
		#return (val, valIR)
		return {"light": {"value": val, "unit": "lux",
				"IR light": {"value": val, "unit": "lux"}
			   }
