#!/usr/bin/env python3
"""DEC-033 recovery: restore power.sch from backup and apply 9 footprint substitutions.
Reads power.sch.bak.before_dec033, applies DEC-033 footprint corrections, writes power.sch.
"""
import os, hashlib, sys

PROJ = os.path.dirname(os.path.abspath(__file__))
BAK  = os.path.join(PROJ, 'power.sch.bak.before_dec033')
SCH  = os.path.join(PROJ, 'power.sch')

BAK_MD5  = '4922751bd9b52f966b395b021c877bc9'
POST_MD5 = '126da442c9bdf1cb99d62f1e8e0778c3'

actual = hashlib.md5(open(BAK, 'rb').read()).hexdigest()
if actual != BAK_MD5:
    print(f'PRE-CHECK FAILED: backup md5={actual} expected={BAK_MD5}')
    sys.exit(1)

content = open(BAK).read()
print('Backup pre-check OK')

# Change 1: B5 (TPS54531) — 1 instance
OLD_B5 = 'Package_TO_SOT_SMD:PowerPAD_SO-8_EP_3.9x4.9mm_P1.27mm'
NEW_B5 = 'Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm'
if content.count(OLD_B5) != 1:
    print(f'PRE-CHECK FAILED: B5 footprint count={content.count(OLD_B5)} expected 1')
    sys.exit(1)
content = content.replace(OLD_B5, NEW_B5, 1)
print('  B5 footprint updated (1)')

# Change 2: L1-L4 (TPS7A85) — 4 instances
OLD_L = 'Package_DFN_QFN:VQFN-20-1EP_3.5x3.5mm_P0.5mm_EP2.1x2.1mm'
NEW_L = 'Package_DFN_QFN:QFN-20-1EP_3.5x3.5mm_P0.5mm_EP2x2mm'
if content.count(OLD_L) != 4:
    print(f'PRE-CHECK FAILED: L1-L4 footprint count={content.count(OLD_L)} expected 4')
    sys.exit(1)
content = content.replace(OLD_L, NEW_L)
print('  L1-L4 footprints updated (4)')

# Change 3: B1-B4 (TPS54320) — 4 instances
OLD_B = 'Package_DFN_QFN:VQFN-14-1EP_3.5x4.5mm_P0.65mm_EP2.1x3.1mm'
NEW_B = 'UZEV_Connectors:VQFN-14-1EP_3.5x3.5mm_P0.5mm_EP2.05x2.05mm'
if content.count(OLD_B) != 4:
    print(f'PRE-CHECK FAILED: B1-B4 footprint count={content.count(OLD_B)} expected 4')
    sys.exit(1)
content = content.replace(OLD_B, NEW_B)
print('  B1-B4 footprints updated (4)')

# Write to SCH (not back to BAK)
tmp = SCH + '.tmp'
with open(tmp, 'w') as f:
    f.write(content)
os.replace(tmp, SCH)

post_md5 = hashlib.md5(open(SCH, 'rb').read()).hexdigest()
print(f'post_md5={post_md5}  size={os.path.getsize(SCH)}')

if post_md5 != POST_MD5:
    print(f'POST-CHECK FAILED: expected {POST_MD5}')
    sys.exit(1)
print('Post-check OK — power.sch restored to post-DEC-033 state')
