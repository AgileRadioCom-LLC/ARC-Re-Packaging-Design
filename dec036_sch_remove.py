#!/usr/bin/env python3
"""DEC-036 Step A: Remove HUSB238 circuit from power.sch.
Removes stamps 6C000095-6C00009E (10 components), their wires, junctions, and NoConns.
Updates VIN text note.
"""
import os, hashlib, sys, re

PROJ = os.path.dirname(os.path.abspath(__file__))
SCH  = os.path.join(PROJ, 'power.sch')

PRE_MD5 = '8eeabb3d55a62b4177046839b82a2275'
actual = hashlib.md5(open(SCH, 'rb').read()).hexdigest()
if actual != PRE_MD5:
    print(f'PRE-CHECK FAILED: md5={actual} expected={PRE_MD5}')
    sys.exit(1)

content = open(SCH).read()
print('Pre-check OK')

def remove_comp_block(content, stamp):
    stamp_str = f'U 1 1 {stamp}'
    stamp_pos = content.find(stamp_str)
    if stamp_pos == -1:
        raise ValueError(f'stamp {stamp} not found')
    comp_start = content.rfind('$Comp\n', 0, stamp_pos)
    if comp_start == -1:
        raise ValueError(f'$Comp not found before stamp {stamp}')
    endcomp_pos = content.find('$EndComp', stamp_pos)
    if endcomp_pos == -1:
        raise ValueError(f'$EndComp not found after stamp {stamp}')
    endcomp_end = endcomp_pos + len('$EndComp')
    if endcomp_end < len(content) and content[endcomp_end] == '\n':
        endcomp_end += 1
    return content[:comp_start] + content[endcomp_end:]

# Remove all 10 DEC-035 component blocks
for stamp in ['6C000095','6C000096','6C000097','6C000098','6C000099',
              '6C00009A','6C00009B','6C00009C','6C00009D','6C00009E']:
    try:
        content = remove_comp_block(content, stamp)
        print(f'  Removed {stamp}')
    except ValueError as e:
        print(f'ERROR: {e}')
        sys.exit(1)

# Remove NoConn flags (4)
for xy in ['1450 2800', '1450 2950', '1450 3100', '1450 3250']:
    tag = f'NoConn ~ {xy}'
    if content.count(tag) != 1:
        print(f'ERROR: NoConn "{xy}" count={content.count(tag)}')
        sys.exit(1)
    content = content.replace(tag, '', 1)
print('  Removed 4 NoConn flags')

# Remove Connection (junction) markers (5)
for xy in ['900 2750', '1200 2750', '2650 2900', '2650 3150', '2650 3250']:
    tag = f'Connection ~ {xy}'
    if content.count(tag) != 1:
        print(f'ERROR: Connection "{xy}" count={content.count(tag)}')
        sys.exit(1)
    content = content.replace(tag, '', 1)
print('  Removed 5 Connection markers')

# Remove Wire segments (17 specific segments from DEC-035)
wires_to_remove = [
    '550 2750 1750 2750',
    '900 2750 900 3250',
    '1200 2750 1200 3250',
    '1750 2750 1750 2900',
    '550 2900 550 3350',
    '900 3550 900 3700',
    '1200 3550 1200 3700',
    '1750 3050 1750 3200',
    '550 3050 1750 3150',
    '550 3200 1750 3300',
    '2650 2900 2800 2900',
    '2650 2900 2950 2900',
    '2950 3200 2950 3050',
    '2950 3050 2650 3050',
    '2650 3150 2650 3350',
    '2650 3250 2650 3350',
    '2650 3350 2650 3550',
]
for coords in wires_to_remove:
    wire = f'Wire Wire Line\n\t{coords}'
    if content.count(wire) != 1:
        print(f'ERROR: wire "{coords}" count={content.count(wire)}')
        sys.exit(1)
    content = content.replace(wire, '', 1)
print(f'  Removed {len(wires_to_remove)} wire segments')

# Update text note
OLD_NOTE = 'USB-C PD (HUSB238, 12V primary/15V fallback) -> VIN -> J1 pins A43,A46,A49,A50,B44,B47,B50,C50'
NEW_NOTE = 'USB-C PD (TPS25730D+TPS7A1633, 12V min/15V max/3A, HW strap) -> VIN -> J1 pins A43,A46,A49,A50,B44,B47,B50,C50'
if content.count(OLD_NOTE) != 1:
    print(f'ERROR: text note count={content.count(OLD_NOTE)}')
    sys.exit(1)
content = content.replace(OLD_NOTE, NEW_NOTE, 1)
print('  Updated text note')

# Post-checks
for stamp in ['6C000095','6C000096','6C000097','6C000098','6C000099',
              '6C00009A','6C00009B','6C00009C','6C00009D','6C00009E']:
    if stamp in content:
        print(f'POST-CHECK FAILED: stamp {stamp} still present')
        sys.exit(1)
if 'HUSB238' in content:
    print('POST-CHECK FAILED: HUSB238 still present')
    sys.exit(1)
if content.count('$EndSCHEMATC') != 1:
    print('POST-CHECK FAILED: $EndSCHEMATC count wrong')
    sys.exit(1)
print('Post-checks OK')

tmp = SCH + '.tmp'
with open(tmp, 'w') as f:
    f.write(content)
os.replace(tmp, SCH)

post_md5 = hashlib.md5(open(SCH, 'rb').read()).hexdigest()
print(f'Done. post_md5={post_md5}  size={os.path.getsize(SCH)}')
