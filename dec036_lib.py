#!/usr/bin/env python3
"""DEC-036 lib: Remove HUSB238; update USB_C_Receptacle; add TPS25730D and TPS7A1633."""
import os, hashlib, sys

PROJ = os.path.dirname(os.path.abspath(__file__))
LIB  = os.path.join(PROJ, 'UZEV_Connectors.lib')

PRE_MD5  = '63fe2e2e3c9c84424d2f50d959ecd432'
PRE_SIZE = 65554

actual_md5  = hashlib.md5(open(LIB, 'rb').read()).hexdigest()
actual_size = os.path.getsize(LIB)
if actual_md5 != PRE_MD5 or actual_size != PRE_SIZE:
    print(f'PRE-CHECK FAILED: md5={actual_md5} size={actual_size}')
    sys.exit(1)

content = open(LIB).read()
print('Pre-check OK')

# ── 1. Remove HUSB238 symbol block ──────────────────────────────────────────
# Block from "# HUSB238\n#\nDEF HUSB238" through "ENDDEF\n"
HUSB238_BLOCK = (
    '# HUSB238\n'
    '#\n'
    'DEF HUSB238 U 0 40 Y Y 1 F N\n'
    'F0 "U" 0 350 50 H V C CNN\n'
    'F1 "HUSB238" 0 -350 50 H V C CNN\n'
    'F2 "" 0 0 50 H I C CNN\n'
    'F3 "" 0 0 50 H I C CNN\n'
    'DRAW\n'
    'S -250 300 250 -300 0 1 10 f\n'
    'X VIN   1 -450  200 200 R 50 50 1 1 W\n'
    'X GND   2 -450   50 200 R 50 50 1 1 W\n'
    'X CC1   3 -450  -50 200 R 50 50 1 1 P\n'
    'X CC2   4 -450 -200 200 R 50 50 1 1 P\n'
    'X VOUT  5  450  200 200 L 50 50 1 1 w\n'
    'X PG    6  450   50 200 L 50 50 1 1 O\n'
    'X CFG1  7  450  -50 200 L 50 50 1 1 I\n'
    'X CFG2  8  450 -150 200 L 50 50 1 1 I\n'
    'X CFG3  9  450 -250 200 L 50 50 1 1 I\n'
    'ENDDRAW\n'
    'ENDDEF\n'
)
if content.count(HUSB238_BLOCK) != 1:
    print(f'PRE-CHECK FAILED: HUSB238 block count={content.count(HUSB238_BLOCK)}')
    sys.exit(1)
content = content.replace(HUSB238_BLOCK, '', 1)
print('  Removed HUSB238 symbol')

# ── 2. Update USB_C_Receptacle: remove D_P/D_N/SBU1/SBU2 pins ──────────────
OLD_USBC = (
    '# USB_C_Receptacle\n'
    '#\n'
    'DEF USB_C_Receptacle J 0 40 Y Y 1 F N\n'
    'F0 "J" 0 400 50 H V C CNN\n'
    'F1 "USB_C_Receptacle" 0 -400 50 H V C CNN\n'
    'F2 "" 0 0 50 H I C CNN\n'
    'F3 "" 0 0 50 H I C CNN\n'
    'DRAW\n'
    'S -250 350 250 -350 0 1 10 f\n'
    'X VBUS  1 -450  250 200 R 50 50 1 1 W\n'
    'X GND   2 -450  100 200 R 50 50 1 1 W\n'
    'X CC1   3 -450  -50 200 R 50 50 1 1 P\n'
    'X CC2   4 -450 -200 200 R 50 50 1 1 P\n'
    'X D_P   5  450  200 200 L 50 50 1 1 P\n'
    'X D_N   6  450   50 200 L 50 50 1 1 P\n'
    'X SBU1  7  450 -100 200 L 50 50 1 1 P\n'
    'X SBU2  8  450 -250 200 L 50 50 1 1 P\n'
    'ENDDRAW\n'
    'ENDDEF\n'
)
NEW_USBC = (
    '# USB_C_Receptacle\n'
    '#\n'
    'DEF USB_C_Receptacle J 0 40 Y Y 1 F N\n'
    'F0 "J" 0 300 50 H V C CNN\n'
    'F1 "USB_C_Receptacle" 0 -300 50 H V C CNN\n'
    'F2 "" 0 0 50 H I C CNN\n'
    'F3 "" 0 0 50 H I C CNN\n'
    'DRAW\n'
    'S -250 250 250 -250 0 1 10 f\n'
    'X VBUS  1 -450  150 200 R 50 50 1 1 W\n'
    'X GND   2 -450    0 200 R 50 50 1 1 W\n'
    'X CC1   3 -450 -100 200 R 50 50 1 1 P\n'
    'X CC2   4 -450 -200 200 R 50 50 1 1 P\n'
    'ENDDRAW\n'
    'ENDDEF\n'
)
if content.count(OLD_USBC) != 1:
    print(f'PRE-CHECK FAILED: USB_C_Receptacle old block count={content.count(OLD_USBC)}')
    sys.exit(1)
content = content.replace(OLD_USBC, NEW_USBC, 1)
print('  Updated USB_C_Receptacle (removed D+/D-/SBU pins)')

# ── 3. Add TPS25730D and TPS7A1633 before #End Library ──────────────────────
# TPS25730D symbol: WQFN-38, organized by function (not physical pin order)
# Left side: control/signal inputs; Right side: power/outputs; Bottom: GND/VBUS/RESERVED
TPS25730D_SYM = (
    '#\n'
    '# TPS25730D\n'
    '#\n'
    'DEF TPS25730D U 0 40 Y Y 1 F N\n'
    'F0 "U" 0 1100 50 H V C CNN\n'
    'F1 "TPS25730D" 0 -1100 50 H V C CNN\n'
    'F2 "" 0 0 50 H I C CNN\n'
    'F3 "" 0 0 50 H I C CNN\n'
    'DRAW\n'
    'S -600 1000 600 -1000 0 1 10 f\n'
    # Left side — inputs/control (top to bottom)
    'X VIN_3V3    38 -800  900 200 R 50 50 1 1 W\n'
    'X CC1        28 -800  800 200 R 50 50 1 1 P\n'
    'X CC2        29 -800  700 200 R 50 50 1 1 P\n'
    'X ADCIN1      2 -800  600 200 R 50 50 1 1 I\n'
    'X ADCIN2      3 -800  500 200 R 50 50 1 1 I\n'
    'X ADCIN3      5 -800  400 200 R 50 50 1 1 I\n'
    'X ADCIN4      7 -800  300 200 R 50 50 1 1 I\n'
    'X LDO_3V3     1 -800  200 200 R 50 50 1 1 O\n'
    'X LDO_1V5     4 -800  100 200 R 50 50 1 1 O\n'
    'X FAULT_IN   18 -800    0 200 R 50 50 1 1 I\n'
    'X I2Ct_SCL    9 -800 -100 200 R 50 50 1 1 I\n'
    'X I2Ct_SDA    8 -800 -200 200 R 50 50 1 1 P\n'
    'X CAP_MIS     6 -800 -300 200 R 50 50 1 1 O\n'
    'X DBG_ACC    10 -800 -400 200 R 50 50 1 1 O\n'
    # Right side — power/outputs (top to bottom)
    'X VBUS_IN_A  23  800  900 200 L 50 50 1 1 W\n'
    'X VBUS_IN_B  24  800  800 200 L 50 50 1 1 W\n'
    'X VBUS_IN_C  25  800  700 200 L 50 50 1 1 W\n'
    'X PPHV_A     20  800  550 200 L 50 50 1 1 P\n'
    'X PPHV_B     21  800  450 200 L 50 50 1 1 P\n'
    'X PPHV_C     22  800  350 200 L 50 50 1 1 P\n'
    'X DRAIN_A    15  800  200 200 L 50 50 1 1 P\n'
    'X DRAIN_B    30  800  100 200 L 50 50 1 1 P\n'
    'X SINK_EN    19  800    0 200 L 50 50 1 1 O\n'
    'X PLUG_EVENT 37  800 -100 200 L 50 50 1 1 O\n'
    'X PLUG_FLIP  13  800 -200 200 L 50 50 1 1 O\n'
    # Bottom — GND (multi-pad), VBUS, RESERVED, thermal
    'X GND_11     11    0 -1200 200 U 50 50 1 1 W\n'
    'X GND_12     12  100 -1200 200 U 50 50 1 1 W\n'
    'X GND_14     14  200 -1200 200 U 50 50 1 1 W\n'
    'X GND_16     16  300 -1200 200 U 50 50 1 1 W\n'
    'X GND_17     17  400 -1200 200 U 50 50 1 1 W\n'
    'X GND_31     31  500 -1200 200 U 50 50 1 1 W\n'
    'X GND_34     34 -500 -1200 200 U 50 50 1 1 W\n'
    'X GND_35     35 -400 -1200 200 U 50 50 1 1 W\n'
    'X GND_EP     39 -300 -1200 200 U 50 50 1 1 W\n'
    'X DRAIN_EP   40 -200 -1200 200 U 50 50 1 1 P\n'
    'X VBUS_32    32 -100 -1200 200 U 50 50 1 1 P\n'
    'X VBUS_33    33    0  1200 200 D 50 50 1 1 P\n'
    'X RSV_26     26  100  1200 200 D 50 50 1 1 I\n'
    'X RSV_27     27  200  1200 200 D 50 50 1 1 I\n'
    'X RSV_36     36  300  1200 200 D 50 50 1 1 I\n'
    'ENDDRAW\n'
    'ENDDEF\n'
)

# TPS7A1633 symbol: HVSSOP-8 + thermal pad
TPS7A1633_SYM = (
    '#\n'
    '# TPS7A1633\n'
    '#\n'
    'DEF TPS7A1633 U 0 40 Y Y 1 F N\n'
    'F0 "U" 0 350 50 H V C CNN\n'
    'F1 "TPS7A1633" 0 -350 50 H V C CNN\n'
    'F2 "" 0 0 50 H I C CNN\n'
    'F3 "" 0 0 50 H I C CNN\n'
    'DRAW\n'
    'S -300 300 300 -300 0 1 10 f\n'
    'X IN    1 -500  200 200 R 50 50 1 1 W\n'
    'X GND   2    0 -500 200 U 50 50 1 1 W\n'
    'X EN    3 -500  100 200 R 50 50 1 1 I\n'
    'X DNC   4 -500    0 200 R 50 50 1 1 N\n'
    'X DELAY 5 -500 -100 200 R 50 50 1 1 P\n'
    'X PG    6  500 -100 200 L 50 50 1 1 O\n'
    'X OUT   7  500  200 200 L 50 50 1 1 w\n'
    'X OUT   8  500  100 200 L 50 50 1 1 w\n'
    'X GND_EP 9   0 -700 200 U 50 50 1 1 W\n'
    'ENDDRAW\n'
    'ENDDEF\n'
)

END_MARKER = '#\n#End Library'
if content.count(END_MARKER) != 1:
    print(f'PRE-CHECK FAILED: #End Library count={content.count(END_MARKER)}')
    sys.exit(1)

content = content.replace(END_MARKER, TPS25730D_SYM + TPS7A1633_SYM + END_MARKER, 1)
print('  Added TPS25730D and TPS7A1633 symbols')

# ── 4. Post-checks ─────────────────────────────────────────────────────────
if 'HUSB238' in content:
    print('POST-CHECK FAILED: HUSB238 still present')
    sys.exit(1)
if 'D_P' in content or 'SBU1' in content:
    print('POST-CHECK FAILED: D_P/SBU1 still in USB_C_Receptacle')
    sys.exit(1)
if 'DEF TPS25730D' not in content:
    print('POST-CHECK FAILED: TPS25730D not found')
    sys.exit(1)
if 'DEF TPS7A1633' not in content:
    print('POST-CHECK FAILED: TPS7A1633 not found')
    sys.exit(1)
if content.count('ENDDEF') < 8:
    print('POST-CHECK FAILED: unexpected ENDDEF count')
    sys.exit(1)

print('Post-checks OK')

tmp = LIB + '.tmp'
with open(tmp, 'w') as f:
    f.write(content)
os.replace(tmp, LIB)

post_md5 = hashlib.md5(open(LIB, 'rb').read()).hexdigest()
print(f'Done. post_md5={post_md5}  size={os.path.getsize(LIB)}')
