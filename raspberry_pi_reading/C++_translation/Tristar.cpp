#include <iostream>
#include <string>
#include "Tristar.h"
#include "json.hpp"
// Where in the PLC's memory are the data located?
// The locations are defined here.
#define ADC_DATA_BEGIN 0x0018
#define ADC_DATA_LENGTH 11

#define TEMPERATURE_DATA_BEGIN 0x0023
#define TEMPERATURE_DATA_LENGTH 3

#define STATUS_DATA_BEGIN 0x0026
#define STATUS_DATA_LENGTH 12

#define CHARGER_DATA_BEGIN 0x0032
#define CHARGER_DATA_LENGTH 8

#define MPPT_DATA_BEGIN 0x003A
#define MPPT_DATA_LENGTH 5

#define LOGGER_DATA_BEGIN 0x0040
#define LOGGER_DATA_LENGTH 16

#define CHARGE_SETTINGS_BEGIN 0xE000
#deifne CHARGE_SETTINGS_LENGTH 32

// A modifier used later to process data.
#define SMALL_MODIFIER 0x8000
#define BIG_MODIFIER 0x20000

// helper functions defined up here.
uint16_t hexCharToDecimal(uint16_t);
uint16_t hex2int(char);


// default constructor
Morningstar::Morningstar() {
	cout << "Default constructor called." << endl;
}
// parameterized constructor.
Morningstar::Morningstar(string port, int baud, int dev_ID, char par='N',int d_bit=8, int s_bit=1) {
	// save the settings to internal class variables.
	device = port;
	baudrate = baud;
	parity = par;
	data_bits = d_bit;
	stop_bit = s_bit;
	DEVICE_ID = dev_ID;
	// start the connection.
	mb = modbus_new_rtu(port, baud,par,d_bit,s_bit);
	if (mb == NULL) {
		fprintf(stderr, "Unable to create the libmodbus contet\n");
		return -1;
	}
	// initialize the connection.
	modbus_set_slave(mb, dev_ID);
	if(modbus_connect(mb) == -1) {
		fprintf(stderr, "connection failed: %s\n", modbus_strerror(errno));
		modbus_free(mb);
		return -1;
	}
	// allocate sufficient space for the arrays.
	ADC_values_array = (float) malloc(sizeof(float)*ADC_VALUES_ARRAY_SIZE);
	Temperature_values_array = (int) malloc(sizeof(int)*TEMPERATURE_VALUES_ARRAY_SIZE);
	Status_values_array = (string) malloc(sizeof(string)*STATUS_VALUES_ARRAY_SIZE);
	Charger_values_array = (string) malloc(sizeof(string)*CHARGER_VALUES_ARRAY_SIZE);
	MPPT_values_array = (float) malloc(sizeof(float)*MPPT_VALUES_ARRAY_SIZE);;
	Logger_values_array = (string) malloc(sizeof(string)*LOGGER_VALUES_ARRAY_SIZE);
	Charge_settings_array = (float) malloc(sizeof(float)*CHARGE_SETTINGS_ARRAY_SIZE);
	// Call Scaling(). It's absolutely necessary.
	Scaling();
}
// destructor
Morningstar::~Morningstar() {
	// close the connection, then free it.
	modbus_close(mb);
	modbus_free(mb);
	// free all the space we allocated earlier.
	// there will be no memory leaks here!!!
	free(ADC_values_array);
	free(Temperature_values_array);
	free(Status_values_array);
	free(Charger_values_array);
	free(MPPT_values_array);	
	free(Logger_values_array);
	free(Charge_settings_array);
}


// Reads the current V_PU and I_PU values that are being used by the Morningstar's PLC.
// Saves it to the object's V_PU and I_PU values.
// Absolutely necessary to call in order to read values correctly.
void Morningstar::Scaling() {
	// the scaling terms are located at addresses 0,1,2,and 3. Version number is located at address 4.
	modbus_read_registers(mb, 0,5, tab_reg);
	V_PU = tab_reg[0] + tab_reg[1] >> 15;
	I_PU = tab_reg[2] + tab_reg[3] >> 15;
	cout << "Running version " << tab_reg[4] << endl;
}


// Reads ADC Data from the Morningstar's PLC.
// Saves it to the object's ADC data array.
void Morningstar::ADCData() {
	modbus_read_registers(mb, ADC_DATA_BEGIN, ADC_DATA_LENGTH, tab_reg);
	ADC_values_array[0] = hexCharToDecimal(tab_reg[0])*V_PU / SMALL_MODIFIER;
	ADC_values_array[1] = hexCharToDecimal(tab_reg[1])*V_PU / SMALL_MODIFIER;
	ADC_values_array[2] = hexCharToDecimal(tab_reg[2])*V_PU / SMALL_MODIFIER;
	ADC_values_array[3] = hexCharToDecimal(tab_reg[3])*V_PU / SMALL_MODIFIER;
	ADC_values_array[4] = hexCharToDecimal(tab_reg[4])*I_PU / SMALL_MODIFIER;
	ADC_values_array[5] = hexCharToDecimal(tab_reg[5])*I_PU / SMALL_MODIFIER;
	ADC_values_array[6] = hexCharToDecimal(tab_reg[6])*18.612 / SMALL_MODIFIER;
	ADC_values_array[7] = hexCharToDecimal(tab_reg[7])*6.6 / SMALL_MODIFIER;
	ADC_values_array[8] = hexCharToDecimal(tab_reg[8])*18.612 / SMALL_MODIFIER;
	ADC_values_array[9] = hexCharToDecimal(tab_reg[9])*3 / SMALL_MODIFIER;
	ADC_values_array[10]= hexCharToDecimal(tab_reg[10])*3 / SMALL_MODIFIER;
	/*
	float bat_voltage = hexCharToDecimal(tab_reg[0])*V_PU / SMALL_MODIFIER;
	float bat_terminal_voltage = hexCharToDecimal(tab_reg[1])*V_PU / SMALL_MODIFIER;
	float bat_sense_voltage = hexCharToDecimal(tab_reg[2])*V_PU / SMALL_MODIFIER;
	float arr_voltage = hexCharToDecimal(tab_reg[3])*V_PU / SMALL_MODIFIER;
	float battery_current = hexCharToDecimal(tab_reg[4])*I_PU / SMALL_MODIFIER;
	float arr_current = hexCharToDecimal(tab_reg[5])*I_PU / SMALL_MODIFIER;
	float supp_12v = hexCharToDecimal(tab_reg[6])*18.612 / SMALL_MODIFIER;
	float supp_3v = hexCharToDecimal(tab_reg[7])*6.6 / SMALL_MODIFIER;
	float meterbus_voltage = hexCharToDecimal(tab_reg[8])*18.612 / SMALL_MODIFIER;
	float supp_1_8v = hexCharToDecimal(tab_reg[9])*3 / SMALL_MODIFIER;
	float v_ref = hexCharToDecimal(tab_reg[10])*3 / SMALL_MODIFIER;
	*/
	
	
}


// Reads Temperature Data from the Morningstar's PLC>
// Saves it to the object's Temperature data array.
void Morningstar::TemperatureData() {
	modbus_read_registers(mb, TEMPERATURE_DATA_BEGIN, TEMPERATURE_DATA_LENGTH, tab_reg);
	Temperature_values_array[0] = hexCharToDecimal(tab_reg[0]);
	Temperature_values_array[1] = hexCharToDecimal(tab_reg[1]);
	Temperature_values_array[2] = hexCharToDecimal(tab_reg[2]);
}


// Reads Status data from the Morningstar PLC>
// Saves it to the object's Status data array.
void Morningstar::StatusData() {
	modbus_read_registers(mb, STATUS_DATA_BEGIN, STATUS_DATA_LENGTH, tab_reg);
	float battery_voltage = hexCharToDecimal(tab_reg[0])*V_PU / SMALL_MODIFIER;
	float charging_current = hexCharToDecimal(tab_reg[1])*I_PU / SMALL_MODIFIER;
	float min_bat_voltage =hexCharToDecimal(tab_reg[2])*V_PU / SMALL_MODIFIER;
	float max_bat_voltage =hexCharToDecimal(tab_reg[3])*V_PU / SMALL_MODIFIER;
	uint32_t hourmeter = hexCharToDecimal(tab_reg[5]) + hexCharToDecimal(tab_reg[4]) << 16;
	Status_values_array[0] = std::to_string(battery_voltage);
	Status_values_array[1] = std::to_string(charging_current);
	Status_values_array[2] = std::to_string(min_bat_voltage);
	Status_values_array[3] = std::to_string(max_bat_voltage);
	Status_values_array[4] = std::to_string((long) hourmeter);
	
	
	
	uint16_t bitfield = tab_reg[6];
	string faults = "";
	std::string faultsTable[] {"overcurrent", "FETs shorted","software bug",
		"battery HVD","array HVD","settings switch changed",
		"custom settings edit","RTS shorted","RTS disconnected",
		"EEPROM retry limit","N/A_10","Slave Control Timeout",
		"N/A_13","N/A_14","N/A_15","N/A_16"};
	for(int i = 0; i < 16; i++) {
		if (bitfield & (0xFFFF & (0x1 << i))) {
			faults.append(faultsTable[i]);
			faults.append(", ");
		}
	}
	Status_values_array[5] = faults;
	
	uint32_t bitfield_1 = (tab_reg[9] << 16) | tab_reg[8];
	string alarms = "";
	std::string alarmsTable[] {"RTS open", "RTS shorted", "RTS disconnected", 
		"Heatsink temp sensor open", "Heatsink temp sensor shorted",
		"High temperature current limit", "Current limit", "Current offset",
		"Battery sense out of range", "Battery sense disconnected",
		"Uncalibrated", "RTS miswire", "High voltage disconnect",
		"Undefined", "System miswire", "MOSFET open", "P12 voltage off",
		"High input voltage current limit", "ADC input max",
	"Controller was reset", "N/A_21", "N/A_22", "N/A_23","N/A_24"};
	for(int i = 0; i < 32; i++) {
		if (bitfield_1 & (0x007FFFF & (0x1 << i))) {
			alarms.append(faultsTable[i]);
			alarms.append(", ");
		}
	}
	Status_values_array[6] = alarms;
	
	
	uint16_t dipswitch = tab_reg[10];
	string dipswitchstatement = "";
	for(int i = 0; i < 8; i++) {
		if(dipswitch & (0x1 << i)){
			dipswitchstatement.append("ON ");
		} else {
			dipswitchstatement.append("OFF ");
		}
	}
	Status_values_array[7] = dipswitchstatement;
	
	ledvalue = tab_reg[11];
	std::string LEDTable[] {
		"LED START","LED START 2","LED BRANCH", "FAST GREEN BLINK","SLOW GREEN BLINK","GREEN BLINK, 1HZ","GREEN LED","UNDEFINED", "YELLOW LED","UNDEFINED","BLINKING RED LED","RED LED","R-Y-G ERROR","R/Y-G ERROR","R/G-Y ERROR","R-Y ERROR (HTD)","R-G ERROR (HVD)","R/Y-G/Y ERROR", "G/Y/R ERROR","G/Y/R X2"};
	string ledstate;
	if(ledvalue > 19) {
		ledstate = "LED State value not recognized";
	} else {
		ledstate = LEDTable[ledvalue];
	}
	Status_values_array[8] = ledstate;
	
}

// Reads Charger data from the Morningstar PLC.
// Saves it to the object's Charger data array.
void Morningstar::ChargerData() {
	modbus_read_registers(mb, CHARGER_DATA_BEGIN, CHARGER_DATA_LENGTH, tab_reg);
	uint16_t chargerValue = tab_reg[0];
	string chargeState;
	if(chargerValue == 0){ chargeState =  "START" };
	else if (chargerValue == 1){ chargeState =  "NIGHT CHECK" };
	else if (chargerValue == 2){ chargeState =  "DISCONNECT" };
	else if (chargerValue == 3){ chargeState =  "NIGHT" };
	else if (chargerValue == 4){  chargeState =  "FAULT" };
	else if (chargerValue == 5){  chargeState =  "MPPT" };
	else if (chargerValue == 6){  chargeState =  "ABSORPTION" };
	else if (chargerValue == 7){  chargeState =  "FLOAT" };
	else if (chargerValue == 8){  chargeState =  "EQUALIZE" };
	else if (chargerValue == 9){  chargeState =  "SLAVE" };
	else ( chargeState =  "Charge state value not recognized." };
	Charger_values_array[0] = chargeState;
	// target regulation voltage
	Charger_values_array[1] = to_string((float) tab_reg[1]);
	// Ah Charge Resettable
	Charger_values_array[2] = to_string( (tab_reg[3] | tab_reg[2] << 16)*0.1);
	// Ah Charge Total
	Charger_values_array[3] = to_string( (tab_reg[5] | tab_reg[4] << 16)*0.1);
	// kWhr charge resettable
	Charger_values_array[4] = to_string(tab_reg[6]);
	// kWhr charge total
	Charger_values_array[5] = to_string(tab_reg[7]);
}

// reads MPPT data from the Morningstar PLC>
// Saves it to the object's MPPT data array.
void Morningstar::MPPTData() {
	modbus_read_registers(mb, MPPT_DATA_BEGIN, MPPT_DATA_LENGTH, tab_reg);
	float P_out = hexCharToDecimal(tab_reg[0])*V_PU*I_PU / BIG_MODIFIER;
	float P_in = hexCharToDecimal(tab_reg[1])*V_PU*I_PU / BIG_MODIFIER;
	float P_max = hexCharToDecimal(tab_reg[2])*V_PU*I_PU / BIG_MODIFIER;
	float Vmp = hexCharToDecimal(tab_reg[3])*V_PU / SMALL_MODIFIER;
	float Voc = hexCharToDecimal(tab_reg[4])*V_PU / SMALL_MODIFIER;
	MPPT_values_array[0] = P_out;
	MPPT_values_array[1] = P_in;
	MPPT_values_array[2] = P_max;
	MPPT_values_array[3] = V_mp;
	MPPT_values_array[4] = V_oc;
}

// reads Logger data from the Morningstar PLC.
// Saves it to the object's Logger data array.
void Morningstar::LoggerData() {
	modbus_read_registers(mb, LOGGER_DATA_BEGIN, LOGGER_DATA_LENGTH, tab_reg);
	float bat_voltage_min_daily = hexCharToDecimal(tab_reg[0])*V_PU / SMALL_MODIFIER;
	float bat_voltage_max_daily = hexCharToDecimal(tab_reg[1])*V_PU / SMALL_MODIFIER;
	float input_voltage_max_daily = hexCharToDecimal(tab_reg[2])*V_PU / SMALL_MODIFIER;
	float Ah_daily = hexCharToDecimal(tab_reg[3])*0.1
	float Wh_daily = hexCharToDecimal(tab_reg[4]);
	float Max_Power_output_daily = hexCharToDecimal(tab_reg[6])*V_PU*I_PU / BIG_MODIFIER;
	float min_temperature_daily = hexCharToDecimal(tab_reg[7]);
	float max_temperature_daily = hexCharToDecimal(tab_reg[8]);
	
	float time_ab_daily = hexCharToDecimal(tab_reg[13]);
	float time_eq_daily = hexCharToDecimal(tab_reg[14]);
	float time_fl_daily = hexCharToDecimal(tab_reg[15]);
	
	std::string alarmsTable[] { "RTS open", "RTS shorted", "RTS disconnected", 
		"Heatsink temp sensor open", "Heatsink temp sensor shorted",
		"High temperature current limit", "Current limit", "Current offset",
		"Battery sense out of range", "Battery sense disconnected",
		"Uncalibrated", "RTS miswire", "High voltage disconnect",
		"Undefined", "System miswire", "MOSFET open", "P12 voltage off",
		"High input voltage current limit", "ADC input max",
		"Controller was reset", "N/A_21", "N/A_22", "N/A_23","N/A_24"};
	std::string flagsTable[] {"Reset detected", "Equalize Triggered",
	"Enered float", "An alarm occurred", "A fault occurred"};
	
	std::string faultsTable[] {"overcurrent", "FETs shorted","software bug",
		"battery HVD","array HVD","settings switch changed",
		"custom settings edit","RTS shorted","RTS disconnected",
		"EEPROM retry limit","N/A_10","Slave Control Timeout",
	"N/A_13","N/A_14","N/A_15","N/A_16"};
	std::string alarms = "";
	std::string faults = "";
	std::string flags = "";
	uint32_t alarmsBitfield = (tab_reg[11] << 16) | tab_reg[12];
	uint32_t faultsBitfield = (uint32_t) tab_reg[9];
	uint32_t flagsBitfield = (uint32_t) tab_reg[5];
	for(int i = 0; i < 24; i++) {
		if( i < 5) {
			if(flagsBitfield & 0x0000001F & (0x1<< i)) {
				flags.append(flagsTable[i]);
				flags.append(", ");
			}
		}
		if( i < 24) {
			if(alarmsBitfield & 0x007FFFFF & (0x1<< i)) {
				alarms.append(alarmsTable[i]);
				alarms.append(", ");
			}
		}
		if (i < 16) {
			if(faultsBitfield & 0x000000FF & (0x1<< i)) {
				faults.append(faultsTable[i]);
				faults.append(", ");
			}
		}
	}
	Logger_values_array[0] = to_string(bat_voltage_max_daily);
	Logger_values_array[1] = to_string(bat_voltage_min_daily);
	Logger_values_array[2] = to_string(input_voltage_max_daily);
	Logger_values_array[3] = to_string(Ah_daily);
	Logger_values_array[4] = to_string(Wh_daily);
	Logger_values_array[5] = to_string(Max_Power_output_daily);
	Logger_values_array[6] = to_string(min_temperature_daily);
	Logger_values_array[7] = to_string(max_temperature_daily);
	Logger_values_array[8] = alarms;
	Logger_values_array[9] = flags;
	Logger_values_array[10] = faults;
	Logger_values_array[11] = to_string(time_ab_daily);
	Logger_values_array[12] = to_string(time_ab_daily);
	Logger_values_array[13] = to_string(time_ab_daily);
	
	
}

// reads Charge Settings from the Morningstar PLC. 
// Saves it to the object's charge settings array.
void Morningstar::ChargeSettings() {
	modbus_read_registers(mb, CHARGE_SETTINGS_BEGIN, CHARGE_SETTINGS_LENGTH, tab_reg);
	float EV_absorp = hexCharToDecimal(tab_reg[0])*V_PU / SMALL_MODIFIER;
	float EV_float = hexCharToDecimal(tab_reg[1])*V_PU / SMALL_MODIFIER;
	float Et_absorp = hexCharToDecimal(tab_reg[2]);
	float Et_absorp_ext = hexCharToDecimal(tab_reg[3]);
	float EV_absorp_ext = hexCharToDecimal(tab_reg[4])*V_PU / SMALL_MODIFIER;
	float EV_float_cancel = hexCharToDecimal(tab_reg[5])*V_PU / SMALL_MODIFIER;
	float Et_float_exit_cum = hexCharToDecimal(tab_reg[6]);
	float EV_eq = hexCharToDecimal(tab_reg[7])*V_PU / SMALL_MODIFIER;
	float Et_eqcalendar = hexCharToDecimal(tab_reg[8]);
	float Et_eq_above = hexCharToDecimal(tab_reg[9]);
	float Et_eq_reg = hexCharToDecimal(tab_reg[10]);
	float Et_battery_service = hexCharToDecimal(tab_reg[11]);
	float EV_tempcomp = hexCharToDecimal(tab_reg[13])*V_PU / SMALL_MODIFIER / 2;
	float EV_hvd = hexCharToDecimal(tab_reg[14]) * V_PU / SMALL_MODIFIER;
	float EV_hvr = hexCharToDecimal(tab_reg[15]) * V_PU / SMALL_MODIFIER;
	float Evb_ref_lim = hexCharToDecimal(tab_reg[16]) *V_PU / SMALL_MODIFIER;
	float ETb_max =hexCharToDecimal(tab_reg[17]);
	float ETb_min = hexCharToDecimal(tab_reg[18]);
	float EV_soc_g_gy = hexCharToDecimal(tab_reg[21])*V_PU / SMALL_MODIFIER;
	float EV_soc_gy_y = hexCharToDecimal(tab_reg[22])*V_PU / SMALL_MODIFIER;
	float EV_soc_y_yr = hexCharToDecimal(tab_reg[23])*V_PU / SMALL_MODIFIER;
	float EV_soc_yr_r = hexCharToDecimal(tab_reg[24])*V_PU / SMALL_MODIFIER;
	float Elb_lim = hexCharToDecimal(tab_reg[29])*I_PU / SMALL_MODIFIER;
	float EVa_ref_fixed_init = hexCharToDecimal(tab_reg[32])*V_PU / SMALL_MODIFIER
	float EVa_ref_fixed_pet_init = hexCharToDecimal(tab_reg[33]) * 100 / SMALL_MODIFIER / 2;
	Charge_settings_array[0] = EV_absorp;
	Charge_settings_array[1] = EV_float;
	Charge_settings_array[2] = Et_absorp;
	Charge_settings_array[3] = Et_absorp_ext;
	Charge_settings_array[4] = EV_absorp_ext;
	Charge_settings_array[5] = EV_float_cancel;
	Charge_settings_array[6] = Et_float_exit_cum;
	Charge_settings_array[7] = EV_eq;
	Charge_settings_array[8] = Et_eqcalendar;
	Charge_settings_array[9] = Et_eq_above;
	Charge_settings_array[10] = Et_eq_reg;
	Charge_settings_array[11] = Et_battery_service;
	Charge_settings_array[12] = EV_tempcomp;
	Charge_settings_array[13] = EV_hvd;
	Charge_settings_array[14] = EV_hvr;
	Charge_settings_array[15] = Evb_ref_lim;
	Charge_settings_array[16] = ETb_max;
	Charge_settings_array[17] = ETb_min;
	Charge_settings_array[18] = EV_soc_g_gy;
	Charge_settings_array[19] = EV_soc_gy_y;
	Charge_settings_array[20] = EV_soc_y_yr;
	Charge_settings_array[21] = EV_soc_yr_r;
	Charge_settings_array[22] = Elb_lim;
	Charge_settings_array[23] = EVa_ref_fixed_init;
	Charge_settings_array[24] = EVa_ref_fixed_pet_init;
}

// UPDATES ALL ARRAYS TO THEIR CURRENT VALUES.
Morningstar::Update() {
	Scaling();
	ADCData();
	TemperatureData();
	StatusData();
	ChargerData();
	MPPTData();
	LoggerData();
	ChargeSettings();
}

// Writes the contents of the array to a JSON file.

void Morningstar::DumpToJSON(char *outfile) {
	// main JSON file we will export.
	json j;
	// Put all ADC data into a JSON object.
	json ADC;
	ADC['battery voltage'] = ADC_values_array[0];
	ADC['battery terminal voltage']= ADC_values_array[1];
	ADC['battery sense voltage'] = ADC_values_array[2];
	ADC['array voltage']= ADC_values_array[3];
	ADC['battery current'] = ADC_values_array[4];
	ADC['array current']= ADC_values_array[5];
	ADC['12V supply'] = ADC_values_array[6];
	ADC['3V supply'] = ADC_values_array[7];
	ADC['meterbus voltage']= ADC_values_array[8];
	ADC['1.8V supply'] = ADC_values_array[9];
	ADC['reference voltage']= ADC_values_array[10];
	// Put the ADC JSON object into the main JSON file.
	j['ADC'] = ADC;
	
	// Put all data into a JSON object, then dump it into the main JSON file.
	json Temp;
	Temp['heatsink temperature'] = Temperature_values_array[0];
	Temp['RTS temperature'] = Temperature_values_array[1];
	Temp['battery regulation temperature'] =Temperature_values_array[2];
	j['Temperature'] = Temp;
	
	// Put all data into a JSON object, then dump it into the main JSON file.
	json Status;
	Status['battery_voltage'] = Status_values_array[0];
	Status['charging_current'] = Status_values_array[1];
	Status['minimum battery voltage'] = Status_values_array[2];
	Status['maximum battery voltage'] = Status_values_array[3];
	Status['hourmeter']  = Status_values_array[4];
	Status['faults'] = Status_values_array[5];
	Status['alarms'] = Status_values_array[6];
	Status['flags'] = Status_values_array[7];
	Status['DIP switch status'] = Status_values_array[8];
	Status['LED state'] = Status_values_array[9];
	j['Status'] = Status;
	
	// Put all data into a JSON object, then dump it into the main JSON file.
	json Charger;
	Charger['Charge State'] = Charger_values_array[0];
	Charger['target regulation voltage'] = Charger_values_array[0];
	Charger['Ah Charge Resettable'] =  Charger_values_array[0];
	Charger['Ah Charge Total'] = Charger_values_array[0];
	Charger['kWhr Charge Resettable'] = Charger_values_array[0];
	Charger['kWhr Charge Total'] = Charger_values_array[0];
	j['Charger'] = Charger;
	
	// Put all data into a JSON object, then dump it into the main JSON file.
	json MPPT;
	MPPT['output power'] = MPPT_values_array[0];
	MPPT['input power'] = MPPT_values_array[1];
	MPPT['max power of last sweep'] =MPPT_values_array[2];
	MPPT['Vmp of last sweep'] = MPPT_values_array[3];
	MPPT['Voc of last sweep'] = MPPT_values_array[4];
	j['MPPT'] = MPPT;
	
	// Put all data into a JSON object, then dump it into the main JSON file.
	json Logger;
	Logger['Battery Voltage Minimum Daily'] = Logger_values_array[0];
	Logger['Battery Voltage Maximum Daily'] = Logger_values_array[1];
	Logger['Input Voltage Maximum Daily'] = Logger_values_array[2];
	Logger['Amp Hours accumulated daily'] = Logger_values_array[3];
	Logger['Watt Hours accumulated daily'] = Logger_values_array[4];
	Logger['Maximum power output daily'] = Logger_values_array[5];
	Logger['Minimum temperature daily'] = Logger_values_array[6];
	Logger['Maximum temperature daily'] = Logger_values_array[7];
	Logger['time_ab_daily'] = Logger_values_array[8];
	Logger['time_eq_daily'] = Logger_values_array[9];
	Logger['time_fl_daily'] = Logger_values_array[10];
	Logger['daily alarms'] = Logger_values_array[11];
	Logger['daily flags'] = Logger_values_array[12];
	Logger['daily faults'] = Logger_values_array[13];
	j['Daily Logger Values'] = Logger;
	
	// Put all data into a JSON object, then dump it into the main JSON file.
	json Charger_settings;
	Charger_settings['EV_absorp'] = Charge_settings_array[0];
	Charger_settings['EV_float'] = Charge_settings_array[1];
	Charger_settings['Et_absorp'] = Charge_settings_array[2];
	Charger_settings['Et_absorp_ext'] = Charge_settings_array[3];
	Charger_settings['EV_absorp_ext'] = Charge_settings_array[4];
	Charger_settings['EV_float_cancel'] = Charge_settings_array[5];
	Charger_settings['Et_float_exit_cum'] =Charge_settings_array[6];
	Charger_settings['EV_eq'] = Charge_settings_array[7];
	Charger_settings['Et_eqcalendar'] = Charge_settings_array[8];
	Charger_settings['Et_eq_above'] = Charge_settings_array[9];
	Charger_settings['Et_eq_reg'] = Charge_settings_array[10];
	Charger_settings['Et_battery_service'] = Charge_settings_array[11];
	Charger_settings['EV_tempcomp'] = Charge_settings_array[12];
	Charger_settings['EV_hvd'] = Charge_settings_array[13];
	Charger_settings['EV_hvr'] =Charge_settings_array[14];
	Charger_settings['Evb_ref_lim'] = Charge_settings_array[15];
	Charger_settings['ETb_max'] = Charge_settings_array[16];
	Charger_settings['ETb_min'] = Charge_settings_array[17];
	Charger_settings['EV_soc_g_gy'] = Charge_settings_array[18];
	Charger_settings['EV_soc_gy_y'] = Charge_settings_array[19];
	Charger_settings['EV_soc_y_yr'] = Charge_settings_array[20];
	Charger_settings['EV_soc_yr_r'] = Charge_settings_array[21];
	Charger_settings['Elb_lim'] = Charge_settings_array[22];
	Charger_settings['EVa_ref_fixed_init'] = Charge_settings_array[23];
	Charger_settings['EVa_ref_fixed_pet_init'] = Charge_settings_array[24];
	j['Charger Settings'] = Charger_settings;
	
	ofstream myfile(outfile);
	myfile << j;
	myfile.close();
}
// HELPER FUNCTIONS
uint16_t hexCharToDecimal(uint16_t x) {
	char a = (char) (x & 0xF);
	char b = (char) ((x >> 4) & 0xF);
	char c = (char) ((x >> 8) & 0xF);
	char d = (char) ((x >> 12) & 0xF);
	uint16_t sum = hex2int(a) + (hex2int(b) << 4) + (hex2int(c) << 8) + (hex2int(d) << 12);
	return sum;
}

uint16_t hex2int(char Z) {
	switch(Z) {
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
			return (uint8_t) (Z - '0');
			break;
		case 'a':
		case 'A':
			return 10;
			break;
		case 'b':
		case 'B':
			return 11;
			break;
		case 'c':
		case 'C':
			return 12;
			break;
		case 'd':
		case 'D':
			return 13;
			break;
		case 'e':
		case 'E':
			return 14;
			break;
		case 'f':
		case 'F':
			return 15;
			break;
		default: 
			return 0;
			break;
	}
}
