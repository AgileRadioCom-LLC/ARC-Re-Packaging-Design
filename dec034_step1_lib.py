#!/usr/bin/env python3
"""DEC-034 Step 1: Add SW/BOOT/COMP/RT/SS pins to Buck_ENPG symbol."""
import os, hashlib, sys

PROJ = os.path.dirname(os.path.abspath(__file__))
LIB  = os.path.join(PROJ, 'UZEV_Connectors.lib')

PRE_MD5  = '55a6352265bd284d8ffab7a67f2f0e08'

OLD_BLOCK = """\
DRAW
S -300 300 300 -300 0 1 10 f
X VIN 1 -500 150 200 R 50 50 1 1 W
X GND 2 0 -500 200 U 50 50 1 1 W
X VOUT 3 500 150 200 L 50 50 1 1 w
X EN 4 -500 -100 200 R 50 50 1 1 I
X PG 5 500 -100 200 L 50 50 1 1 O
X FB 6 500 -300 200 L 50 50 1 1 I
ENDDRAW
ENDDEF
#
# LDO_ENPG"""

NEW_BLOCK = """\
DRAW
S -300 450 300 -450 0 1 10 f
X VIN 1 -500 150 200 R 50 50 1 1 W
X GND 2 0 -500 200 U 50 50 1 1 W
X VOUT 3 500 150 200 L 50 50 1 1 w
X EN 4 -500 -100 200 R 50 50 1 1 I
X PG 5 500 -100 200 L 50 50 1 1 O
X FB 6 500 -300 200 L 50 50 1 1 I
X SW 7 500 350 200 L 50 50 1 1 P
X BOOT 8 0 650 200 D 50 50 1 1 P
X COMP 9 -500 -250 200 R 50 50 1 1 P
X RT 10 -500 -400 200 R 50 50 1 1 I
X SS 11 200 -650 200 U 50 50 1 1 I
ENDDRAW
ENDDEF
#
# LDO_ENPG"""

# --- verify pre-condition ---
content = open(LIB).read()
actual_md5 = hashlib.md5(open(LIB,'rb').read()).hexdigest()
if actual_md5 != PRE_MD5:
    print(f'PRE-CHECK FAILED: md5={actual_md5} expected={PRE_MD5}')
    sys.exit(1)

if OLD_BLOCK not in content:
    print('PRE-CHECK FAILED: expected Buck_ENPG DRAW block not found verbatim')
    sys.exit(1)

# count occurrences
if content.count(OLD_BLOCK) != 1:
    print(f'PRE-CHECK FAILED: found {content.count(OLD_BLOCK)} occurrences of OLD_BLOCK (expected 1)')
    sys.exit(1)

print('Pre-check OK')

# --- apply edit ---
new_content = content.replace(OLD_BLOCK, NEW_BLOCK, 1)

# --- verify post-condition ---
if OLD_BLOCK in new_content:
    print('POST-CHECK FAILED: old block still present')
    sys.exit(1)
if NEW_BLOCK not in new_content:
    print('POST-CHECK FAILED: new block not found')
    sys.exit(1)
# check all 11 pins present
for pin in ['X VIN 1', 'X GND 2', 'X VOUT 3', 'X EN 4', 'X PG 5', 'X FB 6',
            'X SW 7', 'X BOOT 8', 'X COMP 9', 'X RT 10', 'X SS 11']:
    if pin not in new_content:
        print(f'POST-CHECK FAILED: missing {pin}')
        sys.exit(1)

# --- atomic write ---
tmp = LIB + '.tmp'
with open(tmp, 'w') as f:
    f.write(new_content)
os.replace(tmp, LIB)

post_md5 = hashlib.md5(open(LIB,'rb').read()).hexdigest()
print(f'Done. post_md5={post_md5}')
print(f'Size: {os.path.getsize(LIB)}')
