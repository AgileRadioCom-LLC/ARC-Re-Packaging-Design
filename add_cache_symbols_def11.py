#!/usr/bin/env python3
"""
add_cache_symbols_def11.py
Add UZEV_Connectors_Buck_ENPG and UZEV_Connectors_LDO_ENPG
to the project cache library so KiCad ERC recognizes the w-type VOUT pins.
"""
import os, hashlib, sys

CACHE = '/home/arc/projects/uzev_carrier_v5/uzev_adrv9009_carrier-cache.lib'

def file_md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()

sz  = os.path.getsize(CACHE)
md5 = file_md5(CACHE)
print(f'PRE: size={sz} md5={md5}')

with open(CACHE) as f:
    content = f.read()

if 'UZEV_Connectors_Buck_ENPG' in content or 'UZEV_Connectors_LDO_ENPG' in content:
    print('ABORT: symbols already in cache.')
    sys.exit(1)

NEW = """
#
# UZEV_Connectors_Buck_ENPG
#
DEF UZEV_Connectors_Buck_ENPG U 0 40 Y Y 1 F N
F0 "U" 0 350 50 H V C CNN
F1 "UZEV_Connectors_Buck_ENPG" 0 -350 50 H V C CNN
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
# UZEV_Connectors_LDO_ENPG
#
DEF UZEV_Connectors_LDO_ENPG U 0 40 Y Y 1 F N
F0 "U" 0 300 50 H V C CNN
F1 "UZEV_Connectors_LDO_ENPG" 0 -300 50 H V C CNN
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

END_MARKER = '#\n#End Library'
if END_MARKER not in content:
    print('ABORT: end-of-library marker not found.')
    sys.exit(1)

new_content = content.replace(END_MARKER, NEW + END_MARKER)

tmp = CACHE + '.tmp'
with open(tmp, 'w') as f:
    f.write(new_content)
os.replace(tmp, CACHE)

new_sz  = os.path.getsize(CACHE)
new_md5 = file_md5(CACHE)
print(f'POST: size={new_sz} md5={new_md5}')
print('DONE — reopen KiCad and re-run ERC')
