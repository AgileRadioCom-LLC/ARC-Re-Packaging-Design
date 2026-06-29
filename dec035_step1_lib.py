#!/usr/bin/env python3
"""DEC-035 Step 1: Add USB_C_Receptacle and HUSB238 symbols to UZEV_Connectors.lib."""
import os, hashlib, sys

PROJ = os.path.dirname(os.path.abspath(__file__))
LIB  = os.path.join(PROJ, 'UZEV_Connectors.lib')

PRE_MD5 = '6331f14394645f511d8ec71a2a17cd45'

actual = hashlib.md5(open(LIB, 'rb').read()).hexdigest()
if actual != PRE_MD5:
    print(f'PRE-CHECK FAILED: md5={actual} expected={PRE_MD5}')
    sys.exit(1)

content = open(LIB).read()

if 'DEF USB_C_Receptacle' in content or 'DEF HUSB238' in content:
    print('PRE-CHECK FAILED: symbols already present')
    sys.exit(1)

if '#End Library' not in content:
    print('PRE-CHECK FAILED: #End Library marker not found')
    sys.exit(1)

print('Pre-check OK')

NEW_SYMBOLS = """\
# USB_C_Receptacle
#
DEF USB_C_Receptacle J 0 40 Y Y 1 F N
F0 "J" 0 400 50 H V C CNN
F1 "USB_C_Receptacle" 0 -400 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
S -250 350 250 -350 0 1 10 f
X VBUS  1 -450  250 200 R 50 50 1 1 W
X GND   2 -450  100 200 R 50 50 1 1 W
X CC1   3 -450  -50 200 R 50 50 1 1 P
X CC2   4 -450 -200 200 R 50 50 1 1 P
X D_P   5  450  200 200 L 50 50 1 1 P
X D_N   6  450   50 200 L 50 50 1 1 P
X SBU1  7  450 -100 200 L 50 50 1 1 P
X SBU2  8  450 -250 200 L 50 50 1 1 P
ENDDRAW
ENDDEF
#
# HUSB238
#
DEF HUSB238 U 0 40 Y Y 1 F N
F0 "U" 0 350 50 H V C CNN
F1 "HUSB238" 0 -350 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
S -250 300 250 -300 0 1 10 f
X VIN   1 -450  200 200 R 50 50 1 1 W
X GND   2 -450   50 200 R 50 50 1 1 W
X CC1   3 -450  -50 200 R 50 50 1 1 P
X CC2   4 -450 -200 200 R 50 50 1 1 P
X VOUT  5  450  200 200 L 50 50 1 1 w
X PG    6  450   50 200 L 50 50 1 1 O
X CFG1  7  450  -50 200 L 50 50 1 1 I
X CFG2  8  450 -150 200 L 50 50 1 1 I
X CFG3  9  450 -250 200 L 50 50 1 1 I
ENDDRAW
ENDDEF
#
#End Library"""

new_content = content.replace('#End Library', NEW_SYMBOLS, 1)

for sym in ['DEF USB_C_Receptacle', 'DEF HUSB238']:
    if sym not in new_content:
        print(f'POST-CHECK FAILED: {sym} not found')
        sys.exit(1)

for pin in ['X VBUS', 'X CC1', 'X CC2', 'X D_P', 'X SBU1']:
    if pin not in new_content:
        print(f'POST-CHECK FAILED: USB_C_Receptacle pin {pin} missing')
        sys.exit(1)

for pin in ['X VIN', 'X VOUT', 'X PG', 'X CFG1', 'X CFG2', 'X CFG3']:
    if pin not in new_content:
        print(f'POST-CHECK FAILED: HUSB238 pin {pin} missing')
        sys.exit(1)

if new_content.count('#End Library') != 1:
    print('POST-CHECK FAILED: #End Library count wrong')
    sys.exit(1)

print('Post-checks OK')

tmp = LIB + '.tmp'
with open(tmp, 'w') as f:
    f.write(new_content)
os.replace(tmp, LIB)

post_md5 = hashlib.md5(open(LIB, 'rb').read()).hexdigest()
print(f'Done. post_md5={post_md5}  size={os.path.getsize(LIB)}')
