EESchema Schematic File Version 4
LIBS:Solar_Panels_and_Charge_Controller-cache
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 5 5
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L raspberry_pi:raspberry_pi_zero_w R_Pi2
U 1 1 5D3E28DB
P 8600 1400
F 0 "R_Pi2" H 8675 2115 50  0000 C CNN
F 1 "raspberry_pi_zero_w" H 8675 2024 50  0000 C CNN
F 2 "" H 8600 1400 50  0001 C CNN
F 3 "" H 8600 1400 50  0001 C CNN
	1    8600 1400
	1    0    0    -1  
$EndComp
$Comp
L raspberry_pi:12Vto5V_converter U?
U 1 1 5D3E6F98
P 6400 1150
F 0 "U?" H 6375 1615 50  0000 C CNN
F 1 "12Vto5V_converter" H 6375 1524 50  0000 C CNN
F 2 "" H 6400 1150 50  0001 C CNN
F 3 "" H 6400 1150 50  0001 C CNN
	1    6400 1150
	1    0    0    -1  
$EndComp
Wire Wire Line
	7350 950  7350 1000
Wire Wire Line
	7350 1000 7500 1000
Wire Wire Line
	7350 1150 7350 1100
Wire Wire Line
	7350 1100 7500 1100
Wire Wire Line
	5850 950  5600 950 
Wire Wire Line
	5850 1150 5600 1150
Text GLabel 5600 950  0    50   Input ~ 0
LOAD_POSITIVE_TERMINAL
Text GLabel 5600 1150 0    50   Input ~ 0
LOAD_GROUND
$Comp
L raspberry_pi:i2c_shield SHIELD2
U 1 1 5D3E825B
P 6000 2950
F 0 "SHIELD2" V 6350 3400 50  0000 L CNN
F 1 "i2c_shield" V 6450 3400 50  0000 L CNN
F 2 "" H 6000 2950 50  0001 C CNN
F 3 "" H 6000 2950 50  0001 C CNN
	1    6000 2950
	0    1    1    0   
$EndComp
Wire Wire Line
	6500 3150 6850 3150
Wire Wire Line
	6500 3050 7000 3050
Wire Wire Line
	7000 3050 7000 1800
Wire Wire Line
	7000 1800 7500 1800
Wire Wire Line
	6500 2950 7100 2950
Wire Wire Line
	7100 2950 7100 1700
Wire Wire Line
	7100 1700 7500 1700
Wire Wire Line
	6500 2850 7250 2850
Wire Wire Line
	7250 2850 7250 1500
Wire Wire Line
	7250 1500 7500 1500
Wire Wire Line
	6850 1300 6850 3150
Wire Wire Line
	6850 1300 7500 1300
Wire Wire Line
	6900 1150 7350 1150
Wire Wire Line
	6900 950  7350 950 
Text Notes 8750 7500 2    50   ~ 0
Student Sensors and Microcontroller
Text Notes 8550 7650 2    50   ~ 0
7/26/2019
Text Notes 10700 7650 2    50   ~ 0
1.2
$EndSCHEMATC
