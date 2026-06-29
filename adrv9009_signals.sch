EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A1 33110 23386
encoding utf-8
Sheet 4 5
Title "Sheet 3: ADRV9009 Signals"
Date "2026-03-19"
Rev "1.0"
Comp "ADRV9009 + UltraZed-EV Carrier Board"
Comment1 "Step 8D: ADRV9009 Signal Routing"
Comment2 "20 GT signals + 45 Bank 65 signals = 65 total"
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 1000 800  0    100  ~ 0
SHEET 3: ADRV9009 SIGNAL ROUTING
Text Notes 1000 1100 0    45   ~ 0
Section A: GT Signals (Quad 227) — FMC DP pins to JX2 GTH pins
Text Notes 1000 1400 0    45   ~ 0
Section B: Bank 65 Signals (LVDS + LVCMOS18) — FMC LA pins to JX1 HP_DP pins
Text Notes 1000 1700 0    50   ~ 0
CRITICAL: Non-sequential JESD204B lane mapping. rx_data[0]=DP1, NOT DP0.
Text Notes 1000 2000 0    40   ~ 0
AC coupling caps (100nF 0201) on TX lines placed near FMC connector.
Text Notes 1000 2800 0    60   ~ 0
========== SECTION A: GT SIGNALS (FMC DP -> JX2 Quad 227) ==========
Text Notes 1000 3200 0    45   ~ 0
--- Reference Clocks (AC coupled on SOM) ---
Text Notes 1500 3550 0    30   ~ 0
GTH_REFCLK0  (D04_GBTCLK0_M2C_P/D05_GBTCLK0_M2C_N -> JX2.D26/JX2.D27  FPGA:D10/D9)
Text GLabel 1500 3700 0    40   BiDi ~ 0
FMC_D04_GBTCLK0_M2C_P
Text GLabel 2700 3700 2    40   BiDi ~ 0
GTH_REFCLK0_P
Wire Wire Line
	1900 3700 2300 3700
Text GLabel 1500 3900 0    40   BiDi ~ 0
FMC_D05_GBTCLK0_M2C_N
Text GLabel 2700 3900 2    40   BiDi ~ 0
GTH_REFCLK0_N
Wire Wire Line
	1900 3900 2300 3900
Text Notes 1500 4150 0    30   ~ 0
GTH_REFCLK1  (B20_GBTCLK1_M2C_P/B21_GBTCLK1_M2C_N -> JX2.C27/JX2.C28  FPGA:B10/B9)
Text GLabel 1500 4300 0    40   BiDi ~ 0
FMC_B20_GBTCLK1_M2C_P
Text GLabel 2700 4300 2    40   BiDi ~ 0
GTH_REFCLK1_P
Wire Wire Line
	1900 4300 2300 4300
Text GLabel 1500 4500 0    40   BiDi ~ 0
FMC_B21_GBTCLK1_M2C_N
Text GLabel 2700 4500 2    40   BiDi ~ 0
GTH_REFCLK1_N
Wire Wire Line
	1900 4500 2300 4500
Text Notes 1000 4800 0    45   ~ 0
--- RX Lanes (ADRV9009 TX -> FPGA RX, direct connection) ---
Text Notes 1500 4950 0    30   ~ 0
rx_data_0_DP1  (A02_DP1_M2C_P/A03_DP1_M2C_N -> JX2.A21/JX2.A22  FPGA:C4/C3)
Text GLabel 1500 5100 0    40   BiDi ~ 0
FMC_A02_DP1_M2C_P
Text GLabel 2700 5100 2    40   BiDi ~ 0
rx_data_0_DP1_P
Wire Wire Line
	1900 5100 2300 5100
Text GLabel 1500 5300 0    40   BiDi ~ 0
FMC_A03_DP1_M2C_N
Text GLabel 2700 5300 2    40   BiDi ~ 0
rx_data_0_DP1_N
Wire Wire Line
	1900 5300 2300 5300
Text Notes 1500 5550 0    30   ~ 0
rx_data_1_DP2  (A06_DP2_M2C_P/A07_DP2_M2C_N -> JX2.C21/JX2.C22  FPGA:D2/D1)
Text GLabel 1500 5700 0    40   BiDi ~ 0
FMC_A06_DP2_M2C_P
Text GLabel 2700 5700 2    40   BiDi ~ 0
rx_data_1_DP2_P
Wire Wire Line
	1900 5700 2300 5700
Text GLabel 1500 5900 0    40   BiDi ~ 0
FMC_A07_DP2_M2C_N
Text GLabel 2700 5900 2    40   BiDi ~ 0
rx_data_1_DP2_N
Wire Wire Line
	1900 5900 2300 5900
Text Notes 1500 6150 0    30   ~ 0
rx_data_2_DP0  (C06_DP0_M2C_P/C07_DP0_M2C_N -> JX2.C24/JX2.C25  FPGA:B2/B1)
Text GLabel 1500 6300 0    40   BiDi ~ 0
FMC_C06_DP0_M2C_P
Text GLabel 2700 6300 2    40   BiDi ~ 0
rx_data_2_DP0_P
Wire Wire Line
	1900 6300 2300 6300
Text GLabel 1500 6500 0    40   BiDi ~ 0
FMC_C07_DP0_M2C_N
Text GLabel 2700 6500 2    40   BiDi ~ 0
rx_data_2_DP0_N
Wire Wire Line
	1900 6500 2300 6500
Text Notes 1500 6750 0    30   ~ 0
rx_data_3_DP3  (A10_DP3_M2C_P/A11_DP3_M2C_N -> JX2.A24/JX2.A25  FPGA:A4/A3)
Text GLabel 1500 6900 0    40   BiDi ~ 0
FMC_A10_DP3_M2C_P
Text GLabel 2700 6900 2    40   BiDi ~ 0
rx_data_3_DP3_P
Wire Wire Line
	1900 6900 2300 6900
Text GLabel 1500 7100 0    40   BiDi ~ 0
FMC_A11_DP3_M2C_N
Text GLabel 2700 7100 2    40   BiDi ~ 0
rx_data_3_DP3_N
Wire Wire Line
	1900 7100 2300 7100
Text Notes 1000 7400 0    45   ~ 0
--- TX Lanes (FPGA TX -> ADRV9009 RX, AC coupled) ---
Text Notes 1500 7550 0    30   ~ 0
tx_data_0_DP1  (A22_DP1_C2M_P/A23_DP1_C2M_N -> JX2.D20/JX2.D21  FPGA:D6/D5)
Text GLabel 1500 7700 0    40   BiDi ~ 0
FMC_A22_DP1_C2M_P
$Comp
L Device:C C21
U 1 1 7B000001
P 2100 7700
F 0 "C21" H 2150 7600 40  0000 L CNN
F 1 "100nF" H 2150 7800 40  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 2100 7900 40  0001 C CNN
F 3 "" H 2100 7700 40  0001 C CNN
	1    2100 7700
	1    0    0    -1  
$EndComp
Text GLabel 2700 7700 2    40   BiDi ~ 0
tx_data_0_DP1_P
Text GLabel 1500 7900 0    40   BiDi ~ 0
FMC_A23_DP1_C2M_N
$Comp
L Device:C C22
U 1 1 7B000002
P 2100 7900
F 0 "C22" H 2150 7800 40  0000 L CNN
F 1 "100nF" H 2150 8000 40  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 2100 8100 40  0001 C CNN
F 3 "" H 2100 7900 40  0001 C CNN
	1    2100 7900
	1    0    0    -1  
$EndComp
Text GLabel 2700 7900 2    40   BiDi ~ 0
tx_data_0_DP1_N
Text Notes 1500 8150 0    30   ~ 0
tx_data_1_DP2  (A26_DP2_C2M_P/A27_DP2_C2M_N -> JX2.B20/JX2.B21  FPGA:C8/C7)
Text GLabel 1500 8300 0    40   BiDi ~ 0
FMC_A26_DP2_C2M_P
$Comp
L Device:C C23
U 1 1 7B000003
P 2100 8300
F 0 "C23" H 2150 8200 40  0000 L CNN
F 1 "100nF" H 2150 8400 40  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 2100 8500 40  0001 C CNN
F 3 "" H 2100 8300 40  0001 C CNN
	1    2100 8300
	1    0    0    -1  
$EndComp
Text GLabel 2700 8300 2    40   BiDi ~ 0
tx_data_1_DP2_P
Text GLabel 1500 8500 0    40   BiDi ~ 0
FMC_A27_DP2_C2M_N
$Comp
L Device:C C24
U 1 1 7B000004
P 2100 8500
F 0 "C24" H 2150 8400 40  0000 L CNN
F 1 "100nF" H 2150 8600 40  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 2100 8700 40  0001 C CNN
F 3 "" H 2100 8500 40  0001 C CNN
	1    2100 8500
	1    0    0    -1  
$EndComp
Text GLabel 2700 8500 2    40   BiDi ~ 0
tx_data_1_DP2_N
Text Notes 1500 8750 0    30   ~ 0
tx_data_2_DP0  (C02_DP0_C2M_P/C03_DP0_C2M_N -> JX2.D23/JX2.D24  FPGA:B6/B5)
Text GLabel 1500 8900 0    40   BiDi ~ 0
FMC_C02_DP0_C2M_P
$Comp
L Device:C C25
U 1 1 7B000005
P 2100 8900
F 0 "C25" H 2150 8800 40  0000 L CNN
F 1 "100nF" H 2150 9000 40  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 2100 9100 40  0001 C CNN
F 3 "" H 2100 8900 40  0001 C CNN
	1    2100 8900
	1    0    0    -1  
$EndComp
Text GLabel 2700 8900 2    40   BiDi ~ 0
tx_data_2_DP0_P
Text GLabel 1500 9100 0    40   BiDi ~ 0
FMC_C03_DP0_C2M_N
$Comp
L Device:C C26
U 1 1 7B000006
P 2100 9100
F 0 "C26" H 2150 9000 40  0000 L CNN
F 1 "100nF" H 2150 9200 40  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 2100 9300 40  0001 C CNN
F 3 "" H 2100 9100 40  0001 C CNN
	1    2100 9100
	1    0    0    -1  
$EndComp
Text GLabel 2700 9100 2    40   BiDi ~ 0
tx_data_2_DP0_N
Text Notes 1500 9350 0    30   ~ 0
tx_data_3_DP3  (A30_DP3_C2M_P/A31_DP3_C2M_N -> JX2.B23/JX2.B24  FPGA:A8/A7)
Text GLabel 1500 9500 0    40   BiDi ~ 0
FMC_A30_DP3_C2M_P
$Comp
L Device:C C27
U 1 1 7B000007
P 2100 9500
F 0 "C27" H 2150 9400 40  0000 L CNN
F 1 "100nF" H 2150 9600 40  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 2100 9700 40  0001 C CNN
F 3 "" H 2100 9500 40  0001 C CNN
	1    2100 9500
	1    0    0    -1  
$EndComp
Text GLabel 2700 9500 2    40   BiDi ~ 0
tx_data_3_DP3_P
Text GLabel 1500 9700 0    40   BiDi ~ 0
FMC_A31_DP3_C2M_N
$Comp
L Device:C C28
U 1 1 7B000008
P 2100 9700
F 0 "C28" H 2150 9600 40  0000 L CNN
F 1 "100nF" H 2150 9800 40  0000 L CNN
F 2 "Capacitor_SMD:C_0201_0603Metric" H 2100 9900 40  0001 C CNN
F 3 "" H 2100 9700 40  0001 C CNN
	1    2100 9700
	1    0    0    -1  
$EndComp
Text GLabel 2700 9700 2    40   BiDi ~ 0
tx_data_3_DP3_N
Text Notes 11300 2750 0    60   ~ 0
========== SECTION B: BANK 65 SIGNALS (FMC LA -> JX1) ==========
Text Notes 12000 3300 0    45   ~ 0
--- LVDS Differential Pairs ---
Text GLabel 12000 3700 0    40   BiDi ~ 0
FMC_G06_LA00_CC_P
Wire Wire Line
	12400 3700 13000 3700
Text GLabel 13400 3700 2    40   BiDi ~ 0
HP_DP_33_GC_P
Text Notes 14000 3720 0    25   ~ 0
sysref_p (G06_LA00_CC_P->C31)
Text GLabel 12000 3950 0    40   BiDi ~ 0
FMC_G07_LA00_CC_N
Wire Wire Line
	12400 3950 13000 3950
Text GLabel 13400 3950 2    40   BiDi ~ 0
HP_DP_33_GC_N
Text Notes 14000 3970 0    25   ~ 0
sysref_n (G07_LA00_CC_N->C32)
Text GLabel 12000 4200 0    40   BiDi ~ 0
FMC_D08_LA01_CC_P
Wire Wire Line
	12400 4200 13000 4200
Text GLabel 13400 4200 2    40   BiDi ~ 0
HP_DP_32_GC_P
Text Notes 14000 4220 0    25   ~ 0
sysref_out_p (D08_LA01_CC_P->D32)
Text GLabel 12000 4450 0    40   BiDi ~ 0
FMC_D09_LA01_CC_N
Wire Wire Line
	12400 4450 13000 4450
Text GLabel 13400 4450 2    40   BiDi ~ 0
HP_DP_32_GC_N
Text Notes 14000 4470 0    25   ~ 0
sysref_out_n (D09_LA01_CC_N->D33)
Text GLabel 12000 4700 0    40   BiDi ~ 0
FMC_H07_LA02_P
Wire Wire Line
	12400 4700 13000 4700
Text GLabel 13400 4700 2    40   BiDi ~ 0
HP_DP_30_P
Text Notes 14000 4720 0    25   ~ 0
tx_sync_p (H07_LA02_P->B28)
Text GLabel 12000 4950 0    40   BiDi ~ 0
FMC_H08_LA02_N
Wire Wire Line
	12400 4950 13000 4950
Text GLabel 13400 4950 2    40   BiDi ~ 0
HP_DP_30_N
Text Notes 14000 4970 0    25   ~ 0
tx_sync_n (H08_LA02_N->B29)
Text GLabel 12000 5200 0    40   BiDi ~ 0
FMC_G09_LA03_P
Wire Wire Line
	12400 5200 13000 5200
Text GLabel 13400 5200 2    40   BiDi ~ 0
HP_DP_46_P
Text Notes 14000 5220 0    25   ~ 0
rx_sync_p (G09_LA03_P->B42)
Text GLabel 12000 5450 0    40   BiDi ~ 0
FMC_G10_LA03_N
Wire Wire Line
	12400 5450 13000 5450
Text GLabel 13400 5450 2    40   BiDi ~ 0
HP_DP_46_N
Text Notes 14000 5470 0    25   ~ 0
rx_sync_n (G10_LA03_N->B43)
Text GLabel 12000 5700 0    40   BiDi ~ 0
FMC_G27_LA25_P
Wire Wire Line
	12400 5700 13000 5700
Text GLabel 13400 5700 2    40   BiDi ~ 0
HP_DP_26_P
Text Notes 14000 5720 0    25   ~ 0
rx_os_sync_p (G27_LA25_P->A28)
Text GLabel 12000 5950 0    40   BiDi ~ 0
FMC_G28_LA25_N
Wire Wire Line
	12400 5950 13000 5950
Text GLabel 13400 5950 2    40   BiDi ~ 0
HP_DP_26_N
Text Notes 14000 5970 0    25   ~ 0
rx_os_sync_n (G28_LA25_N->A29)
Text Notes 12000 7000 0    45   ~ 0
--- SPI Bus (LVCMOS18) ---
Text GLabel 12000 7400 0    40   BiDi ~ 0
FMC_H13_LA07_P
Wire Wire Line
	12400 7400 13000 7400
Text GLabel 13400 7400 2    40   BiDi ~ 0
HP_DP_34_GC_P
Text Notes 14000 7420 0    25   ~ 0
spi_clk (H13_LA07_P->B32)
Text GLabel 12000 7650 0    40   BiDi ~ 0
FMC_H14_LA07_N
Wire Wire Line
	12400 7650 13000 7650
Text GLabel 13400 7650 2    40   BiDi ~ 0
HP_DP_34_GC_N
Text Notes 14000 7670 0    25   ~ 0
spi_mosi (H14_LA07_N->B33)
Text GLabel 12000 7900 0    40   BiDi ~ 0
FMC_G12_LA08_P
Wire Wire Line
	12400 7900 13000 7900
Text GLabel 13400 7900 2    40   BiDi ~ 0
HP_DP_40_P
Text Notes 14000 7920 0    25   ~ 0
spi_miso (G12_LA08_P->D39)
Text GLabel 12000 8150 0    40   BiDi ~ 0
FMC_D14_LA09_P
Wire Wire Line
	12400 8150 13000 8150
Text GLabel 13400 8150 2    40   BiDi ~ 0
HP_DP_36_P
Text Notes 14000 8170 0    25   ~ 0
spi_csn_adrv9009 (D14_LA09_P->D36)
Text GLabel 12000 8400 0    40   BiDi ~ 0
FMC_D15_LA09_N
Wire Wire Line
	12400 8400 13000 8400
Text GLabel 13400 8400 2    40   BiDi ~ 0
HP_DP_36_N
Text Notes 14000 8420 0    25   ~ 0
spi_csn_ad9528 (D15_LA09_N->D37)
Text Notes 12000 8950 0    45   ~ 0
--- Control Signals (LVCMOS18) ---
Text GLabel 12000 9350 0    40   BiDi ~ 0
FMC_H10_LA04_P
Wire Wire Line
	12400 9350 13000 9350
Text GLabel 13400 9350 2    40   BiDi ~ 0
HP_DP_39_P
Text Notes 13950 9370 0    25   ~ 0
adrv9009_reset_b (H10_LA04_P->A35)
Text GLabel 12000 9600 0    40   BiDi ~ 0
FMC_H11_LA04_N
Wire Wire Line
	12400 9600 13000 9600
Text GLabel 13400 9600 2    40   BiDi ~ 0
HP_DP_39_N
Text Notes 13950 9620 0    25   ~ 0
ad9528_reset_b (H11_LA04_N->A36)
Text GLabel 12000 9850 0    40   BiDi ~ 0
FMC_C18_LA14_P
Wire Wire Line
	12400 9850 13000 9850
Text GLabel 13400 9850 2    40   BiDi ~ 0
HP_DP_45_P
Text Notes 13950 9870 0    25   ~ 0
adrv9009_test (D11_LA05_P->D22)
Text GLabel 12000 10100 0    40   BiDi ~ 0
FMC_C19_LA14_N
Wire Wire Line
	12400 10100 13000 10100
Text GLabel 13400 10100 2    40   BiDi ~ 0
HP_DP_45_N
Text Notes 13950 10120 0    25   ~ 0
ad9528_status (D12_LA05_N->D23)
Text GLabel 12000 10350 0    40   BiDi ~ 0
FMC_C10_LA06_P
Wire Wire Line
	12400 10350 13000 10350
Text GLabel 13400 10350 2    40   BiDi ~ 0
HP_DP_44_P
Text Notes 13950 10370 0    25   ~ 0
adrv9009_gpint1 (C10_LA06_P->D25)
Text GLabel 12000 10600 0    40   BiDi ~ 0
FMC_C11_LA06_N
Wire Wire Line
	12400 10600 13000 10600
Text GLabel 13400 10600 2    40   BiDi ~ 0
HP_DP_44_N
Text Notes 13950 10620 0    25   ~ 0
adrv9009_gpint2 (C11_LA06_N->D26)
Text Notes 12000 11150 0    45   ~ 0
--- ADRV9009 GPIO (LVCMOS18) ---
Text Notes 12000 11350 0    30   ~ 0
4 GPIO corrections from Section 6 applied (gpio_04/05/09/10 JX1 pins fixed)
Text GLabel 12000 11650 0    40   BiDi ~ 0
FMC_C22_LA18_CC_P
Wire Wire Line
	12400 11650 13000 11650
Text GLabel 13400 11650 2    40   BiDi ~ 0
HP_DP_31_P
Text Notes 14100 11670 0    25   ~ 0
adrv9009_gpio_00 (C14_LA10_P->C14)
Text GLabel 12000 11900 0    40   BiDi ~ 0
FMC_C23_LA18_CC_N
Wire Wire Line
	12400 11900 13000 11900
Text GLabel 13400 11900 2    40   BiDi ~ 0
HP_DP_31_N
Text Notes 14100 11920 0    25   ~ 0
adrv9009_gpio_01 (C15_LA10_N->C15)
Text GLabel 12000 12150 0    40   BiDi ~ 0
FMC_H16_LA11_P
Wire Wire Line
	12400 12150 13000 12150
Text GLabel 13400 12150 2    40   BiDi ~ 0
HP_DP_43_P
Text Notes 14100 12170 0    25   ~ 0
adrv9009_gpio_02 (H16_LA11_P->B11)
Text GLabel 12000 12400 0    40   BiDi ~ 0
FMC_H17_LA11_N
Wire Wire Line
	12400 12400 13000 12400
Text GLabel 13400 12400 2    40   BiDi ~ 0
HP_DP_43_N
Text Notes 14100 12420 0    25   ~ 0
adrv9009_gpio_03 (H17_LA11_N->B12)
Text GLabel 12000 12650 0    40   BiDi ~ 0
FMC_G15_LA12_P
Wire Wire Line
	12400 12650 13000 12650
Text GLabel 13400 12650 2    40   BiDi ~ 0
HP_DP_37_P
Text Notes 14100 12670 0    25   ~ 0
adrv9009_gpio_04 (G15_LA12_P->A24)
Text GLabel 12000 12900 0    40   BiDi ~ 0
FMC_G16_LA12_N
Wire Wire Line
	12400 12900 13000 12900
Text GLabel 13400 12900 2    40   BiDi ~ 0
HP_DP_37_N
Text Notes 14100 12920 0    25   ~ 0
adrv9009_gpio_05 (G16_LA12_N->A25)
Text GLabel 12000 13150 0    40   BiDi ~ 0
FMC_D17_LA13_P
Wire Wire Line
	12400 13150 13000 13150
Text GLabel 13400 13150 2    40   BiDi ~ 0
HP_DP_35_GC_P
Text Notes 14100 13170 0    25   ~ 0
adrv9009_gpio_06 (D17_LA13_P->C18)
Text GLabel 12000 13400 0    40   BiDi ~ 0
FMC_D18_LA13_N
Wire Wire Line
	12400 13400 13000 13400
Text GLabel 13400 13400 2    40   BiDi ~ 0
HP_DP_35_GC_N
Text Notes 14100 13420 0    25   ~ 0
adrv9009_gpio_07 (D18_LA13_N->C19)
Text GLabel 12000 13650 0    40   BiDi ~ 0
FMC_G18_LA16_P
Wire Wire Line
	12400 13650 13000 13650
Text GLabel 13400 13650 2    40   BiDi ~ 0
HP_DP_29_P
Text Notes 14100 13670 0    25   ~ 0
adrv9009_gpio_08 (G18_LA16_P->D19)
Text GLabel 12000 13900 0    40   BiDi ~ 0
FMC_G19_LA16_N
Wire Wire Line
	12400 13900 13000 13900
Text GLabel 13400 13900 2    40   BiDi ~ 0
HP_DP_29_N
Text Notes 14100 13920 0    25   ~ 0
adrv9009_gpio_09 (G19_LA16_N->C24)
Text GLabel 12000 14150 0    40   BiDi ~ 0
FMC_H19_LA15_P
Wire Wire Line
	12400 14150 13000 14150
Text GLabel 13400 14150 2    40   BiDi ~ 0
HP_DP_28_P
Text Notes 14100 14170 0    25   ~ 0
adrv9009_gpio_10 (H19_LA15_P->C25)
Text GLabel 12000 14400 0    40   BiDi ~ 0
FMC_H20_LA15_N
Wire Wire Line
	12400 14400 13000 14400
Text GLabel 13400 14400 2    40   BiDi ~ 0
HP_DP_28_N
Text Notes 14100 14420 0    25   ~ 0
adrv9009_gpio_11 (H20_LA15_N->B15)
Text GLabel 12000 14650 0    40   BiDi ~ 0
FMC_G21_LA20_P
Wire Wire Line
	12400 14650 13000 14650
Text GLabel 13400 14650 2    40   BiDi ~ 0
HP_DP_24_P
Text Notes 14100 14670 0    25   ~ 0
adrv9009_gpio_12 (G21_LA20_P->D11)
Text GLabel 12000 14900 0    40   BiDi ~ 0
FMC_G22_LA20_N
Wire Wire Line
	12400 14900 13000 14900
Text GLabel 13400 14900 2    40   BiDi ~ 0
HP_DP_24_N
Text Notes 14100 14920 0    25   ~ 0
adrv9009_gpio_13 (G22_LA20_N->D12)
Text GLabel 12000 15150 0    40   BiDi ~ 0
FMC_H22_LA19_P
Wire Wire Line
	12400 15150 13000 15150
Text GLabel 13400 15150 2    40   BiDi ~ 0
HP_DP_25_P
Text Notes 14100 15170 0    25   ~ 0
adrv9009_gpio_14 (H22_LA19_P->D8)
Text GLabel 12000 15400 0    40   BiDi ~ 0
FMC_H23_LA19_N
Wire Wire Line
	12400 15400 13000 15400
Text GLabel 13400 15400 2    40   BiDi ~ 0
HP_DP_25_N
Text Notes 14100 15420 0    25   ~ 0
adrv9009_gpio_15 (H23_LA19_N->D9)
Text Notes 12000 15950 0    45   ~ 0
--- Additional Signals ---
Text GLabel 12000 16350 0    40   BiDi ~ 0
FMC_H25_LA21_P
Wire Wire Line
	12400 16350 13000 16350
Text GLabel 13400 16350 2    40   BiDi ~ 0
HP_DP_27_P
Text Notes 14000 16370 0    25   ~ 0
adrv9009_rx1_enable (H25_LA21_P->B22)
Text GLabel 12000 16600 0    40   BiDi ~ 0
FMC_H26_LA21_N
Wire Wire Line
	12400 16600 13000 16600
Text GLabel 13400 16600 2    40   BiDi ~ 0
HP_DP_27_N
Text Notes 14000 16620 0    25   ~ 0
adrv9009_rx2_enable (H26_LA21_N->B23)
Text GLabel 12000 16850 0    40   BiDi ~ 0
FMC_D26_LA26_P
Wire Wire Line
	12400 16850 13000 16850
Text GLabel 13400 16850 2    40   BiDi ~ 0
HP_DP_47_P
Text Notes 14000 16870 0    25   ~ 0
adrv9009_tx1_enable (D23_LA23_P->C22)
Text GLabel 12000 17100 0    40   BiDi ~ 0
FMC_D27_LA26_N
Wire Wire Line
	12400 17100 13000 17100
Text GLabel 13400 17100 2    40   BiDi ~ 0
HP_DP_47_N
Text Notes 14000 17120 0    25   ~ 0
adrv9009_tx2_enable (D24_LA23_N->C23)
Text GLabel 12000 17350 0    40   BiDi ~ 0
FMC_G24_LA22_P
Wire Wire Line
	12400 17350 13000 17350
Text GLabel 13400 17350 2    40   BiDi ~ 0
HP_DP_41_P
Text Notes 14000 17370 0    25   ~ 0
ad9528_sysref_req (G24_LA22_P->B19)
Text GLabel 12000 17600 0    40   BiDi ~ 0
FMC_G25_LA22_N
Wire Wire Line
	12400 17600 13000 17600
Text GLabel 13400 17600 2    40   BiDi ~ 0
HP_DP_41_N
Text Notes 14000 17620 0    25   ~ 0
hmc7044_sync (G25_LA22_N->B20)
Text Notes 1000 15000 0    60   ~ 0
========== DESIGN NOTES ==========
Text Notes 1000 15400 0    40   ~ 0
1. GT signals route: FMC J4 (DP pins) -> carrier PCB -> JX2 (SOM GTH pins)
Text Notes 1000 15700 0    40   ~ 0
2. Bank 65 signals route: FMC J4 (LA pins) -> carrier PCB -> JX1 (SOM HP_DP pins)
Text Notes 1000 16000 0    40   ~ 0
3. AC coupling caps on TX only (100nF 0201) — place within 50 mils of FMC pads
Text Notes 1000 16300 0    40   ~ 0
4. REFCLK pairs already AC coupled on SOM (10nF caps on SOM schematic sheet 10)
Text Notes 1000 16600 0    40   ~ 0
5. Non-sequential lane mapping is handled in FPGA IP config (system_bd.tcl)
Text Notes 1000 16900 0    40   ~ 0
6. All LVDS pairs must be length-matched within 5 mils during PCB layout
Text Notes 1000 17200 0    40   ~ 0
7. GT traces: 100-ohm diff impedance, route on top layer with solid GND reference
Text Notes 1000 17500 0    40   ~ 0
8. GPIO corrections (Section 6): gpio_04->A24, gpio_05->A25, gpio_09->C24, gpio_10->C25
Wire Wire Line
	1500 5100 2700 5100
Wire Wire Line
	1500 5300 2700 5300
Wire Wire Line
	1500 5700 2700 5700
Wire Wire Line
	1500 5900 2700 5900
Wire Wire Line
	1500 6300 2700 6300
Wire Wire Line
	1500 6500 2700 6500
Wire Wire Line
	1500 6900 2700 6900
Wire Wire Line
	1500 7100 2700 7100
Wire Wire Line
	1500 7700 2700 7700
Wire Wire Line
	1500 7900 2700 7900
Wire Wire Line
	1500 8300 2700 8300
Wire Wire Line
	1500 8500 2700 8500
Wire Wire Line
	1500 8900 2700 8900
Wire Wire Line
	1500 9100 2700 9100
Wire Wire Line
	1500 9500 2700 9500
Wire Wire Line
	1500 9700 2700 9700
Wire Wire Line
	1500 3700 2700 3700
Wire Wire Line
	12000 3700 13400 3700
Wire Wire Line
	1500 3900 2700 3900
Wire Wire Line
	12000 3950 13400 3950
Wire Wire Line
	12000 4200 13400 4200
Wire Wire Line
	1500 4300 2700 4300
Wire Wire Line
	12000 4450 13400 4450
Wire Wire Line
	1500 4500 2700 4500
Wire Wire Line
	12000 4700 13400 4700
Wire Wire Line
	12000 4950 13400 4950
Wire Wire Line
	12000 5200 13400 5200
Wire Wire Line
	12000 5450 13400 5450
Wire Wire Line
	12000 5700 13400 5700
Wire Wire Line
	12000 5950 13400 5950
Wire Wire Line
	12000 7400 13400 7400
Wire Wire Line
	12000 7650 13400 7650
Wire Wire Line
	12000 7900 13400 7900
Wire Wire Line
	12000 8150 13400 8150
Wire Wire Line
	12000 8400 13400 8400
Wire Wire Line
	12000 9350 13400 9350
Wire Wire Line
	12000 9600 13400 9600
Wire Wire Line
	12000 9850 13400 9850
Wire Wire Line
	12000 10100 13400 10100
Wire Wire Line
	12000 10350 13400 10350
Wire Wire Line
	12000 10600 13400 10600
Wire Wire Line
	12000 11650 13400 11650
Wire Wire Line
	12000 11900 13400 11900
Wire Wire Line
	12000 12150 13400 12150
Wire Wire Line
	12000 12400 13400 12400
Wire Wire Line
	12000 12650 13400 12650
Wire Wire Line
	12000 12900 13400 12900
Wire Wire Line
	12000 13150 13400 13150
Wire Wire Line
	12000 13400 13400 13400
Wire Wire Line
	12000 13650 13400 13650
Wire Wire Line
	12000 13900 13400 13900
Wire Wire Line
	12000 14150 13400 14150
Wire Wire Line
	12000 14400 13400 14400
Wire Wire Line
	12000 14650 13400 14650
Wire Wire Line
	12000 14900 13400 14900
Wire Wire Line
	12000 15150 13400 15150
Wire Wire Line
	12000 15400 13400 15400
Wire Wire Line
	12000 16350 13400 16350
Wire Wire Line
	12000 16600 13400 16600
Wire Wire Line
	12000 16850 13400 16850
Wire Wire Line
	12000 17100 13400 17100
Wire Wire Line
	12000 17350 13400 17350
Wire Wire Line
	12000 17600 13400 17600
NoConn ~ 2100 8450
NoConn ~ 2100 8150
NoConn ~ 2100 8050
NoConn ~ 2100 7750
NoConn ~ 2100 8350
NoConn ~ 2100 7850
NoConn ~ 2100 7550
NoConn ~ 2100 8650
NoConn ~ 2100 8750
NoConn ~ 2100 9050
NoConn ~ 2100 8950
NoConn ~ 2100 9250
NoConn ~ 2100 9350
NoConn ~ 2100 9650
NoConn ~ 2100 9850
NoConn ~ 2100 9550
$EndSCHEMATC
