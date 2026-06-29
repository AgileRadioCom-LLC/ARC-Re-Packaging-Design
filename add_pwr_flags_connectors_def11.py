#!/usr/bin/env python3
"""
add_pwr_flags_connectors_def11.py
Add PWR_FLAG stubs for 5 nets to connectors.sch so ERC sees a power driver
on Sheet /Connectors/ for MGTAVCC, MGTAVTT, MGTVCCAUX, VCCO_HP_64, VCCO_HP_65.
Mirrors DEC-014 approach (#FLG01 on VIN). Preflight on size+md5. Atomic write.
"""
import os, hashlib, sys

SCH = '/home/arc/projects/uzev_carrier_v5/connectors.sch'
EXPECTED_MD5  = 'd7f96c7310c85ca8a2c853d49faf9735'
EXPECTED_SIZE = 26980

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

# Abort if already applied
for net in ('MGTAVCC_PWR_FLAG', 'AABB0002'):
    if net in content:
        print('ABORT: flags already present.')
        sys.exit(1)

# 5 flags placed at Y=9200, X stepped by 2000, starting at X=1500
# Each: short wire to right, then GLabel pointing right
# #FLG02..#FLG06 ; UIDs AABB0002..AABB0006
FLAGS = [
    ('MGTAVCC',   1500, 9200, 'FLG02', 'AABB0002'),
    ('MGTAVTT',   3500, 9200, 'FLG03', 'AABB0003'),
    ('MGTVCCAUX', 5500, 9200, 'FLG04', 'AABB0004'),
    ('VCCO_HP_64',7500, 9200, 'FLG05', 'AABB0005'),
    ('VCCO_HP_65',9500, 9200, 'FLG06', 'AABB0006'),
]

blocks = []
for net, x, y, ref, uid in FLAGS:
    lx = x + 100   # GLabel x (right of flag pin)
    block = f"""\
Wire Wire Line
\t{x} {y} {lx} {y}
Text GLabel {lx} {y} 0    50   BiDi ~ 0
{net}
$Comp
L power:PWR_FLAG #{ref}
U 1 1 {uid}
P {x} {y}
F 0 "#{ref}" H {x} {y+50} 50  0001 C CNN
F 1 "PWR_FLAG" H {x} {y+50} 50  0000 C CNN
F 2 "" H {x} {y} 50  0001 C CNN
F 3 "~" H {x} {y} 50  0001 C CNN
\t1    {x} {y}
\t1    0    0    -1
$EndComp
"""
    blocks.append(block)

END_MARKER = '$EndSCHEMATC'
if END_MARKER not in content:
    print('ABORT: $EndSCHEMATC marker not found.')
    sys.exit(1)

insert = '\n'.join(blocks)
new_content = content.replace(END_MARKER, insert + END_MARKER)

tmp = SCH + '.tmp'
with open(tmp, 'w') as f:
    f.write(new_content)
os.replace(tmp, SCH)

new_sz  = os.path.getsize(SCH)
new_md5 = file_md5(SCH)
print(f'DONE: size={new_sz} md5={new_md5}')
print('Added PWR_FLAGs: FLG02-FLG06 for MGTAVCC MGTAVTT MGTVCCAUX VCCO_HP_64 VCCO_HP_65')
