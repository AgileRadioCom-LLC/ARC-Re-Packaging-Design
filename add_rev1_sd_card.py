#!/usr/bin/env python3
"""
ADD_REV1: Add micro-SD card slot (PS SD1, MIO46-51).

Decision references: DEC-021, DEC-022 (SD card = sole carrier-side storage addition,
DNP for flight builds).

Signals routed:
  MIO45 (J3 A23)  → SD1_CD_N  (card detect, active-low)
  MIO46 (J3 B24)  → SD1_CLK
  MIO47 (J3 A25)  → SD1_CMD
  MIO48 (J3 B26)  → SD1_D0
  MIO49 (J3 A27)  → SD1_D1
  MIO50 (J3 B28)  → SD1_D2
  MIO51 (J3 A29)  → SD1_D3

Changes:
  connectors.sch  — remove 7 NoConns, add 7 wire stubs + GLabels on J3
  support_io.sch  — add J8 (Micro_SD_Card_Det), power symbols, GLabels, wires

Pin positions (sheet coords, verified from UZEV_Connectors.lib + J3 transforms):
  J3 unit 1 P=(2500,16000) 1 0 0 -1:
    MIO45 A23 lib(-400,-750)  → (2100,16750)  LEFT-side
    MIO47 A25 lib(-400,-950)  → (2100,16950)  LEFT-side
    MIO49 A27 lib(-400,-1150) → (2100,17150)  LEFT-side
    MIO51 A29 lib(-400,-1350) → (2100,17350)  LEFT-side
  J3 unit 2 P=(6000,16000) 1 0 0 -1:
    MIO46 B24 lib(+400,-850)  → (6400,16850)  RIGHT-side
    MIO48 B26 lib(+400,-1050) → (6400,17050)  RIGHT-side
    MIO50 B28 lib(+400,-1250) → (6400,17250)  RIGHT-side

Connector:Micro_SD_Card_Det J8 at P=(3500,12800) in support_io.sch:
  lib pin positions (direction R, all at lib_x=-900):
    DAT2    pin1  lib(-900, 400) → sheet(2600,12400)
    DAT3/CD pin2  lib(-900, 300) → sheet(2600,12500)
    CMD     pin3  lib(-900, 200) → sheet(2600,12600)
    VDD     pin4  lib(-900, 100) → sheet(2600,12700)
    CLK     pin5  lib(-900,   0) → sheet(2600,12800)
    VSS     pin6  lib(-900,-100) → sheet(2600,12900)
    DAT0    pin7  lib(-900,-200) → sheet(2600,13000)
    DAT1    pin8  lib(-900,-300) → sheet(2600,13100)
    DET_A   pin10 lib(-900,-400) → sheet(2600,13200)
    DET_B   pin9  lib(-900,-500) → sheet(2600,13300)  ← NoConn
    SHIELD  pin11 lib(+800,-500) → sheet(4300,13300)  ← GND
"""
import os, hashlib

def md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()

def atomic_write(path, content):
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        f.write(content)
    os.replace(tmp, path)

# ── connectors.sch ───────────────────────────────────────────────────────────

CON = '/home/arc/projects/uzev_carrier_v5/connectors.sch'
con_before = md5(CON)
print(f'connectors.sch  before: {con_before}')
con_text = open(CON).read()

# Backup
bak = CON + '.bak.before_add_rev1_sd'
if not os.path.exists(bak):
    open(bak, 'w').write(con_text)
    print(f'  backup → {bak}')

# --- Remove 7 NoConns ---
noconns_to_remove = [
    'NoConn ~ 2100 16750\n',   # MIO45 CD#
    'NoConn ~ 2100 16950\n',   # MIO47 CMD
    'NoConn ~ 2100 17150\n',   # MIO49 D1
    'NoConn ~ 2100 17350\n',   # MIO51 D3
    'NoConn ~ 6400 16850\n',   # MIO46 CLK
    'NoConn ~ 6400 17050\n',   # MIO48 D0
    'NoConn ~ 6400 17250\n',   # MIO50 D2
]
for nc in noconns_to_remove:
    assert nc in con_text, f'ABORT: {nc.strip()} not found'
    assert con_text.count(nc) == 1, f'ABORT: {nc.strip()} found multiple times'
    con_text = con_text.replace(nc, '', 1)

# --- Insert J3 Row A LEFT-side stubs (MIO45,47,49,51) after Row A NoConn block ---
# Anchor: the last confirmed NoConn in the Row A left-side region at y=16550
# (MIO_41 A21 noconn), use it as insertion anchor.
# MIO_41 noconn is at (2100,16550) — already present, not removed.
# Insert new stubs AFTER the NoConn for MIO_41 (2100,16550).
ROW_A_ANCHOR = 'NoConn ~ 2100 16550\n'
ROW_A_INSERT = (
    'Wire Wire Line\n'
    '\t2100 16750 1900 16750\n'
    'Text GLabel 1900 16750 2    50   BiDi ~ 0\n'
    'SD1_CD_N\n'
    'Wire Wire Line\n'
    '\t2100 16950 1900 16950\n'
    'Text GLabel 1900 16950 2    50   BiDi ~ 0\n'
    'SD1_CMD\n'
    'Wire Wire Line\n'
    '\t2100 17150 1900 17150\n'
    'Text GLabel 1900 17150 2    50   BiDi ~ 0\n'
    'SD1_D1\n'
    'Wire Wire Line\n'
    '\t2100 17350 1900 17350\n'
    'Text GLabel 1900 17350 2    50   BiDi ~ 0\n'
    'SD1_D3\n'
)
assert ROW_A_ANCHOR in con_text, 'ABORT: Row A anchor (NoConn ~ 2100 16550) not found'
assert con_text.count(ROW_A_ANCHOR) == 1, 'ABORT: Row A anchor found multiple times'
con_text = con_text.replace(ROW_A_ANCHOR, ROW_A_ANCHOR + ROW_A_INSERT, 1)

# --- Insert J3 Row B RIGHT-side stubs (MIO46,48,50) after Row B NoConn at (6400,16650) ---
ROW_B_ANCHOR = 'NoConn ~ 6400 16650\n'
ROW_B_INSERT = (
    'Wire Wire Line\n'
    '\t6400 16850 6600 16850\n'
    'Text GLabel 6600 16850 0    50   BiDi ~ 0\n'
    'SD1_CLK\n'
    'Wire Wire Line\n'
    '\t6400 17050 6600 17050\n'
    'Text GLabel 6600 17050 0    50   BiDi ~ 0\n'
    'SD1_D0\n'
    'Wire Wire Line\n'
    '\t6400 17250 6600 17250\n'
    'Text GLabel 6600 17250 0    50   BiDi ~ 0\n'
    'SD1_D2\n'
)
assert ROW_B_ANCHOR in con_text, 'ABORT: Row B anchor (NoConn ~ 6400 16650) not found'
assert con_text.count(ROW_B_ANCHOR) == 1, 'ABORT: Row B anchor found multiple times'
con_text = con_text.replace(ROW_B_ANCHOR, ROW_B_ANCHOR + ROW_B_INSERT, 1)

atomic_write(CON, con_text)
con_after = md5(CON)
print(f'connectors.sch  after:  {con_after}')

# ── support_io.sch ────────────────────────────────────────────────────────────

SIO = '/home/arc/projects/uzev_carrier_v5/support_io.sch'
sio_before = md5(SIO)
print(f'support_io.sch  before: {sio_before}')
sio_text = open(SIO).read()

# Backup
sbak = SIO + '.bak.before_add_rev1_sd'
if not os.path.exists(sbak):
    open(sbak, 'w').write(sio_text)
    print(f'  backup → {sbak}')

SD_SECTION = (
    'Text Notes 1000 11000 0    60   ~ 0\n'
    '========== 5. SD CARD (ADD_REV1 — DNP for flight builds) ==========\n'
    'Text Notes 1000 11300 0    35   ~ 0\n'
    'PS SD1: MIO46=CLK MIO47=CMD MIO48-51=DAT0-3 MIO45=CD# | 1.8V UHS-I via JX3 | VDD=3.3V\n'
    'Text Notes 1000 11500 0    35   ~ 0\n'
    'DNP J8 and ESD array (PRTR5V0U2X or equiv) for flight builds per DEC-021.\n'
    '$Comp\n'
    'L Connector:Micro_SD_Card_Det J8\n'
    'U 1 1 5FDA0008\n'
    'P 3500 12800\n'
    'F 0 "J8" H 3600 11900 50  0000 C CNN\n'
    'F 1 "MICRO_SD_DNP" H 3700 12000 50  0000 C CNN\n'
    'F 2 "Connector_Card:microSD_HC_Hirose_DM3AT-SF-PEJM5" H 3650 12900 50  0001 C CNN\n'
    'F 3 "~" H 3500 12800 50  0001 C CNN\n'
    '\t1    3500 12800\n'
    '\t1    0    0    -1  \n'
    '$EndComp\n'
    '$Comp\n'
    'L power:+3V3 #PWR_SD01\n'
    'U 1 1 5FDA0009\n'
    'P 2600 12700\n'
    'F 0 "#PWR_SD01" H 2600 12550 50  0001 C CNN\n'
    'F 1 "+3V3" H 2605 12823 50  0000 L CNN\n'
    'F 2 "" H 2600 12700 50  0001 C CNN\n'
    'F 3 "~" H 2600 12700 50  0001 C CNN\n'
    '\t1    2600 12700\n'
    '\t1    0    0    -1  \n'
    '$EndComp\n'
    '$Comp\n'
    'L power:GND #PWR_SD02\n'
    'U 1 1 5FDA000A\n'
    'P 2600 12900\n'
    'F 0 "#PWR_SD02" H 2600 13050 50  0001 C CNN\n'
    'F 1 "GND" H 2605 12977 50  0000 C CNN\n'
    'F 2 "" H 2600 12900 50  0001 C CNN\n'
    'F 3 "~" H 2600 12900 50  0001 C CNN\n'
    '\t1    2600 12900\n'
    '\t1    0    0    -1  \n'
    '$EndComp\n'
    '$Comp\n'
    'L power:GND #PWR_SD03\n'
    'U 1 1 5FDA000B\n'
    'P 4300 13300\n'
    'F 0 "#PWR_SD03" H 4300 13450 50  0001 C CNN\n'
    'F 1 "GND" H 4305 13377 50  0000 C CNN\n'
    'F 2 "" H 4300 13300 50  0001 C CNN\n'
    'F 3 "~" H 4300 13300 50  0001 C CNN\n'
    '\t1    4300 13300\n'
    '\t1    0    0    -1  \n'
    '$EndComp\n'
    'Text GLabel 1100 12400 0    40   BiDi ~ 0\n'
    'SD1_D2\n'
    'Wire Wire Line\n'
    '\t1100 12400 2600 12400\n'
    'Text GLabel 1100 12500 0    40   BiDi ~ 0\n'
    'SD1_D3\n'
    'Wire Wire Line\n'
    '\t1100 12500 2600 12500\n'
    'Text GLabel 1100 12600 0    40   BiDi ~ 0\n'
    'SD1_CMD\n'
    'Wire Wire Line\n'
    '\t1100 12600 2600 12600\n'
    'Text GLabel 1100 12800 0    40   BiDi ~ 0\n'
    'SD1_CLK\n'
    'Wire Wire Line\n'
    '\t1100 12800 2600 12800\n'
    'Text GLabel 1100 13000 0    40   BiDi ~ 0\n'
    'SD1_D0\n'
    'Wire Wire Line\n'
    '\t1100 13000 2600 13000\n'
    'Text GLabel 1100 13100 0    40   BiDi ~ 0\n'
    'SD1_D1\n'
    'Wire Wire Line\n'
    '\t1100 13100 2600 13100\n'
    'Text GLabel 1100 13200 0    40   BiDi ~ 0\n'
    'SD1_CD_N\n'
    'Wire Wire Line\n'
    '\t1100 13200 2600 13200\n'
    'NoConn ~ 2600 13300\n'
)

END_MARKER = '$EndSCHEMATC\n'
assert END_MARKER in sio_text, 'ABORT: $EndSCHEMATC not found in support_io.sch'
sio_text = sio_text.replace(END_MARKER, SD_SECTION + END_MARKER, 1)

atomic_write(SIO, sio_text)
sio_after = md5(SIO)
print(f'support_io.sch  after:  {sio_after}')

print()
print('ADD_REV1 SD card complete.')
print('Next steps:')
print('  1. Open KiCad → reload project')
print('  2. Run ERC — expect 0 errors')
print('     (SD1_CD_N/CLK/CMD/D0-D3 nets connect J3 MIO pins to J8)')
print('  3. Save ERC as 14uzev_adrv9009_carrier.erc')
print('  4. Export updated netlist')
print('  5. Verify SD1_CLK net has J3-B24 and J8-CLK; etc.')
