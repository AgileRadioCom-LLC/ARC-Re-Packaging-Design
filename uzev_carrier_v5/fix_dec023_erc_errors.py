#!/usr/bin/env python3
"""
DEC-023: Fix three ERC issues in power.sch
  A) Add PWR_FLAG for GND net (ErrType(3) #PWR012 Net 829)
  B) Fix C10 wire endpoints (both pins 50 mils off, both floating)
  C) Fix C11 wire endpoints (same generator error as C10)
"""
import os, hashlib, shutil

SCH = '/home/arc/projects/uzev_carrier_v5/power.sch'
TMP = SCH + '.tmp'
BAK = SCH + '.bak.before_dec023'

with open(SCH) as f:
    content = f.read()

md5_before = hashlib.md5(content.encode()).hexdigest()
print(f"Before: md5={md5_before}")

# --- Fix B: C10 wire endpoints ---
assert content.count('\t1800 12800 1800 13000\n') == 1, "C10 top wire not unique"
assert content.count('\t1800 13200 1800 13300\n') == 1, "C10 bottom wire not unique"
content = content.replace('\t1800 12800 1800 13000\n', '\t1800 12800 1800 12950\n')
content = content.replace('\t1800 13200 1800 13300\n', '\t1800 13250 1800 13300\n')

# --- Fix C: C11 wire endpoints ---
assert content.count('\t2600 12800 2600 13000\n') == 1, "C11 top wire not unique"
assert content.count('\t2600 13200 2600 13300\n') == 1, "C11 bottom wire not unique"
content = content.replace('\t2600 12800 2600 13000\n', '\t2600 12800 2600 12950\n')
content = content.replace('\t2600 13200 2600 13300\n', '\t2600 13250 2600 13300\n')

# --- Fix A: PWR_FLAG + GND pair for GND net ---
new_block = """\
$Comp
L power:PWR_FLAG #FLG_V02
U 1 1 6C000041
P 4800 2900
F 0 "#FLG_V02" H 4800 2925 50  0001 C CNN
F 1 "PWR_FLAG" H 4800 2975 50  0000 C CNN
F 2 "" H 4800 2900 50  0001 C CNN
F 3 "~" H 4800 2900 50  0001 C CNN
\t1    4800 2900
\t1    0    0    -1
$EndComp
$Comp
L power:GND #PWR041
U 1 1 6C000042
P 4800 3100
F 0 "#PWR041" H 4800 3150 50  0001 C CNN
F 1 "GND" H 4800 3250 50  0000 C CNN
F 2 "" H 4800 3100 50  0001 C CNN
F 3 "" H 4800 3100 50  0001 C CNN
\t1    4800 3100
\t1    0    0    -1
$EndComp
Wire Wire Line
\t4800 2900 4800 3100
"""

# Anchor: immediately after #FLG_V01 $EndComp, before the VIN Text GLabel
marker = '$EndComp\nText GLabel 4000 2900 2    50   Output ~ 0\n'
assert marker in content, "Anchor marker not found — check power.sch structure"
content = content.replace(marker, '$EndComp\n' + new_block + 'Text GLabel 4000 2900 2    50   Output ~ 0\n', 1)

# Post-write assertions
assert '1800 12800 1800 12950' in content
assert '1800 13250 1800 13300' in content
assert '2600 12800 2600 12950' in content
assert '2600 13250 2600 13300' in content
assert '#FLG_V02' in content
assert '#PWR041' in content

shutil.copy2(SCH, BAK)
with open(TMP, 'w') as f:
    f.write(content)
os.replace(TMP, SCH)

with open(SCH) as f:
    md5_after = hashlib.md5(f.read().encode()).hexdigest()
print(f"After:  md5={md5_after}")
print(f"Backup: {BAK}")
print("Done — 3 fixes applied (PWR_FLAG/GND, C10 wires, C11 wires).")
