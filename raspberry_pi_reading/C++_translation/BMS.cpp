#include <stdio.h>
#include <string>
#include <cstring>
#include <iostream>
#include <cstdio>
#include <unistd.h>
#include <vector>

#include "serial/serial.h"
#include "BMS.h"
#include "CRC8_Dallas.h"

using namespace std;
// sleep function necessary for the serial library.
void my_sleep(unsigned long milliseconds)
{
#ifdef _WIN32
	Sleep(milliseconds); // 100 ms
#else
	usleep(milliseconds*1000); // 100ms
}

// Default BMS constructor
BMS::BMS() {
	cout << "Default constructor called. No connection made." << endl;
}
// Parameterized Constructor:
BMS::BMS(string device, int baud, char par='N', int d_bit=8, int s_bit=2) {
	port = device,
	parity = par;
	data_bits = d_bit;
	stop_bit = s_bit;
	ser = serial::Serial (device, baud, serial::Timeout::simpleTimout(1000));
	if(ser.isOpen()) {
		cout << "Successfully created connection." << endl;
	} else {
		cout << "No connection." << endl;
	}
}



vector<string> BMS::VR1() {
	string sentence = "VR1,?,";
	// calculate the CRC8 value, then append it to the sentence.
	uint8_t x = CRC8(sentence, strlen(sentence))
	sentence.append(chr(x));
	
	// ask for the response.
	size_t bytes_wrote = ser.write(sentence);
	string response = ser.readline(65536, "\n");
	
	int size = response.size() + 1;
	int sentenceSize = size-2;
	
	// CRC8 check
	// first, let's copy the real sentence into the CRC8 sentence for later.
	// we're going to read the CRC8 sentence later.
	uint8_t *CRC8sentence = (uint8_t) malloc(sentenceSize);
	int i;
	for(i = 0; i < sentenceSize; i++) {
		CRC8sentence[i] = (uint8_t) response[i];
	}
	// determine sent CRC8 value
		// reuse i from last loop to determine CRC8 value sent.
		// CRC8 value sent is in form (XY)_base16. 
		// response[i] is X.
		// response[i+1] is Y.
		// read the library.
	uint8_t sentCRC8Value = crc8_from2Chars(response[i], response[i+1]);;
	// determine actual CRC8 value
	// we're using a library I found on Wikipedia for this.
	uint8_t actualCRC8Value = crc8(CRC8sentence, sentenceSize);
	// free unneeded space.
	free(CRC8sentence);
	// comparison time.
	// I don't know how to handle bad CRC8 values yet. 
	if (sentCRC8Value != actualCRC8Value) {
		cout << "SHIT!!!!!" << endl;
		return NULL;
	}
	
	// Copy string to char array for processing. 
	char r[size];
	strcpy(r, &response[0]);
	
	// split the sentence into statements.
	char *token = strtok(input, ",");
	vector<string> responses;
	
	while(token!=NULL) {
		responses.push_back(token);
		token = strtok(NULL, ",");
	}
	/* 
	responses format: 
	
	responses[0]: Must be exactly "VR1". If not, terminate process.
	responses[1]: hardware type
	responses[2]: serial number
	responses[3]: firmware version
	responses[4]: CRC8 value
	*/
	if(responses[0] != "VR1") {
		cout << "wrong response." << endl;
		return NULL;
	}
	// erase the CRC8 value.
	responses.pop_back();
	// erase "VR1".
	responses.erase(responses.begin());
	return responses;
}
void BMS::Update() {
	VR1();
}
/*
test bench (unusable here)
int main(void) {
	modbus_t *mb
	uint16_t tab_reg[32];
	int baud = 9600;
	if(std::system_interface.startswith == "win32") {
		device = ""
	}
	char *device = "";
	char parity = 'N';
	int data_bits = 8;
	int stop_bit = 1;
	
	mb = modbus_new_rtu("", 1)
	modbus_close(mb);
	modbus_free(mb);
}*/
