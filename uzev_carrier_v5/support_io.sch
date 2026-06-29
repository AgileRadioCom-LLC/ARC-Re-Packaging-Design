EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 5 5
Title "Sheet 4: Support I/O"
Date "2026-03-19"
Rev "1.0"
Comp "ADRV9009 + UltraZed-EV Carrier Board"
Comment1 "Step 8E: Support I/O - I2C, UART, Reset, JTAG Isolation"
Comment2 "Defense-grade hardening: JTAG/UART isolation via DNP resistors"
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 1000 800  0    100  ~ 0
SHEET 4: SUPPORT I/O
Text Notes 950  1650 0    60   ~ 0
========== 1. CARRIER CARD I2C BUS ==========
Text Notes 950  1950 0    35   ~ 0
CC_SCL (JX3.A1), CC_SDA (JX3.C1) — Channel 0 of SOM PCA9543A I2C mux
Text Notes 950  2150 0    35   ~ 0
Pull up to VCCO_HP_65 (1.8V). SOM operates I2C at 1.8V via Bank 503.
Text GLabel 1500 2900 0    40   BiDi ~ 0
CC_SCL
$Comp
L Device:R R1
U 1 1 8C000001
P 2200 2600
F 0 "R1" H 2250 2500 40  0000 L CNN
F 1 "2.2k" H 2250 2700 40  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H 2200 2800 40  0001 C CNN
F 3 "" H 2200 2600 40  0001 C CNN
	1    2200 2600
	1    0    0    -1  
$EndComp
Text GLabel 2200 2300 2    40   Input ~ 0
VCCO_HP_65
Wire Wire Line
	1900 2900 2200 2900
Wire Wire Line
	2200 2900 2200 2800
Text GLabel 1500 3400 0    40   BiDi ~ 0
CC_SDA
$Comp
L Device:R R2
U 1 1 8C000002
P 2200 3100
F 0 "R2" H 2250 3000 40  0000 L CNN
F 1 "2.2k" H 2250 3200 40  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H 2200 3300 40  0001 C CNN
F 3 "" H 2200 3100 40  0001 C CNN
	1    2200 3100
	1    0    0    -1  
$EndComp
Text GLabel 2200 3300 2    40   Input ~ 0
VCCO_HP_65
Wire Wire Line
	1900 3400 2200 3400
Wire Wire Line
	2200 3400 2200 3300
Text GLabel 1500 3900 0    40   BiDi ~ 0
CC_INT_N
$Comp
L Device:R R3
U 1 1 8C000003
P 2200 3600
F 0 "R3" H 2250 3500 40  0000 L CNN
F 1 "10k" H 2250 3700 40  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H 2200 3800 40  0001 C CNN
F 3 "" H 2200 3600 40  0001 C CNN
	1    2200 3600
	1    0    0    -1  
$EndComp
Text GLabel 2200 3300 2    40   Input ~ 0
VCCO_HP_65
Wire Wire Line
	1900 3900 2200 3900
Wire Wire Line
	2200 3900 2200 3800
Text Notes 1000 5500 0    60   ~ 0
========== 2. UART DEBUG HEADER ==========
Text Notes 1000 5800 0    35   ~ 0
PS UART on MIO pair from JX3. Use MIO_26 (TX) / MIO_27 (RX) for UART0.
Text Notes 1000 6000 0    35   ~ 0
1.8V LVCMOS levels. Use FTDI FT232R or 1.8V-compatible USB-UART adapter.
Text Notes 1000 6200 0    35   ~ 0
UART isolation: 0-ohm DNP resistors (R4, R5) for deployed units.
$Comp
L Connector:Conn_01x04_Male J6
U 1 1 8C000004
P 4500 6600
F 0 "J6" H 4400 6500 40  0000 L CNN
F 1 "UART_HDR" H 4750 6700 40  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 4500 6800 40  0001 C CNN
F 3 "" H 4500 6600 40  0001 C CNN
	1    4500 6600
	1    0    0    -1  
$EndComp
Text GLabel 1500 6400 0    40   Output ~ 0
MIO_26
$Comp
L Device:R R4
U 1 1 8C000005
P 2500 6400
F 0 "R4" H 2550 6300 40  0000 L CNN
F 1 "0R_DNP" H 2550 6500 40  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H 2500 6600 40  0001 C CNN
F 3 "" H 2500 6400 40  0001 C CNN
	1    2500 6400
	1    0    0    -1  
$EndComp
Text Notes 3200 6420 0    30   ~ 0
TX
Wire Wire Line
	1900 6400 2300 6400
Wire Wire Line
	2700 6400 4100 6400
Text GLabel 1500 6700 0    40   Input ~ 0
MIO_27
$Comp
L Device:R R5
U 1 1 8C000006
P 2500 6700
F 0 "R5" H 2550 6600 40  0000 L CNN
F 1 "0R_DNP" H 2550 6800 40  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H 2500 6900 40  0001 C CNN
F 3 "" H 2500 6700 40  0001 C CNN
	1    2500 6700
	1    0    0    -1  
$EndComp
Text Notes 3200 6720 0    30   ~ 0
RX
Wire Wire Line
	1900 6700 2300 6700
Wire Wire Line
	2700 6700 4100 6700
$Comp
L power:GND #PWR0101
U 1 1 8C000007
P 4500 7200
F 0 "#PWR0101" H 4500 7250 50  0001 C CNN
F 1 "GND" H 4500 7350 40  0000 C CNN
F 2 "" H 4500 7200 50  0001 C CNN
F 3 "" H 4500 7200 50  0001 C CNN
	1    4500 7200
	1    0    0    -1  
$EndComp
Wire Wire Line
	4500 7200 4500 6800
Wire Wire Line
	4500 6800 4700 6800
Text GLabel 4900 7000 2    40   Input ~ 0
VCCO_HP_65
Text Notes 8450 900  0    60   ~ 0
========== 3. RESET AND POWER-GOOD ==========
Text Notes 8450 1200 0    35   ~ 0
SOM_RESET_IN_N (JX1.A2): Active-low, 10k pullup to VCCO_PSIO on SOM.
Text Notes 8450 1400 0    35   ~ 0
Add pushbutton to GND for manual reset. SOM pullup exists on-board.
Text GLabel 9000 2100 0    40   Output ~ 0
SOM_RESET_IN_N
$Comp
L Device:R R10
U 1 1 8C000008
P 9700 1800
F 0 "R10" H 9750 1700 40  0000 L CNN
F 1 "10k" H 9750 1900 40  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H 9700 2000 40  0001 C CNN
F 3 "" H 9700 1800 40  0001 C CNN
	1    9700 1800
	1    0    0    -1  
$EndComp
Text GLabel 9700 1500 2    40   Input ~ 0
VCCO_HP_65
Wire Wire Line
	9400 2100 9700 2100
Wire Wire Line
	9700 2100 9700 2000
$Comp
L Switch:SW_Push SW1
U 1 1 8C000009
P 10300 2100
F 0 "SW1" H 10350 2000 40  0000 L CNN
F 1 "RESET" H 10350 2200 40  0000 L CNN
F 2 "Button_Switch_SMD:SW_SPST_CK_RS282G05A3" H 10300 2300 40  0001 C CNN
F 3 "" H 10300 2100 40  0001 C CNN
	1    10300 2100
	1    0    0    -1  
$EndComp
Wire Wire Line
	9700 2100 10100 2100
$Comp
L power:GND #PWR000A01
U 1 1 8C00000A
P 10500 2400
F 0 "#PWR000A01" H 10500 2450 50  0001 C CNN
F 1 "GND" H 10500 2550 40  0000 C CNN
F 2 "" H 10500 2400 50  0001 C CNN
F 3 "" H 10500 2400 50  0001 C CNN
	1    10500 2400
	1    0    0    -1  
$EndComp
Text Notes 8500 2900 0    35   ~ 0
SOM_PG_OUT (JX1.D47): Open-drain, 10k pullup to 3.3V on SOM.
Text Notes 8500 3100 0    35   ~ 0
LED ON = SOM power good. Do NOT drive high from carrier.
Text GLabel 9000 3500 0    40   Input ~ 0
SOM_PG_OUT
$Comp
L Device:R R11
U 1 1 8C00000B
P 9700 3500
F 0 "R11" H 9750 3400 40  0000 L CNN
F 1 "1k" H 9750 3600 40  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H 9700 3700 40  0001 C CNN
F 3 "" H 9700 3500 40  0001 C CNN
	1    9700 3500
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D1
U 1 1 8C00000C
P 10300 3500
F 0 "D1" H 10350 3400 40  0000 L CNN
F 1 "GREEN" H 10350 3600 40  0000 L CNN
F 2 "LED_SMD:LED_0603_1608Metric" H 10300 3700 40  0001 C CNN
F 3 "" H 10300 3500 40  0001 C CNN
	1    10300 3500
	1    0    0    -1  
$EndComp
Wire Wire Line
	9400 3500 9500 3500
Wire Wire Line
	9900 3500 10100 3500
$Comp
L power:GND #PWR000D01
U 1 1 8C00000D
P 10500 3800
F 0 "#PWR000D01" H 10500 3850 50  0001 C CNN
F 1 "GND" H 10500 3950 40  0000 C CNN
F 2 "" H 10500 3800 50  0001 C CNN
F 3 "" H 10500 3800 50  0001 C CNN
	1    10500 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	10500 3500 10500 3600
Text Notes 7500 4100 0    35   ~ 0
CC_RESET_OUT_N (JX1.C46): Open-drain from SOM. Pullup needed on carrier.
Text GLabel 9000 4300 0    40   Input ~ 0
CC_RESET_OUT_N
$Comp
L Device:R R12
U 1 1 8C00000E
P 9700 4000
F 0 "R12" H 9750 3900 40  0000 L CNN
F 1 "10k" H 9750 4100 40  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H 9700 4200 40  0001 C CNN
F 3 "" H 9700 4000 40  0001 C CNN
	1    9700 4000
	1    0    0    -1  
$EndComp
Text GLabel 9700 3700 2    40   Input ~ 0
VCCO_HP_65
Wire Wire Line
	9400 4300 9700 4300
Wire Wire Line
	9700 4300 9700 4200
Text Notes 7550 5400 0    60   ~ 0
========== 4. JTAG ISOLATION (Security Hardening) ==========
Text Notes 7550 5700 0    35   ~ 0
0-ohm DNP resistors between JX1 JTAG pins and debug header.
Text Notes 7550 5900 0    35   ~ 0
Populate for development. Remove for deployed units to sever JTAG chain.
$Comp
L Connector:Conn_01x06_Male J7
U 1 1 8C00000F
P 11050 6600
F 0 "J7" H 10950 6500 40  0000 L CNN
F 1 "JTAG_HDR" H 11300 6700 40  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical" H 11050 6800 40  0001 C CNN
F 3 "" H 11050 6600 40  0001 C CNN
	1    11050 6600
	1    0    0    -1  
$EndComp
Text GLabel 8050 6600 0    40   BiDi ~ 0
JTAG_TCK
$Comp
L Device:R R6
U 1 1 8C000010
P 9050 6600
F 0 "R6" H 9100 6500 40  0000 L CNN
F 1 "0R_DNP" H 9100 6700 40  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H 9050 6800 40  0001 C CNN
F 3 "" H 9050 6600 40  0001 C CNN
	1    9050 6600
	0    -1   -1   0   
$EndComp
Text Notes 9650 6300 0    25   ~ 0
JTAG_TCK (JX1.D1)
Text GLabel 8050 6800 0    40   BiDi ~ 0
JTAG_TDI
$Comp
L Device:R R7
U 1 1 8C000011
P 9050 6800
F 0 "R7" H 9100 6700 40  0000 L CNN
F 1 "0R_DNP" H 9100 6900 40  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H 9050 7000 40  0001 C CNN
F 3 "" H 9050 6800 40  0001 C CNN
	1    9050 6800
	0    -1   -1   0   
$EndComp
Text Notes 9650 6600 0    25   ~ 0
JTAG_TDI (JX1.C2)
Text GLabel 8050 6700 0    40   BiDi ~ 0
JTAG_TDO
$Comp
L Device:R R8
U 1 1 8C000012
P 9050 6700
F 0 "R8" H 9100 6600 40  0000 L CNN
F 1 "0R_DNP" H 9100 6800 40  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H 9050 6900 40  0001 C CNN
F 3 "" H 9050 6700 40  0001 C CNN
	1    9050 6700
	0    -1   -1   0   
$EndComp
Text Notes 9650 6900 0    25   ~ 0
JTAG_TDO (JX1.D2)
Text GLabel 8050 6500 0    40   BiDi ~ 0
JTAG_TMS
$Comp
L Device:R R9
U 1 1 8C000013
P 9050 6500
F 0 "R9" H 9100 6400 40  0000 L CNN
F 1 "0R_DNP" H 9100 6600 40  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H 9050 6700 40  0001 C CNN
F 3 "" H 9050 6500 40  0001 C CNN
	1    9050 6500
	0    -1   -1   0   
$EndComp
Text Notes 9650 7200 0    25   ~ 0
JTAG_TMS (JX1.C1)
$Comp
L power:GND #PWR0102
U 1 1 8C000014
P 11050 6900
F 0 "#PWR0102" H 11050 6950 50  0001 C CNN
F 1 "GND" H 11050 7050 40  0000 C CNN
F 2 "" H 11050 6900 50  0001 C CNN
F 3 "" H 11050 6900 50  0001 C CNN
	1    11050 6900
	1    0    0    -1  
$EndComp
Text GLabel 11450 7600 2    40   Input ~ 0
VCCO_HP_65
Text Notes 1000 8500 0    60   ~ 0
========== 5. VCCO_PSIO_501 (JX3.D18) ==========
Text Notes 1000 8800 0    35   ~ 0
Sets Bank 501 MIO voltage. Tie to 1.8V for UART compatibility.
Text Notes 1000 9000 0    35   ~ 0
If 3.3V peripherals needed on MIO, change to 3.3V.
Text GLabel 1500 9400 0    40   Output ~ 0
VCCO_PSIO_501
Text GLabel 3000 9400 2    40   Input ~ 0
VCCO_HP_65
Wire Wire Line
	1900 9400 2600 9400
Text Notes 3450 9420 0    30   ~ 0
1.8V — tied to VCCO_HP_65
$Comp
L Device:C C29
U 1 1 8C000015
P 2200 9600
F 0 "C29" H 2250 9500 40  0000 L CNN
F 1 "100nF" H 2250 9700 40  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 2200 9800 40  0001 C CNN
F 3 "" H 2200 9600 40  0001 C CNN
	1    2200 9600
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 8C000016
P 2200 9900
F 0 "#PWR0103" H 2200 9950 50  0001 C CNN
F 1 "GND" H 2200 10050 40  0000 C CNN
F 2 "" H 2200 9900 50  0001 C CNN
F 3 "" H 2200 9900 50  0001 C CNN
	1    2200 9900
	1    0    0    -1  
$EndComp
Text Notes 12600 4150 0    60   ~ 0
========== DESIGN NOTES ==========
Text Notes 12600 4450 0    35   ~ 0
1. I2C pullups to 1.8V (VCCO_HP_65) — matches SOM I2C mux channel 0 levels
Text Notes 12600 4650 0    35   ~ 0
2. UART uses MIO_26/MIO_27 (UART0). Directly connected to JX3 pins D21/C22.
Text Notes 12600 4850 0    35   ~ 0
3. JTAG isolation: R6-R9 are 0-ohm DNP. Populate during dev, remove for deployment.
Text Notes 12600 5050 0    35   ~ 0
4. UART isolation: R4-R5 are 0-ohm DNP. Same hardening approach.
Text Notes 12600 5250 0    35   ~ 0
5. SOM_PG_OUT is open-drain — do NOT add pullup on carrier (SOM has 10k to 3.3V).
Text Notes 12600 5450 0    35   ~ 0
6. CC_RESET_OUT_N is open-drain — pullup R8 (10k to 1.8V) required on carrier.
Text Notes 12600 5650 0    35   ~ 0
7. VCCO_PSIO_501 set to 1.8V for UART. Change to 3.3V if adding 3.3V peripherals.
Connection ~ 9700 2100
Text GLabel 11450 6400 2    40   Input ~ 0
VCCO_HP_65
Wire Wire Line
	8050 6500 8900 6500
Wire Wire Line
	8050 6600 8900 6600
Wire Wire Line
	8050 6700 8900 6700
Wire Wire Line
	8050 6800 8900 6800
Wire Wire Line
	9200 6500 11250 6500
Wire Wire Line
	9200 6600 11250 6600
Wire Wire Line
	9200 6700 11250 6700
Wire Wire Line
	9200 6800 11250 6800
Wire Wire Line
	11250 6400 11450 6400
Wire Wire Line
	11050 6900 11250 6900
Wire Wire Line
	10500 2100 10500 2400
NoConn ~ 9700 4150
NoConn ~ 9700 3850
NoConn ~ 10100 2100
NoConn ~ 2200 9750
NoConn ~ 2200 9450
NoConn ~ 2500 6250
NoConn ~ 4700 6700
NoConn ~ 4700 6600
NoConn ~ 4700 6500
NoConn ~ 2200 3750
NoConn ~ 2200 3450
NoConn ~ 2200 3250
NoConn ~ 2200 2950
NoConn ~ 2200 2750
NoConn ~ 2200 2450
NoConn ~ 9700 1950
NoConn ~ 10150 3500
NoConn ~ 9700 3650
NoConn ~ 9700 3350
NoConn ~ 10450 3500
NoConn ~ 9700 1650
NoConn ~ 2500 6850
$Comp
L power:GND #PWR_SD03
U 1 1 5FDA000B
P 11100 10700
F 0 "#PWR_SD03" H 11100 10850 50  0001 C CNN
F 1 "GND" H 11105 10777 50  0000 C CNN
F 2 "" H 11100 10700 50  0001 C CNN
F 3 "~" H 11100 10700 50  0001 C CNN
	1    11100 10700
	1    0    0    -1  
$EndComp
Connection ~ 9400 10100
NoConn ~ 9400 10700
Wire Wire Line
	7900 10600 9400 10600
Text GLabel 7900 10600 0    40   BiDi ~ 0
SD1_CD_N
Wire Wire Line
	7900 10500 9400 10500
Text GLabel 7900 10500 0    40   BiDi ~ 0
SD1_D1
Wire Wire Line
	7900 10400 9400 10400
Text GLabel 7900 10400 0    40   BiDi ~ 0
SD1_D0
Wire Wire Line
	7900 10200 9400 10200
Text GLabel 7900 10200 0    40   BiDi ~ 0
SD1_CLK
Wire Wire Line
	7900 10000 9400 10000
Text GLabel 7900 10000 0    40   BiDi ~ 0
SD1_CMD
Wire Wire Line
	7900 9900 9400 9900
Text GLabel 7900 9900 0    40   BiDi ~ 0
SD1_D3
Wire Wire Line
	7900 9800 9400 9800
Text GLabel 7900 9800 0    40   BiDi ~ 0
SD1_D2
$Comp
L power:GND #PWR_SD02
U 1 1 5FDA000A
P 9400 10300
F 0 "#PWR_SD02" H 9400 10450 50  0001 C CNN
F 1 "GND" H 9405 10377 50  0000 C CNN
F 2 "" H 9400 10300 50  0001 C CNN
F 3 "~" H 9400 10300 50  0001 C CNN
	1    9400 10300
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG_SD01
U 1 1 5FDA000C
P 9400 10100
F 0 "#FLG_SD01" H 9400 10125 50  0001 C CNN
F 1 "PWR_FLAG" H 9400 10175 50  0000 C CNN
F 2 "" H 9400 10100 50  0001 C CNN
F 3 "~" H 9400 10100 50  0001 C CNN
	1    9400 10100
	1    0    0    -1  
$EndComp
$Comp
L power:+3V3 #PWR_SD01
U 1 1 5FDA0009
P 9400 10100
F 0 "#PWR_SD01" H 9400 9950 50  0001 C CNN
F 1 "+3V3" H 9405 10223 50  0000 L CNN
F 2 "" H 9400 10100 50  0001 C CNN
F 3 "~" H 9400 10100 50  0001 C CNN
	1    9400 10100
	1    0    0    -1  
$EndComp
$Comp
L Connector:Micro_SD_Card_Det J8
U 1 1 5FDA0008
P 10300 10200
F 0 "J8" H 10400 9300 50  0000 C CNN
F 1 "MICRO_SD_DNP" H 10500 9400 50  0000 C CNN
F 2 "Connector_Card:microSD_HC_Hirose_DM3AT-SF-PEJM5" H 10450 10300 50  0001 C CNN
F 3 "~" H 10300 10200 50  0001 C CNN
	1    10300 10200
	1    0    0    -1  
$EndComp
Text Notes 7800 8900 0    35   ~ 0
DNP J8 and ESD array (PRTR5V0U2X or equiv) for flight builds per DEC-021.
Text Notes 7800 8700 0    35   ~ 0
PS SD1: MIO46=CLK MIO47=CMD MIO48-51=DAT0-3 MIO45=CD# | 1.8V UHS-I via JX3 | VDD=3.3V
Text Notes 7800 8400 0    60   ~ 0
========== 5. SD CARD (ADD_REV1 — DNP for flight builds) ==========
$EndSCHEMATC
