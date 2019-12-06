#ifndef __TRISTAR_H
#define __TRISTAR_H

#include <string>
#include <stdio.h>
#include <fstream>
#include <modbus.h>
// Array sizes are defined here.
#define ADC_VALUES_ARRAY_SIZE 11
#define TEMPERATURE_VALUES_ARRAY_SIZE 3
#define STATUS_VALUES_ARRAY_SIZE 9
#define CHARGER_VALUES_ARRAY_SIZE 6
#define MPPT_VALUES_ARRAY_SIZE 5
#define LOGGER_VALUES_ARRAY_SIZE 14
#define CHARGE_SETTINGS_ARRAY_SIZE 25
class Morningstar {
	public: 
		float V_PU;
		float I_PU;
		Morningstar();
		Morningstar(string port, int baud, int dev_ID, char par,int d_bit, int s_bit);
		void Scaling();
		void ADCData();
		void TemperatureData();
		void StatusData();
		void ChargerData();
		void MPPTData();
		void LoggerData();
		void ChargeSettings();
		void Update();
		void DumpToJSON(ofstream outfile);
		
	private: 
		string port; // name of port to open on operating system.
		int baudrate; // baudrate.
		char parity; // 'N', 'E', or 'O'.
		int data_bits; // number of data bits transferred.
		int stop_bit; // number of bits to stop
		int DEVICE_ID; // MODBUS slave number.
		modbus_t *mb; // the actual reader.
		uint16_t tab_reg[64]; // the buffer that the reader needs to put data into.
		
		
		
		float *ADC_values_array;
		int *Temperature_values_array;
		string *Status_values_array;
		string *Charger_values_array;
		float *MPPT_values_array;	
		string *Logger_values_array;
		float *Charge_settings_array;
		
		
		void ADCData();
		void TemperatureData();
		void StatusData();
		void ChargerData();
		void MPPTData();
		void LoggerData();
		void ChargeSettings();
		
}

#endif