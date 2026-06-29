#!/usr/bin/env python3
"""
fix_dec017_resistor_orientation.py
Rotate R6-R9 from vertical (AR 1 0 0 -1) to horizontal (AR 0 -1 -1 0).
With horizontal placement: pin 1 at (P_x-150, P_y), pin 2 at (P_x+150, P_y).
Update left wire endpoints 8900→8950, right wire starts 9300→9250.
Aborts on any verification failure. Atomic write via .tmp + os.replace.
DO NOT execute without user approval.
"""

import os, hashlib, re, sys

SCH = '/home/arc/projects/uzev_carrier_v5/support_io.sch'

EXPECTED_MD5  = 'ab82c71253c6c5f0be2672e77dc769bc'
EXPECTED_SIZE = 11794

RESISTORS = {'R6', 'R7', 'R8', 'R9'}

# Wire coord replacements: old → new (tab-prefixed, no newline)
WIRE_FIXES = {
    '\t8100 7800 8900 7800': '\t8100 7800 8950 7800',
    '\t8100 7900 8900 7900': '\t8100 7900 8950 7900',
    '\t8100 8000 8900 8000': '\t8100 8000 8950 8000',
    '\t8100 8100 8900 8100': '\t8100 8100 8950 8100',
    '\t9300 7800 11300 7800': '\t9250 7800 11300 7800',
    '\t9300 7900 11300 7900': '\t9250 7900 11300 7900',
    '\t9300 8000 11300 8000': '\t9250 8000 11300 8000',
    '\t9300 8100 11300 8100': '\t9250 8100 11300 8100',
}

def file_md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()

# ── preflight ────────────────────────────────────────────────────────────────

actual_size = os.path.getsize(SCH)
actual_md5  = file_md5(SCH)
if actual_size != EXPECTED_SIZE or actual_md5 != EXPECTED_MD5:
    print(f'PREFLIGHT FAIL: expected size={EXPECTED_SIZE} md5={EXPECTED_MD5}')
    print(f'                actual   size={actual_size} md5={actual_md5}')
    sys.exit(1)
print(f'PREFLIGHT OK: size={actual_size} md5={actual_md5}')

with open(SCH) as f:
    lines = f.readlines()

# ── phase 1: fix AR matrices for R6–R9 ──────────────────────────────────────

ar_fixed = {r: False for r in RESISTORS}
pass1 = []
i = 0

while i < len(lines):
    if lines[i].strip() == '$Comp':
        block = []
        while lines[i].strip() != '$EndComp':
            block.append(lines[i])
            i += 1
        block.append(lines[i])  # $EndComp
        i += 1

        ref = None
        for bl in block:
            m = re.match(r'^L Device:R (R\d+)\s*$', bl.strip())
            if m and m.group(1) in RESISTORS:
                ref = m.group(1)
                break

        if ref:
            new_block = []
            for bl in block:
                s = bl.rstrip('\n')
                # Match AR line: tab + exactly 4 numbers (unit line has only 3)
                m = re.match(r'^\t([-\d]+)\s+([-\d]+)\s+([-\d]+)\s+([-\d]+)\s*$', s)
                if m and (m.group(1), m.group(2), m.group(3), m.group(4)) == ('1', '0', '0', '-1'):
                    new_block.append('\t0    -1   -1   0  \n')
                    ar_fixed[ref] = True
                else:
                    new_block.append(bl)
            pass1.extend(new_block)
        else:
            pass1.extend(block)
    else:
        pass1.append(lines[i])
        i += 1

# ── phase 2: fix wire coordinates ────────────────────────────────────────────

pass2 = []
wires_fixed = {k: False for k in WIRE_FIXES}
i = 0

while i < len(pass1):
    if pass1[i].strip() == 'Wire Wire Line' and i + 1 < len(pass1):
        coord = pass1[i + 1].rstrip('\n')
        if coord in WIRE_FIXES:
            pass2.append(pass1[i])
            pass2.append(WIRE_FIXES[coord] + '\n')
            wires_fixed[coord] = True
            i += 2
            continue
    pass2.append(pass1[i])
    i += 1

# ── verification ──────────────────────────────────────────────────────────────

content = ''.join(pass2)
ok = True
print('\n--- VERIFICATION ---')

for ref, done in ar_fixed.items():
    tag = 'OK' if done else 'FAIL'
    print(f'{tag}: AR matrix rotated for {ref}')
    if not done: ok = False

for old, new in WIRE_FIXES.items():
    done = wires_fixed[old]
    tag = 'OK' if done else 'FAIL'
    print(f'{tag}: wire {old.strip()} → {new.strip()}')
    if not done: ok = False

for new_coord in WIRE_FIXES.values():
    present = (new_coord + '\n') in content
    tag = 'OK' if present else 'FAIL'
    print(f'{tag}: new coord present: {new_coord.strip()}')
    if not present: ok = False

for old_coord in WIRE_FIXES:
    absent = (old_coord + '\n') not in content
    tag = 'OK' if absent else 'FAIL'
    print(f'{tag}: old coord absent: {old_coord.strip()}')
    if not absent: ok = False

if not ok:
    print('\nABORTED — verification failed, no file written.')
    sys.exit(1)

# ── atomic write ──────────────────────────────────────────────────────────────

tmp = SCH + '.tmp'
with open(tmp, 'w') as f:
    f.write(content)
os.replace(tmp, SCH)

sz  = os.path.getsize(SCH)
md5 = file_md5(SCH)
print(f'\nAFTER: size={sz} md5={md5}')
print('DONE')
