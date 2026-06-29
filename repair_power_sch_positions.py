#!/usr/bin/env python3
"""
repair_power_sch_positions.py
Each $Comp block in power.sch is missing the position-repeat line
(the '\t1    X    Y' that must precede the rotation matrix '\t1    0    0    -1').
This script inserts the correct position for every affected component.
Atomic write via .tmp + os.replace.
"""
import re, os, hashlib, sys

SCH = '/home/arc/projects/uzev_carrier_v5/power.sch'
EXPECTED_MD5  = '36675a02ad64a536ff21468faaddae66'
EXPECTED_SIZE = 23959

def file_md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()

sz  = os.path.getsize(SCH)
md5 = file_md5(SCH)
if sz != EXPECTED_SIZE or md5 != EXPECTED_MD5:
    print(f'PREFLIGHT FAIL: expected size={EXPECTED_SIZE} md5={EXPECTED_MD5}')
    print(f'                actual   size={sz} md5={md5}')
    sys.exit(1)
print(f'PREFLIGHT OK: size={sz} md5={md5}')

with open(SCH) as f:
    content = f.read()

# Split into $Comp blocks and non-comp sections
# Strategy: process line by line, tracking state
lines = content.split('\n')
out = []
i = 0
fixed = 0
p_x = p_y = None
in_comp = False

while i < len(lines):
    line = lines[i]

    if line.strip() == '$Comp':
        in_comp = True
        p_x = p_y = None
        out.append(line)
        i += 1
        continue

    if in_comp:
        # Extract P X Y
        m = re.match(r'^P\s+(\d+)\s+(\d+)$', line.strip())
        if m:
            p_x, p_y = int(m.group(1)), int(m.group(2))

        # Detect the rotation matrix line (last line before $EndComp)
        # Pattern: starts with tab, then 1 or -1, then 0 0 -1 or similar
        rot_m = re.match(r'^\t(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)', line)
        if rot_m and i + 1 < len(lines) and lines[i+1].strip() == '$EndComp':
            # This is the rotation matrix line — check if the line BEFORE it
            # is the position line (tab + 1 + X + Y)
            prev = out[-1] if out else ''
            pos_m = re.match(r'^\t1\s+\d+\s+\d+', prev)
            if not pos_m and p_x is not None:
                # Insert missing position line
                out.append(f'\t1    {p_x} {p_y}')
                fixed += 1

        if line.strip() == '$EndComp':
            in_comp = False
            p_x = p_y = None

    out.append(line)
    i += 1

new_content = '\n'.join(out)

tmp = SCH + '.tmp'
with open(tmp, 'w') as f:
    f.write(new_content)
os.replace(tmp, SCH)

new_sz  = os.path.getsize(SCH)
new_md5 = file_md5(SCH)
print(f'Fixed {fixed} component(s).')
print(f'DONE: size={new_sz} md5={new_md5}')
