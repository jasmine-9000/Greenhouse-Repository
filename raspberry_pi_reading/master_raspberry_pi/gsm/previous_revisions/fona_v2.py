import time, sys
import serial

class FONA:
	def __init__(self, port="/dev/ttyS0",baudrate=9600,PIN="****"):
		self.port = port
		self.baudrate=baudrate
		self.ser = serial.Serial(port,baudrate,timeout=5)
		self.PIN = PIN
	def execute(self, sentence):
		#convert sentence to bytes
		byteArray = bytes(sentence, 'ascii')
		self.ser.write(byteArray)
		self.ser.flush()
		data = []
		while True:
			response = self.ser.readline().decode()
			if response == '':
				break
			data.append(response)
		return data

	def init(self,APN,username,password):	
		response = self.execute("AT") #this always comes first. Checks if the PI is connected to the SIM card at all.
		if not response == ["OK"]:
			return False
		
		response = self.execute("AT+CREG?") # is the SIM ready? and does it have correct permissions to connect to the internet?
		permissions = response[0]
		if permissions == "ERROR":
			return False 
			
		response = self.execute("AT+CGATT?") # Does the SIM card have internet access?
		if not response == ["OK"]:
			return False
			
		response = self.execute("AT+CIPSTATUS") # Configure modem to make a single port open for connection.
		if not response == ["OK"]:
			return False
			
		response = self.execute(
			"AT+CSTT=\"" + str(APN) +"\",\"" + str(username) + 
			"\",\"" + str(password) + "\""
								) #connect to the internet. Parameters: APN, username, password.
		if not response == ["OK"]:
			return False
			
		response = self.execute("AT+CIICR") #bring up wireless network. ensure that the modem has a SIM with credit and data plan activated.
		if not response == ["OK"]:
			return False
	def HTTP_POST()
		