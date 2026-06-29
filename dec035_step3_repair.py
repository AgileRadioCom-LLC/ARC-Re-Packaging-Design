#!/usr/bin/env python3
"""DEC-035 Step 3 repair: restore accidentally deleted VIN caps and fix ref collisions.

The remove_comp_block regex in dec035_step3_sch.py expanded across block boundaries,
deleting C4, C5, C6, #PWR01-03 (stamps 6C000002-6C000007) along with #PWR04.
This script:
  1. Restores C4, C5, C6, #PWR01, #PWR02, #PWR03 (VIN rail decoupling — NOT barrel jack).
  2. Renames the new VBUS decoupling caps: C7→C60, C8→C61 (avoid collision with
     existing C7/100nF and C8/47uF in B3 buck output area).
"""
import os, hashlib, sys

PROJ = os.path.dirname(os.path.abspath(__file__))
SCH  = os.path.join(PROJ, 'power.sch')

PRE_MD5 = 'ec59929f83a2c907b317741ff6be736c'

actual = hashlib.md5(open(SCH, 'rb').read()).hexdigest()
if actual != PRE_MD5:
    print(f'PRE-CHECK FAILED: md5={actual} expected={PRE_MD5}')
    sys.exit(1)

content = open(SCH).read()

# Verify the stamps are indeed missing
for stamp in ['6C000002','6C000003','6C000004','6C000005','6C000006','6C000007']:
    if stamp in content:
        print(f'PRE-CHECK FAILED: stamp {stamp} already present — unexpected state')
        sys.exit(1)

# Verify new C7/C8 (new VBUS decoupling) are present at expected coords
if 'F 0 "C7" H 950 3250' not in content:
    print('PRE-CHECK FAILED: new C7 at (950,3250) not found')
    sys.exit(1)
if 'F 0 "C8" H 1250 3250' not in content:
    print('PRE-CHECK FAILED: new C8 at (1250,3250) not found')
    sys.exit(1)

print('Pre-check OK')

# ── 1. Rename new C7→C60, new C8→C61 (precise coord-based match) ─────────────
# C7 new: F0 field "C7" H 950 ... and L Device:C C7 with stamp 6C000097
content = content.replace('L Device:C C7\nU 1 1 6C000097', 'L Device:C C60\nU 1 1 6C000097', 1)
content = content.replace('F 0 "C7" H 950 3250', 'F 0 "C60" H 950 3250', 1)

# C8 new: F0 field "C8" H 1250 ... and stamp 6C000098
content = content.replace('L Device:C C8\nU 1 1 6C000098', 'L Device:C C61\nU 1 1 6C000098', 1)
content = content.replace('F 0 "C8" H 1250 3250', 'F 0 "C61" H 1250 3250', 1)

print('Refs renamed: C7→C60, C8→C61')

# ── 2. Restore deleted blocks (C4, C5, C6, #PWR01, #PWR02, #PWR03) ───────────
# These are the VIN rail input decoupling caps and their GND symbols.
# Wires (2800,3100→2800,2900), (2800,3300→2800,3500) etc. are still in the file
# (the wire removal in step 3 only removed 2400,2900→2800,2900 which was J5's wire).
# We insert these blocks before $EndSCHEMATC.
STD = '1    0    0    -1'

RESTORED = f"""\
$Comp
L Device:C C4
U 1 1 6C000002
P 2800 3200
F 0 "C4" H 2850 3050 50  0000 L CNN
F 1 "33uF" H 2850 3350 50  0000 L CNN
F 2 "Capacitor_SMD:C_1210_3225Metric" H 2800 3200 50  0001 C CNN
F 3 "" H 2800 3200 50  0001 C CNN
\t1    2800 3200
\t{STD}
$EndComp
$Comp
L Device:C C5
U 1 1 6C000003
P 3200 3200
F 0 "C5" H 3250 3050 50  0000 L CNN
F 1 "33uF" H 3250 3350 50  0000 L CNN
F 2 "Capacitor_SMD:C_1210_3225Metric" H 3200 3200 50  0001 C CNN
F 3 "" H 3200 3200 50  0001 C CNN
\t1    3200 3200
\t{STD}
$EndComp
$Comp
L Device:C C6
U 1 1 6C000004
P 3600 3200
F 0 "C6" H 3650 3050 50  0000 L CNN
F 1 "100nF" H 3650 3350 50  0000 L CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 3600 3200 50  0001 C CNN
F 3 "" H 3600 3200 50  0001 C CNN
\t1    3600 3200
\t{STD}
$EndComp
$Comp
L power:GND #PWR01
U 1 1 6C000005
P 2800 3500
F 0 "#PWR01" H 2800 3550 50  0001 C CNN
F 1 "GND" H 2800 3650 50  0000 C CNN
F 2 "" H 2800 3500 50  0001 C CNN
F 3 "" H 2800 3500 50  0001 C CNN
\t1    2800 3500
\t{STD}
$EndComp
$Comp
L power:GND #PWR02
U 1 1 6C000006
P 3200 3500
F 0 "#PWR02" H 3200 3550 50  0001 C CNN
F 1 "GND" H 3200 3650 50  0000 C CNN
F 2 "" H 3200 3500 50  0001 C CNN
F 3 "" H 3200 3500 50  0001 C CNN
\t1    3200 3500
\t{STD}
$EndComp
$Comp
L power:GND #PWR03
U 1 1 6C000007
P 3600 3500
F 0 "#PWR03" H 3600 3550 50  0001 C CNN
F 1 "GND" H 3600 3650 50  0000 C CNN
F 2 "" H 3600 3500 50  0001 C CNN
F 3 "" H 3600 3500 50  0001 C CNN
\t1    3600 3500
\t{STD}
$EndComp
"""

if content.count('$EndSCHEMATC') != 1:
    print(f'PRE-CHECK FAILED: $EndSCHEMATC count = {content.count("$EndSCHEMATC")}')
    sys.exit(1)

new_content = content.replace('$EndSCHEMATC', RESTORED + '$EndSCHEMATC', 1)

# ── 3. Post-checks ─────────────────────────────────────────────────────────────
for ref in ['C4', 'C5', 'C6', 'C60', 'C61']:
    if f'F 0 "{ref}"' not in new_content:
        print(f'POST-CHECK FAILED: {ref} not found')
        sys.exit(1)

for stamp in ['6C000002','6C000003','6C000004','6C000005','6C000006','6C000007']:
    if stamp not in new_content:
        print(f'POST-CHECK FAILED: stamp {stamp} not restored')
        sys.exit(1)

# Verify old colliding C7/C8 refs in new area are gone
if 'F 0 "C7" H 950 3250' in new_content:
    print('POST-CHECK FAILED: old C7 coord ref still present')
    sys.exit(1)
if 'F 0 "C8" H 1250 3250' in new_content:
    print('POST-CHECK FAILED: old C8 coord ref still present')
    sys.exit(1)

# Existing C7/C8 in B3 area should still be present
if 'F 0 "C7" H 2850 10900' not in new_content:
    print('POST-CHECK FAILED: existing C7 (B3) missing')
    sys.exit(1)
if 'F 0 "C8" H 5575 10900' not in new_content:
    print('POST-CHECK FAILED: existing C8 (B3) missing')
    sys.exit(1)

if new_content.count('$EndSCHEMATC') != 1:
    print('POST-CHECK FAILED: $EndSCHEMATC count wrong')
    sys.exit(1)

print('Post-checks OK')

# ── 4. Atomic write ───────────────────────────────────────────────────────────
tmp = SCH + '.tmp'
with open(tmp, 'w') as f:
    f.write(new_content)
os.replace(tmp, SCH)

post_md5 = hashlib.md5(open(SCH, 'rb').read()).hexdigest()
print(f'Done. post_md5={post_md5}  size={os.path.getsize(SCH)}')
