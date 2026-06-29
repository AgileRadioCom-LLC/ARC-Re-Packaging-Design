#!/usr/bin/env python3
"""DEC-034 Step 2b: Fix ref collisions in power.sch.

Renames new buck components to use non-conflicting refs:
  C20-C24 (C_BOOT)  → C40-C44
  C25-C29 (C_COMP)  → C45-C49
  C30-C34 (C_HF)    → C50-C54
  C35-C39 (C_SS)    → C55-C59
  D1 (catch diode)  → D2

C21-C29 and D1 already exist in adrv9009_signals.sch / support_io.sch.
"""
import os, hashlib, sys

PROJ = os.path.dirname(os.path.abspath(__file__))
SCH  = os.path.join(PROJ, 'power.sch')
PRE_MD5 = '2e8bbdb393e72771961c0e6008e8b410'

actual = hashlib.md5(open(SCH, 'rb').read()).hexdigest()
if actual != PRE_MD5:
    print(f'PRE-CHECK FAILED: md5={actual}')
    sys.exit(1)
print('Pre-check OK')

content = open(SCH).read()

# Build rename map — must rename in DESCENDING numeric order to avoid
# e.g. C20→C40 then C40 being renamed again (not an issue here since
# target range C40-C59 is not in source range C20-C39, but be safe).
renames = {}
for i in range(5):
    renames[f'C{20+i}']  = f'C{40+i}'   # C_BOOT
    renames[f'C{25+i}']  = f'C{45+i}'   # C_COMP
    renames[f'C{30+i}']  = f'C{50+i}'   # C_HF
    renames[f'C{35+i}']  = f'C{55+i}'   # C_SS
renames['D1_CATCH'] = 'D2'  # handled specially below

# Rename capacitors: match the F 0 "Cxx" pattern (exact match)
for old, new in renames.items():
    if old == 'D1_CATCH':
        continue
    pat = f'F 0 "{old}"'
    rep = f'F 0 "{new}"'
    count = content.count(pat)
    if count != 1:
        print(f'WARN: {pat} found {count} times (expected 1)')
    content = content.replace(pat, rep)

# Rename D1 catch diode: must only rename the NEW one (Device:D CDBC540-G),
# not any existing D1.  The new D1 block has stamp 6C000093.
old_d1_stamp = 'L Device:D D1\nU 1 1 6C000093'
new_d2_stamp = 'L Device:D D2\nU 1 1 6C000093'
if content.count(old_d1_stamp) != 1:
    print(f'PRE-CHECK FAILED: D1 stamp block found {content.count(old_d1_stamp)} times')
    sys.exit(1)
content = content.replace(old_d1_stamp, new_d2_stamp, 1)
# Also rename the F 0 "D1" in that same block — it's unique to stamp 6C000093
# Find the block and fix the F 0 field
old_d1_f0 = 'F 0 "D1" H 14050 7900'
new_d2_f0 = 'F 0 "D2" H 14050 7900'
if content.count(old_d1_f0) != 1:
    print(f'PRE-CHECK FAILED: D1 F0 field found {content.count(old_d1_f0)} times')
    sys.exit(1)
content = content.replace(old_d1_f0, new_d2_f0, 1)

# Post-checks: verify new refs present, old conflicting refs absent in new additions
expected = (
    [f'C{40+i}' for i in range(20)] +  # C40-C59
    ['D2']
)
for ref in expected:
    if f'F 0 "{ref}"' not in content:
        print(f'POST-CHECK FAILED: {ref} not found')
        sys.exit(1)

# old conflicting refs (C21-C29, D1-catch) should no longer be present
# as F 0 "Cxx" patterns originating from the new additions
# (C21-C28 from adrv9009_signals will still be there but have different footprints)
# Just verify D1 CDBC540-G is gone
if 'CDBC540-G' in content and 'F 0 "D1"' in content:
    # If D1 still has CDBC540-G value in an F1 field, something is wrong
    idx = content.find('CDBC540-G')
    surrounding = content[max(0,idx-200):idx+50]
    if 'F 0 "D1"' in surrounding:
        print('POST-CHECK FAILED: D1 still associated with CDBC540-G')
        sys.exit(1)

print('Post-checks OK')

tmp = SCH + '.tmp'
with open(tmp, 'w') as f:
    f.write(content)
os.replace(tmp, SCH)

post_md5 = hashlib.md5(open(SCH, 'rb').read()).hexdigest()
print(f'Done. post_md5={post_md5}  size={os.path.getsize(SCH)}')
