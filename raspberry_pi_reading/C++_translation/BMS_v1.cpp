#include <stdio.h>
#include <string>
#include <cstring>
#include <iostream>
#include <cstudio>
#include <unistd.h>
#include <vector>
#include <fstream>

#include "serial/serial.h"
#include "BMS.h"
#include "CRC8_Dallas.h"
#include "JSON.hpp"

#define READ_SIZE 65536
using namespace std;
// sleep function necessary for the serial library.
void my_sleep(unsigned long milliseconds)

{
#ifdef _WIN32
	Sleep(milliseconds); // 100 ms
#else
	usleep(milliseconds*1000); // 100ms
}
// converts from uint8_t to char.
char singleHexCharFromInt(uint8_t);
// tokenizes a string.
vector<string> split(const string& str, const string& delim);
// constructs a string
string constructSentence(string&);
// checks a string to see if it has proper CRC8 value
bool checkSentence(string&);

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

// This is a special sentence. Instead of writing to an array, it will write a string to the
// object variables Hardware_type, Serial_number, and Firmware_version.
void BMS::VR1() {
	string sentence = constructSentence("VR1,?,");
	// send the package. It will automatically call the sleep function.
	size_t bytes_wrote = ser.write(sentence);
	// ask for the response.
	string response = ser.readline(READ_SIZE, "\n");
	// the response will be in a string format.
	// the string will be formatted like this:
	// VR1,Hardware_type,Serial_number,Firmware_version,CRC8_value.
	if(!checkSentence(response)) {
		return;
	}
	
	// tokenize the string. 
	
	vector<string> responses = split(response, ",");
	Hardware_type = responses[1];
	Serial_number = responses[2];
	Firmware_version = responses[3];
}
void BMS::BB1() {
	string sentence = constructSentence("BB1,?,");
	// send the package. It will automatically call the sleep function.
	size_t bytes_wrote = ser.write(sentence);
	// ask for the response.
	string response = ser.readline(READ_SIZE, "\n");
	// the response will be in a string format.
	
	if(!checkSentence(response)) {
		return;
	}
	vector<string> responses = split(response, ",");
	// copied from the python version.
	number_of_cells = DecimalstringToInteger(responses[1]);
	minCellBalancingRate = (float) HexstringToInteger(responses[2]) * 100 / 255;
	maxCellBalancingRate =  (float) HexstringToInteger(responses[3]) * 100 / 255;
	averageCellBalancingRate = (float) HexstringToInteger(responses[5])*100/255;
	balancingVoltageThreshold = (float) (HexstringToInteger(r[6],16)+200)*0.01;
}
void BMS::Update() {
	VR1();
	BB1();
}
void BMS::DumpToJSON(string filename) {
	Update();
	json j;
	j["Hardware type"] = Hardware_type;
	j["Serial number"] = Serial_number;
	j["Firmware version"] = Firmware_version;
	ofstream myfile(filename);
	myfile << j;
}

// Helper functions
string constructSentence(const string& sentence) {
	string response = sentence;
	uint8_t x = CRC8(sentence, strlen(sentence)) 
	//uint8_t y = x & (0xF);
	//uint8_t z = (x >> 4) & (0xF);
	// convert from uint8_t to 2 characters. example:
	// 00001000 = 0x08
	// append 0, then 8.
	// there's a helper function for this. 
	response.append(singleHexCharFromInt((x >> 4));
	response.append(singleHexCharFromInt((x & 0xF));
	return response;
}
char singleHexCharFromInt(uint8_t x) {
	switch(x) {
		case 0:
		case 1: 
		case 2:
		case 3:
		case 4:
		case 5:
		case 6:
		case 7:
		case 8:
		case 9:
			return (char) x + '0';
			break;
		case 10: return 'a';
		case 11: return 'b';
		case 12: return 'c';
		case 13: return 'd';
		case 14: return 'e';
		case 15: return 'f';
		default: return '0';
	}
}

// source: https://stackoverflow.com/questions/14265581/parse-split-a-string-in-c-using-string-delimiter-standard-c
vector<string> split(const string& str, const string& delim)
{
    vector<string> tokens;
    size_t prev = 0, pos = 0;
    do
    {
        pos = str.find(delim, prev);
        if (pos == string::npos) pos = str.length();
        string token = str.substr(prev, pos-prev);
        if (!token.empty()) tokens.push_back(token);
        prev = pos + delim.length();
    }
    while (pos < str.length() && prev < str.length());
    return tokens;
}
bool checkSentence(const string& response) {
	// let's determine the size of the response.
	// size is how many characters are in the sentence.
	// sentenceSize is how many characters are actually in the sentence.
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
		// response[i-1] is X.
		// response[i] is Y.
		// read the library for details.
	uint8_t sentCRC8Value = crc8_from2Chars((char) (response[i-1] & 0xFF), (char) (response[i] & 0xFF));;
	// determine actual CRC8 value
	// we're using a library I found on Wikipedia for this.
	uint8_t actualCRC8Value = crc8(CRC8sentence, (uint16_t) sentenceSize);
	// free unneeded space.
	free(CRC8sentence);
	// comparison time.
	// I don't know how to handle bad CRC8 values yet. 
	if (sentCRC8Value != actualCRC8Value) {
		cout << "SHIT!!!!!" << endl;
		return false;
	} else {
		return true;
	}
}
int DecimalstringToInteger(string a) {
	int sum = 0;
	int power = 0;
	for(int i = a.size(); i >= 0 ; i--) {
		int number = a[i] - '0';
		for(int j = 0; j < power; j++) {
			number *= 10;
		}
		sum += number;
		power++;
	}
	return sum;
}

int HexstringToInteger(string a) {
	int sum = 0;
	int power = 0;
	for(int i = a.size(); i >= 0 ; i--) {
		int number;
		switch(a[i]) {
			case '0':
			case '1':
			case '2':
			case '3':
			case '4':
			case '5':
			case '6':
			case '7':
			case '8':
			case '9': 
				number = a[i] - '0';
				break;
			case 'a':
			case 'A':
				number = 10;
				break;
			case 'b':
			case 'B':
				number = 11;
				break;
			case 'c':
			case 'C':
				number = 12;
				break;
			case 'd':
			case 'D':
				number = 13;
				break;
			case 'e':
			case 'E':
				number = 14;
				break;
			case 'f':
			case 'F':
				number = 15;
				break;
			default:
				number = 0;
				break;
		}
		for(int j = 0; j < power; j++) {
			number *= 16;
		}
		sum += number;
		power++;
	}
	return sum;
}