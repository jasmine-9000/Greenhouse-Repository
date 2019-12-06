#!/usr/bin/python 

import time,sys
import RPi.GPIO as GPIO
import serial

#you must enable UART on the Raspberry Pi to use this code.

class FONA:
	def __init__(self,port="/dev/ttyS0",baudrate=9600, PIN="******",):
		"""
		
		
		"""
		#initialize the connection to the fona.
		#default is through the UART port on the Raspberry PI.
		self.port = port
		self.baudrate = baudrate
		self.ser = serial.Serial(port,baudrate)
		
		self.PIN = PIN
	def execute(self,sentence):
		"""
			
		"""
		self.ser.write(sentence)
		self.ser.flush()
		return self.ser.readline()
	def sendJSONfile(self, JSON_file,APN=None,username=None,password=None,IP_address='localhost'):
		#let's use a SIM900 for demonstration.
		if not isinstance(APN, "str"):
			return False
		response = self.execute("AT") #this always comes first. Checks if the PI is connected to the SIM card at all.
		if not response == "OK":
			return False
		response = self.execute("AT+CREG?") # is the SIM ready?
		if not response == "OK":
			return False 
		response = self.execute("AT+CGATT?") # Does the SIM card have internet access?
		if not response == "OK":
			return False
			
		response = self.execute("AT+CIPSTATUS") # Configure modem to make a single port open for connection.
		if not response == "OK":
			return False
			
		response = self.execute(
			"AT+CSTT=\"" + webDomain +"\",\"" + str(username) + 
			"\",\"" + str(password) + "\""
								) #connect to the internet. Parameters: APN, username, password.
		if not response == "OK":
			return False
			
		response = self.execute("AT+CIICR") #bring up wireless network. ensure that the modem has a SIM with credit and data plan activated.
		if not response == "OK":
			return False
		
		server = str(IP_address) #server IP address is not known yet. default is localhost.
		port = 80 #port number is 80 for non-admin access.
		#let's make a TCP connection at the server IP address on port 80.
		#I would like a CS student to write a proper website for me.
		#I also need to set up my website so that it accepts JSON files.
		#I found these commands using https://www.slideshare.net/DevrhoidDavis1/at-command-set-for-sending-data-via-tcp-using-sim900
		
		response = self.execute("AT+CIPSTART=\"TCP\",\"" + server + "\",\"" + str(port) + "\"")
		if not response == "OK":
			return False
		response = self.ser.readline()
		if not response == "OK":
			return False
		
		#let's make our request now.
		#we want to make an HTTP POST request for this one.
		response = self.execute("AT+CIPSEND")
		if not response == ">":
			return False
		#let's first build our request.
		request  = "POST /newtasks HTTP/1.1\r\n"  # we want to make a post requet
		request += "HOST: localhost\n" #our host:  localhost (for now)
		request += "Accept: application/json\r\n" #we must let the server know what application it needs to use.
		request += "Content-Type: application/json\r\n"  #let the server know what kind of a file we're sending.
		request += "Content-Length: " + str(len(JSON_file)) + "\r\n\r\n" #let the server know how long the file is (in bytes)
		request += str(JSON_file) #send the JSON file in ASCII form.
		request += "\r\n" + "\r\x1A" # we need an EOF character at the end. in the AT command line, this is SUB, represented by the number 0x1A.
				
		response = self.execute(request)
		if not response == "SEND OK":
			return False
		return True
	def checkforUpdates(self):
		"""
		we will not be sending code to the raspberry Pi using the server.
		to send code, we will be SSH-ing into the Raspberry Pi using a laptop PC.
		"""
		response = self.execute("AT")
		if not response == "OK":
			return False
		return True
if __name__ == "__main__":
	#testing grounds.
	testFONA = FONA("dev/ttyS0",9600,"1234")
	testJSON = '{ "status": 404,"error": "not found" }'
	testFona.sendJSONfile(testJSON)
	