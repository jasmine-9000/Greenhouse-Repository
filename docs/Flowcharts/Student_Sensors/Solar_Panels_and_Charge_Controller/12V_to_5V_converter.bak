EESchema Schematic File Version 4
LIBS:Solar_Panels_and_Charge_Controller-cache
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 4 5
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 850  1050 0    247  ~ 0
Vin+
Text Notes 800  3300 0    247  ~ 0
Vin -\n
Wire Wire Line
	1200 1200 2950 1200
Text Notes 9450 1150 0    247  ~ 0
Vout +
Text Notes 9350 3000 0    247  ~ 0
Vout -
$Comp
L Device:R_US Rsc
U 1 1 5D33235A
P 2950 1350
F 0 "Rsc" H 3018 1396 50  0000 L CNN
F 1 "R_US" H 3018 1305 50  0000 L CNN
F 2 "" V 2990 1340 50  0001 C CNN
F 3 "~" H 2950 1350 50  0001 C CNN
	1    2950 1350
	1    0    0    -1  
$EndComp
$Comp
L Device:CP Cin
U 1 1 5D333025
P 3450 1350
F 0 "Cin" H 3568 1396 50  0000 L CNN
F 1 "CP" H 3568 1305 50  0000 L CNN
F 2 "" H 3488 1200 50  0001 C CNN
F 3 "~" H 3450 1350 50  0001 C CNN
	1    3450 1350
	1    0    0    -1  
$EndComp
Wire Wire Line
	2950 1200 3450 1200
Connection ~ 2950 1200
$Comp
L Regulator_Switching:MC34063AD U7
U 1 1 5D3360EA
P 4250 1400
F 0 "U7" H 4250 1867 50  0000 C CNN
F 1 "MC34063AD" H 4250 1776 50  0000 C CNN
F 2 "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" H 4300 950 50  0001 L CNN
F 3 "http://www.onsemi.com/pub_link/Collateral/MC34063A-D.PDF" H 4750 1300 50  0001 C CNN
	1    4250 1400
	1    0    0    -1  
$EndComp
Connection ~ 3450 1200
Wire Wire Line
	2950 1500 2950 2100
Wire Wire Line
	2950 2100 4750 2100
Wire Wire Line
	4750 2100 4750 1400
Wire Wire Line
	4750 1400 4750 1300
Connection ~ 4750 1400
Wire Wire Line
	4650 1200 4750 1200
Wire Wire Line
	4750 1200 4750 1300
Connection ~ 4750 1300
Wire Wire Line
	3650 1600 3650 1700
$Comp
L Device:CP Ct
U 1 1 5D337BFB
P 3650 1850
F 0 "Ct" H 3768 1896 50  0000 L CNN
F 1 "CP" H 3768 1805 50  0000 L CNN
F 2 "" H 3688 1700 50  0001 C CNN
F 3 "~" H 3650 1850 50  0001 C CNN
	1    3650 1850
	1    0    0    -1  
$EndComp
Wire Wire Line
	3450 1500 3450 2700
Wire Wire Line
	1150 2700 3450 2700
Wire Wire Line
	3650 2000 3650 2700
Wire Wire Line
	3650 2700 3450 2700
Connection ~ 3450 2700
Wire Wire Line
	3650 2700 4250 2700
Connection ~ 3650 2700
Wire Wire Line
	4750 1400 4650 1400
Wire Wire Line
	4750 1300 4650 1300
Wire Wire Line
	3650 1600 3850 1600
Wire Wire Line
	3450 1200 3850 1200
Wire Wire Line
	4650 1600 4900 1600
$Comp
L Device:R_US R1
U 1 1 5D339FAE
P 4900 1750
F 0 "R1" H 4968 1796 50  0000 L CNN
F 1 "R_US" H 4968 1705 50  0000 L CNN
F 2 "" V 4940 1740 50  0001 C CNN
F 3 "~" H 4900 1750 50  0001 C CNN
	1    4900 1750
	1    0    0    -1  
$EndComp
Wire Wire Line
	4250 1900 4250 2700
Connection ~ 4250 2700
Wire Wire Line
	4250 2700 4900 2700
Wire Wire Line
	4900 1900 4900 2700
Connection ~ 4900 2700
Wire Wire Line
	4900 2700 5650 2700
Wire Wire Line
	4900 1600 5150 1600
Connection ~ 4900 1600
Wire Wire Line
	5450 1600 5650 1600
Wire Wire Line
	5650 1600 5650 1750
$Comp
L Device:CP Cout
U 1 1 5D33B917
P 6250 1850
F 0 "Cout" H 6368 1896 50  0000 L CNN
F 1 "CP" H 6368 1805 50  0000 L CNN
F 2 "" H 6288 1700 50  0001 C CNN
F 3 "~" H 6250 1850 50  0001 C CNN
	1    6250 1850
	1    0    0    -1  
$EndComp
$Comp
L Device:L L
U 1 1 5D33C1E7
P 5650 1900
F 0 "L" H 5703 1946 50  0000 L CNN
F 1 "L" H 5703 1855 50  0000 L CNN
F 2 "" H 5650 1900 50  0001 C CNN
F 3 "~" H 5650 1900 50  0001 C CNN
	1    5650 1900
	1    0    0    -1  
$EndComp
$Comp
L Diode:1N5819 D1
U 1 1 5D33C811
P 5650 2350
F 0 "D1" V 5604 2429 50  0000 L CNN
F 1 "1N5819" V 5695 2429 50  0000 L CNN
F 2 "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal" H 5650 2175 50  0001 C CNN
F 3 "http://www.vishay.com/docs/88525/1n5817.pdf" H 5650 2350 50  0001 C CNN
	1    5650 2350
	0    1    1    0   
$EndComp
Wire Wire Line
	4650 1700 4650 2200
Wire Wire Line
	4650 2200 5650 2200
Wire Wire Line
	5650 2050 5650 2200
Connection ~ 5650 2200
Wire Wire Line
	5650 2500 5650 2700
Connection ~ 5650 2700
Wire Wire Line
	5650 2700 6250 2700
Wire Wire Line
	5650 1600 6250 1600
Wire Wire Line
	6250 1600 6250 1700
Connection ~ 5650 1600
Wire Wire Line
	6250 2000 6250 2700
Connection ~ 6250 2700
Wire Wire Line
	6250 2700 10650 2700
Connection ~ 6250 1600
Wire Wire Line
	6250 1200 10650 1200
Wire Wire Line
	6250 1200 6250 1600
Text Notes 1050 4500 0    90   ~ 0
Source:\n\nhttps://circuitdigest.com/electronic-circuits/12v-to-5v-buck-converter-circuit-diagram
$Comp
L Device:R_US R2
U 1 1 5D33AB53
P 5300 1600
F 0 "R2" V 5095 1600 50  0000 C CNN
F 1 "R_US" V 5186 1600 50  0000 C CNN
F 2 "" V 5340 1590 50  0001 C CNN
F 3 "~" H 5300 1600 50  0001 C CNN
	1    5300 1600
	0    1    1    0   
$EndComp
$EndSCHEMATC
