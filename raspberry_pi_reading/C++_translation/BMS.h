#ifndef BMS_H
#define BMS_H

#if (defined(__unix__) || defined(unix)) && !defined(USG)
#include <sys/param.h>
#endif


#ifndef _MSC_VER
	#include <stdint.h>
#else
	#include "stdint.h"
#endif

#include <string>
#include "serial/serial.h"

class BMS {
	public: 
		BMS();
		BMS(string port, int baud, char par,int d_bit, int s_bit);
		void VR1();
	private: 
		string port;
		char parity;
		int baud;
		int data_bits;
		int stop_bit;	
		serial::Serial ser;
		
		string Hardware_type;
		string Serial_number;
		string Version_number;
		int number_of_cells;
		float minCellBalancingRate;
		float maxCellBalancingRate;
		float averageCellBalancingRate;
		float balancingVoltageThreshold;
		float *BB2;
		float *BB3;
		float *BB4;

}

#endif