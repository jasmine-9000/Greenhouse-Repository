EESchema Schematic File Version 4
LIBS:Solar_Panels_and_Charge_Controller-cache
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 3 5
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Entry Wire Line
	9850 950  9950 1050
Entry Wire Line
	9850 1050 9950 1150
Entry Wire Line
	9850 1150 9950 1250
Entry Wire Line
	9850 1250 9950 1350
Entry Wire Line
	9850 1700 9950 1800
Entry Wire Line
	9850 1800 9950 1900
Entry Wire Line
	9850 1900 9950 2000
Entry Wire Line
	9850 2000 9950 2100
Entry Wire Line
	9850 2350 9950 2450
Entry Wire Line
	9850 2450 9950 2550
Entry Wire Line
	9850 2550 9950 2650
Entry Wire Line
	9850 2650 9950 2750
Text GLabel 9950 2300 2    50   Input ~ 0
TSMPPT_2_USB_BUS
Text GLabel 9950 2950 2    50   Input ~ 0
TSMPPT_1_USB_BUS
Text GLabel 9950 1450 2    50   Input ~ 0
BMS_USB_connection
$Comp
L raspberry_pi:raspberry_pi_3B+ R_Pi1
U 1 1 5DBA7A9A
P 9450 1350
F 0 "R_Pi1" H 8675 2015 50  0000 C CNN
F 1 "raspberry_pi_3B+" H 8675 1924 50  0000 C CNN
F 2 "" H 8750 1850 50  0001 C CNN
F 3 "" H 8750 1850 50  0001 C CNN
	1    9450 1350
	1    0    0    -1  
$EndComp
$Comp
L raspberry_pi:i2c_shield SHIELD1
U 1 1 5D31AE39
P 2950 2350
F 0 "SHIELD1" V 3800 2400 50  0000 L CNN
F 1 "i2c_shield" V 3700 2350 50  0000 L CNN
F 2 "" H 2950 2350 50  0001 C CNN
F 3 "" H 2950 2350 50  0001 C CNN
	1    2950 2350
	0    1    1    0   
$EndComp
Entry Wire Line
	7000 1600 7100 1500
Entry Wire Line
	7000 1800 7100 1700
Entry Wire Line
	7000 1900 7100 1800
Entry Wire Line
	3600 2350 3700 2450
Entry Wire Line
	3600 2250 3700 2350
Entry Wire Line
	3600 2450 3700 2550
Entry Wire Line
	3600 2550 3700 2650
Wire Wire Line
	3450 2250 3600 2250
Wire Wire Line
	3450 2350 3600 2350
Wire Wire Line
	3450 2450 3600 2450
Wire Wire Line
	3450 2550 3600 2550
Text GLabel 3700 2700 3    50   Input ~ 0
Master_I2C_Bus
Text GLabel 7000 1950 3    50   Input ~ 0
Master_I2C_Bus
$Comp
L raspberry_pi:12Vto5V_converter U6
U 1 1 5D32C6C3
P 6500 1150
F 0 "U6" H 6475 1615 50  0000 C CNN
F 1 "12Vto5V_converter" H 6475 1524 50  0000 C CNN
F 2 "" H 6500 1150 50  0001 C CNN
F 3 "" H 6500 1150 50  0001 C CNN
	1    6500 1150
	1    0    0    -1  
$EndComp
Wire Wire Line
	7000 1150 7150 1150
Wire Wire Line
	7150 1150 7150 1100
Wire Wire Line
	7150 1100 7500 1100
Wire Wire Line
	7000 950  7150 950 
Wire Wire Line
	7150 950  7150 1000
Wire Wire Line
	7150 1000 7500 1000
Wire Wire Line
	5950 950  5400 950 
Wire Wire Line
	5950 1150 5400 1150
$Comp
L Sensor_Humidity:HDC1080 SENSOR1
U 1 1 5D3494AA
P 1900 1500
F 0 "SENSOR1" H 1557 1546 50  0000 R CNN
F 1 "HDC1080" H 1557 1455 50  0000 R CNN
F 2 "Package_SON:Texas_PWSON-N6" H 1850 1250 50  0001 L CNN
F 3 "http://www.ti.com/lit/ds/symlink/hdc1080.pdf" H 1500 1750 50  0001 C CNN
	1    1900 1500
	1    0    0    -1  
$EndComp
Wire Wire Line
	1800 1200 2400 1200
Wire Wire Line
	2200 1400 2400 1400
Wire Wire Line
	2200 1500 2400 1500
Wire Wire Line
	1800 1800 2250 1800
Wire Wire Line
	2250 1800 2250 1300
Wire Wire Line
	2250 1300 2400 1300
Text Notes 1100 1100 0    50   ~ 0
Temperature and Humidity Sensor\n
$Comp
L raspberry_pi:VEML7700 SENSOR2
U 1 1 5D357FB1
P 1400 2300
F 0 "SENSOR2" H 1728 2263 50  0000 L CNN
F 1 "VEML7700" H 1728 2172 50  0000 L CNN
F 2 "" H 1800 2500 50  0001 C CNN
F 3 "https://www.vishay.com/docs/84286/veml7700.pdf" H 1800 2500 50  0001 C CNN
	1    1400 2300
	1    0    0    -1  
$EndComp
Text Notes 1150 2000 0    50   ~ 0
Light Sensor\n
Wire Wire Line
	1800 2650 2400 2650
Wire Wire Line
	1500 2650 1500 2750
Wire Wire Line
	1500 2750 2400 2750
Wire Wire Line
	1650 2650 1650 2950
Wire Wire Line
	1650 2950 2400 2950
Wire Wire Line
	1800 2650 1800 3050
Wire Wire Line
	1200 2650 1200 2850
Wire Wire Line
	1200 2850 2400 2850
Wire Wire Line
	1350 2650 1350 3050
Wire Wire Line
	1350 3050 1800 3050
$Comp
L raspberry_pi:VEML7700 SENSOR3
U 1 1 5D361415
P 950 3200
F 0 "SENSOR3" H 1278 3163 50  0000 L CNN
F 1 "VEML7700" H 1278 3072 50  0000 L CNN
F 2 "" H 1350 3400 50  0001 C CNN
F 3 "https://www.vishay.com/docs/84286/veml7700.pdf" H 1350 3400 50  0001 C CNN
	1    950  3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	1050 3550 1050 3650
Wire Wire Line
	1200 3550 1200 3850
Wire Wire Line
	1350 3550 1350 3950
Wire Wire Line
	750  3550 750  3750
Wire Wire Line
	900  3550 900  3950
Wire Wire Line
	900  3950 1350 3950
Wire Wire Line
	1350 3550 2400 3550
Wire Wire Line
	1050 3650 2400 3650
Wire Wire Line
	750  3750 2400 3750
Wire Wire Line
	1200 3850 2400 3850
Text Notes 1200 800  0    50   ~ 0
I2C sensor node shield\n\nHas Pull-up resistors contained inside\n
Text GLabel 5400 950  0    50   Input ~ 0
LOAD_POSITIVE_TERMINAL
Text GLabel 5400 1150 0    50   Input ~ 0
LOAD_GROUND
Text Notes 600  2950 0    50   ~ 0
Light Sensor\n
Entry Wire Line
	7000 1400 7100 1300
Wire Wire Line
	7100 1300 7500 1300
Wire Wire Line
	7500 2200 7350 2200
Wire Wire Line
	7350 2000 7500 2000
Entry Wire Line
	7350 3100 7250 3200
Wire Wire Line
	7500 3100 7350 3100
Entry Wire Line
	7250 2300 7350 2200
Entry Wire Line
	7250 2100 7350 2000
Entry Wire Line
	7250 1500 7350 1400
Wire Wire Line
	7500 1400 7350 1400
Wire Wire Line
	7500 1600 7350 1600
Entry Wire Line
	7250 1600 7350 1500
Entry Wire Line
	7250 1700 7350 1600
Entry Wire Line
	7250 1900 7350 1800
Wire Wire Line
	7500 2600 7350 2600
Wire Wire Line
	7500 2500 7350 2500
Entry Wire Line
	7250 2600 7350 2500
Entry Wire Line
	7250 2700 7350 2600
Entry Wire Line
	7350 3700 7250 3800
Wire Wire Line
	7500 3700 7350 3700
Entry Wire Line
	7350 4300 7250 4400
Wire Wire Line
	7500 4300 7350 4300
Entry Wire Line
	7350 4200 7250 4300
Wire Wire Line
	7500 4200 7350 4200
Entry Wire Line
	7350 4600 7250 4700
Wire Wire Line
	7500 4600 7350 4600
Entry Wire Line
	7350 5200 7250 5300
Wire Wire Line
	7500 5200 7350 5200
Text Label 7250 4800 1    50   ~ 0
GSM_GPRS_BUS
$Comp
L sixfab:gsm_gprs_shield GSM1
U 1 1 5D39EE43
P 6400 6100
F 0 "GSM1" H 5862 6054 50  0000 R CNN
F 1 "gsm_gprs_shield" H 5862 6145 50  0000 R CNN
F 2 "" H 6050 6400 50  0001 C CNN
F 3 "" H 6050 6400 50  0001 C CNN
	1    6400 6100
	-1   0    0    1   
$EndComp
Entry Wire Line
	6650 5600 6750 5500
Entry Wire Line
	6850 5600 6950 5500
Entry Wire Line
	6750 5600 6850 5500
Entry Wire Line
	6350 5600 6450 5500
Entry Wire Line
	6550 5600 6650 5500
Entry Wire Line
	6450 5600 6550 5500
Entry Wire Line
	6050 5600 6150 5500
Entry Wire Line
	6250 5600 6350 5500
Entry Wire Line
	6150 5600 6250 5500
Entry Wire Line
	5750 5600 5850 5500
Entry Wire Line
	5950 5600 6050 5500
Entry Wire Line
	5850 5600 5950 5500
Entry Wire Line
	5650 5600 5750 5500
Entry Wire Line
	5550 5600 5650 5500
$Comp
L Connector:SIM_Card J1
U 1 1 5D3B94F3
P 6450 7200
F 0 "J1" V 6450 6800 50  0000 L CNN
F 1 "SIM_Card" V 6550 6550 50  0000 L CNN
F 2 "" H 6450 7550 50  0001 C CNN
F 3 " ~" H 6400 7200 50  0001 C CNN
	1    6450 7200
	0    1    1    0   
$EndComp
Wire Wire Line
	6750 6700 6750 6650
Wire Wire Line
	6750 6650 6650 6550
Wire Wire Line
	6650 6700 6650 6650
Wire Wire Line
	6650 6650 6750 6550
Wire Wire Line
	6550 6700 6550 6550
Wire Wire Line
	6250 6700 6250 6600
Wire Wire Line
	6250 6600 6450 6550
Wire Wire Line
	6350 6700 6350 6650
Wire Wire Line
	6350 6650 6650 6550
Connection ~ 6650 6550
Wire Wire Line
	6450 6700 6350 6600
Wire Wire Line
	6350 6600 6350 6550
NoConn ~ 2950 4200
NoConn ~ 3050 4200
NoConn ~ 3150 4200
NoConn ~ 3250 4200
NoConn ~ 2400 3400
NoConn ~ 2400 3300
NoConn ~ 2400 3200
NoConn ~ 2400 3100
NoConn ~ 2400 2500
NoConn ~ 2400 2400
NoConn ~ 2400 2300
NoConn ~ 2400 2200
NoConn ~ 2400 2050
NoConn ~ 2400 1950
NoConn ~ 2400 1800
NoConn ~ 2400 1700
NoConn ~ 2950 1000
NoConn ~ 3050 1000
NoConn ~ 3150 1000
NoConn ~ 3250 1000
Text Notes 6700 700  0    50   ~ 0
Micro USB power out\n
Entry Wire Line
	9850 2950 9950 3050
Entry Wire Line
	9850 3050 9950 3150
Entry Wire Line
	9850 3150 9950 3250
Entry Wire Line
	9850 3250 9950 3350
Text GLabel 9950 3550 2    50   Input ~ 0
SURESINE_INVERTER_USB_BUS
Text Notes 6150 6650 2    50   ~ 0
Antenna is built-in to the PCB\n
Text Notes 9200 7500 2    50   ~ 0
Raspberry Pi, I2C shield, and GSM/GPRS shield
Text Notes 10700 7650 2    50   ~ 0
1.3
Text Notes 8550 7650 2    50   ~ 0
7/31/2019
$Comp
L Device:Antenna AE1
U 1 1 5DB5BD1B
P 5000 5750
F 0 "AE1" H 5080 5739 50  0000 L CNN
F 1 "Antenna" H 5080 5648 50  0000 L CNN
F 2 "" H 5000 5750 50  0001 C CNN
F 3 "~" H 5000 5750 50  0001 C CNN
	1    5000 5750
	1    0    0    -1  
$EndComp
Wire Wire Line
	7100 1800 7500 1800
Wire Wire Line
	6850 5650 6850 5600
Wire Wire Line
	6750 5650 6750 5600
Wire Wire Line
	6650 5600 6650 5650
Wire Wire Line
	6550 5650 6550 5600
Wire Wire Line
	6350 5650 6350 5600
Wire Wire Line
	6250 5600 6250 5650
Wire Wire Line
	6150 5650 6150 5600
Wire Wire Line
	5950 5600 5950 5650
Wire Wire Line
	5850 5650 5850 5600
Wire Wire Line
	5750 5650 5750 5600
Wire Wire Line
	5650 5650 5650 5600
Wire Wire Line
	5550 5650 5550 5600
Wire Wire Line
	7100 1700 7500 1700
Wire Wire Line
	7100 1500 7500 1500
Wire Bus Line
	3700 2350 3700 2700
Wire Bus Line
	7000 1400 7000 1950
Wire Bus Line
	9950 2450 9950 2950
Wire Bus Line
	9950 1800 9950 2300
Wire Bus Line
	9950 1050 9950 1450
Wire Bus Line
	9950 3050 9950 3550
Wire Bus Line
	7250 1500 7250 5500
Wire Bus Line
	5650 5500 7250 5500
$EndSCHEMATC
