#!/usr/bin/env python3
"""DEC-028: Add Rfb resistor pairs + GND for all 9 power stages."""
import os, hashlib, shutil

SCH = '/home/arc/projects/uzev_carrier_v5/power.sch'
BAK = SCH + '.bak.before_dec028'

# (stage, Px, Py, x_offset, r_top_val, r_bot_val, r_top_ref, r_bot_ref)
STAGES = [
    ('B1', 3500,  5500, 500, '88.7k', '100k', 'R1',  'R2' ),
    ('B2', 3500,  8200, 500, '124k',  '100k', 'R3',  'R4' ),
    ('B3', 3500, 10900, 500, '215k',  '100k', 'R5',  'R6' ),
    ('B4',13500,  5500, 500, '215k',  '100k', 'R7',  'R8' ),
    ('B5',13500,  8200, 500, '316k',  '100k', 'R9',  'R10'),
    ('L1', 7500,  5500, 450, '12.4k', '100k', 'R11', 'R12'),
    ('L2', 7500,  8200, 450, '49.9k', '100k', 'R13', 'R14'),
    ('L3', 7500, 10900, 450, '124k',  '100k', 'R15', 'R16'),
    ('L4',17500,  5500, 450, '124k',  '100k', 'R17', 'R18'),
]

RFMT = """$Comp
L Device:R {ref}
U 1 1 {uid}
P {cx} {cy}
F 0 "{ref}" H {lx} {ly0} 50  0000 L CNN
F 1 "{val}" H {lx} {ly1} 50  0000 L CNN
F 2 "Resistor_SMD:R_0402_1005Metric" H {cx} {cy} 50  0001 C CNN
F 3 "~" H {cx} {cy} 50  0001 C CNN
\t1    {cx} {cy}
\t1    0    0    -1
$EndComp
"""

GNDFMT = """$Comp
L power:GND {ref}
U 1 1 {uid}
P {x} {y}
F 0 "{ref}" H {x} {fy0} 50  0001 C CNN
F 1 "GND" H {x} {fy1} 50  0000 C CNN
F 2 "" H {x} {y} 50  0001 C CNN
F 3 "" H {x} {y} 50  0001 C CNN
\t1    {x} {y}
\t1    0    0    -1
$EndComp
"""

WIRE = "Wire Wire Line\n\t{x1} {y1} {x2} {y2}\n"

uid = 0x43  # next after 6C000042
new_blocks = []

for i, (name, Px, Py, xoff, rtop_val, rbot_val, rtop_ref, rbot_ref) in enumerate(STAGES):
    x   = Px + xoff
    # R_top: pin1=VOUT=(x,Py-150), pin2=(x,Py+150)
    cx1, cy1 = x, Py
    # R_bot: pin1=FB=(x,Py+300), pin2=(x,Py+600)
    cx2, cy2 = x, Py + 450
    gnd_y = Py + 600

    rtop_uid = f"6C{uid:06X}"; uid += 1
    rbot_uid = f"6C{uid:06X}"; uid += 1
    gnd_uid  = f"6C{uid:06X}"; uid += 1
    gnd_ref  = f"#PWR{0x55 + i:03X}".replace('X','').replace('PWR0','PWR0')
    # simpler:
    gnd_ref  = f"#PWRFB{i+1:02d}"

    new_blocks.append(RFMT.format(
        ref=rtop_ref, uid=rtop_uid, cx=cx1, cy=cy1,
        lx=cx1+50, ly0=cy1-150, ly1=cy1, val=rtop_val))
    new_blocks.append(RFMT.format(
        ref=rbot_ref, uid=rbot_uid, cx=cx2, cy=cy2,
        lx=cx2+50, ly0=cy2-150, ly1=cy2, val=rbot_val))
    new_blocks.append(WIRE.format(x1=x, y1=Py+150, x2=x, y2=Py+300))
    new_blocks.append(GNDFMT.format(
        ref=gnd_ref, uid=gnd_uid, x=x, y=gnd_y,
        fy0=gnd_y+50, fy1=gnd_y+150))

with open(SCH) as f:
    content = f.read()

md5_before = hashlib.md5(content.encode()).hexdigest()
assert '$EndSCHEMATC' in content
insert = ''.join(new_blocks)
content = content.replace('$EndSCHEMATC', insert + '$EndSCHEMATC')

shutil.copy2(SCH, BAK)
with open(SCH + '.tmp', 'w') as f:
    f.write(content)
os.replace(SCH + '.tmp', SCH)

with open(SCH) as f:
    md5_after = hashlib.md5(f.read().encode()).hexdigest()
print(f"Before: {md5_before}\nAfter:  {md5_after}")
print(f"Added {len(STAGES)*3} components + {len(STAGES)} wires.")
