#!/usr/bin/env python3
"""Add FB pin (pin 6, Input, right side below PG) to Buck_ENPG and LDO_ENPG symbols."""
import os, hashlib, shutil

LIB = '/home/arc/projects/uzev_carrier_v5/UZEV_Connectors.lib'
BAK = LIB + '.bak.before_dec028_fb'
TMP = LIB + '.tmp'

with open(LIB) as f:
    content = f.read()

md5_before = hashlib.md5(content.encode()).hexdigest()
print(f"Before: md5={md5_before}")

# FB pin line format: X name num x y length direction elec unit convert
# Buck_ENPG box: S -300 300 300 -300 — right side below PG (500,-100) → FB at (500,-300)
# LDO_ENPG box:  S -250 250 250 -250 — right side below PG (450,-100) → FB at (450,-300)

buck_fb = 'X FB 6 500 -300 200 L 50 50 1 1 I\n'
ldo_fb  = 'X FB 6 450 -300 200 L 50 50 1 1 I\n'

# Insert before ENDDRAW in each symbol block
# Buck_ENPG ends with: X PG 5 ... \nENDDRAW
assert content.count('DEF Buck_ENPG') == 1
assert content.count('DEF LDO_ENPG') == 1

# Anchor: last pin before ENDDRAW in Buck_ENPG
buck_anchor = 'X PG 5 500 -100 200 L 50 50 1 1 O\nENDDRAW\nENDDEF\n#\n# LDO_ENPG'
ldo_anchor  = 'X PG 5 450 -100 200 L 50 50 1 1 O\nENDDRAW\nENDDEF\n#\n#End Library'

assert buck_anchor in content, f"Buck anchor not found"
assert ldo_anchor  in content, f"LDO anchor not found"

content = content.replace(
    buck_anchor,
    f'X PG 5 500 -100 200 L 50 50 1 1 O\n{buck_fb}ENDDRAW\nENDDEF\n#\n# LDO_ENPG'
)
content = content.replace(
    ldo_anchor,
    f'X PG 5 450 -100 200 L 50 50 1 1 O\n{ldo_fb}ENDDRAW\nENDDEF\n#\n#End Library'
)

assert 'X FB 6 500 -300 200 L 50 50 1 1 I' in content, "Buck FB pin not inserted"
assert 'X FB 6 450 -300 200 L 50 50 1 1 I' in content, "LDO FB pin not inserted"

shutil.copy2(LIB, BAK)
with open(TMP, 'w') as f:
    f.write(content)
os.replace(TMP, LIB)

with open(LIB) as f:
    md5_after = hashlib.md5(f.read().encode()).hexdigest()
print(f"After:  md5={md5_after}")
print(f"Backup: {BAK}")
print("FB pin added to Buck_ENPG and LDO_ENPG.")
