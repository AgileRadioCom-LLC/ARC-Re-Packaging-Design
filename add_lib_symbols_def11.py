#!/usr/bin/env python3
"""
add_lib_symbols_def11.py
Add Buck_ENPG and LDO_ENPG symbols to UZEV_Connectors.lib.
Aborts on preflight mismatch. Atomic write via .tmp + os.replace.
"""
import os, hashlib, sys

LIB = '/home/arc/projects/uzev_carrier_v5/UZEV_Connectors.lib'
EXPECTED_MD5  = '54f0444e3da6ff4f5b11c23de9ca7413'
EXPECTED_SIZE = 63497

def file_md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()

sz  = os.path.getsize(LIB)
md5 = file_md5(LIB)
if sz != EXPECTED_SIZE or md5 != EXPECTED_MD5:
    print(f'PREFLIGHT FAIL: expected size={EXPECTED_SIZE} md5={EXPECTED_MD5}')
    print(f'                actual   size={sz} md5={md5}')
    sys.exit(1)
print(f'PREFLIGHT OK: size={sz} md5={md5}')

NEW_SYMBOLS = """
#
# Buck_ENPG
#
DEF Buck_ENPG U 0 40 Y Y 1 F N
F0 "U" 0 350 50 H V C CNN
F1 "Buck_ENPG" 0 -350 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
S -300 300 300 -300 0 1 10 f
X VIN 1 -500 150 200 R 50 50 1 1 W
X GND 2 0 -500 200 U 50 50 1 1 W
X VOUT 3 500 150 200 L 50 50 1 1 w
X EN 4 -500 -100 200 R 50 50 1 1 I
X PG 5 500 -100 200 L 50 50 1 1 O
ENDDRAW
ENDDEF
#
# LDO_ENPG
#
DEF LDO_ENPG U 0 40 Y Y 1 F N
F0 "U" 0 300 50 H V C CNN
F1 "LDO_ENPG" 0 -300 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
DRAW
S -250 250 250 -250 0 1 10 f
X VIN 1 -450 150 200 R 50 50 1 1 W
X GND 2 0 -450 200 U 50 50 1 1 W
X VOUT 3 450 150 200 L 50 50 1 1 w
X EN 4 -450 -100 200 R 50 50 1 1 I
X PG 5 450 -100 200 L 50 50 1 1 O
ENDDRAW
ENDDEF
"""

with open(LIB) as f:
    content = f.read()

if 'DEF Buck_ENPG' in content or 'DEF LDO_ENPG' in content:
    print('ABORT: symbols already present in library.')
    sys.exit(1)

# Insert before #End Library
END_MARKER = '#\n#End Library'
if END_MARKER not in content:
    print('ABORT: could not find end-of-library marker.')
    sys.exit(1)

new_content = content.replace(END_MARKER, NEW_SYMBOLS + END_MARKER)

tmp = LIB + '.tmp'
with open(tmp, 'w') as f:
    f.write(new_content)
os.replace(tmp, LIB)

new_sz  = os.path.getsize(LIB)
new_md5 = file_md5(LIB)
print(f'DONE: size={new_sz} md5={new_md5}')
print('Symbols added: Buck_ENPG, LDO_ENPG')
