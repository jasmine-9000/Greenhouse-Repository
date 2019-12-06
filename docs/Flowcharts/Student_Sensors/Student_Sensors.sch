EESchema Schematic File Version 4
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
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
L Sensor_Temperature:DS18B20 U1
U 1 1 5D223712
P 4200 2800
F 0 "U1" H 3970 2846 50  0000 R CNN
F 1 "DS18B20" H 3970 2755 50  0000 R CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 3200 2550 50  0001 C CNN
F 3 "http://datasheets.maximintegrated.com/en/ds/DS18B20.pdf" H 4050 3050 50  0001 C CNN
	1    4200 2800
	1    0    0    -1  
$EndComp
$Comp
L Sensor:DHT11 U2
U 1 1 5D2240D5
P 5950 2900
F 0 "U2" H 5706 2946 50  0000 R CNN
F 1 "DHT11" H 5706 2855 50  0000 R CNN
F 2 "Sensor:Aosong_DHT11_5.5x12.0_P2.54mm" H 5950 2500 50  0001 C CNN
F 3 "http://akizukidenshi.com/download/ds/aosong/DHT11.pdf" H 6100 3150 50  0001 C CNN
	1    5950 2900
	1    0    0    -1  
$EndComp
$EndSCHEMATC
