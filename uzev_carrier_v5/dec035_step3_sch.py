#!/usr/bin/env python3
"""DEC-035 Step 3: Replace barrel jack J5 with USB-C receptacle + HUSB238 in power.sch."""
import os, hashlib, sys, re

def remove_comp_block(content, stamp):
    """Remove a $Comp block identified by its unique stamp (U 1 1 STAMP)."""
    pat = re.compile(
        r'\$Comp\n(?:.*\n)*?U 1 1 ' + re.escape(stamp) + r'\n(?:.*\n)*?\$EndComp\n?',
        re.MULTILINE
    )
    matches = pat.findall(content)
    if len(matches) != 1:
        raise ValueError(f'stamp {stamp}: found {len(matches)} blocks (expected 1)')
    return pat.sub('', content, count=1)

PROJ = os.path.dirname(os.path.abspath(__file__))
SCH  = os.path.join(PROJ, 'power.sch')

PRE_MD5 = '7c33f35db7145168e8f9760c04a47975'

actual = hashlib.md5(open(SCH, 'rb').read()).hexdigest()
if actual != PRE_MD5:
    print(f'PRE-CHECK FAILED: md5={actual} expected={PRE_MD5}')
    sys.exit(1)

content = open(SCH).read()
print('Pre-check OK')

# ── 1. Remove J5 Barrel_Jack and #PWR04 using stamp-based removal ─────────────
try:
    content = remove_comp_block(content, '6C000001')  # J5 Barrel_Jack
    print('  Removed J5 Barrel_Jack')
    content = remove_comp_block(content, '6C000008')  # #PWR04 J5 sleeve GND
    print('  Removed #PWR04')
except ValueError as e:
    print(f'PRE-CHECK FAILED: {e}')
    sys.exit(1)

# ── 3. Remove wire: J5 Tip → VIN bus ─────────────────────────────────────────
OLD_WIRE_J5 = "Wire Wire Line\n\t2400 2900 2800 2900"
if content.count(OLD_WIRE_J5) != 1:
    print(f'PRE-CHECK FAILED: J5 tip wire found {content.count(OLD_WIRE_J5)} times')
    sys.exit(1)
content = content.replace(OLD_WIRE_J5, '', 1)

# ── 4. Update text note ───────────────────────────────────────────────────────
OLD_NOTE = "Barrel jack -> VIN -> J1 pins A43,A46,A49,A50,B44,B47,B50,C50"
NEW_NOTE = "USB-C PD (HUSB238, 12V primary/15V fallback) -> VIN -> J1 pins A43,A46,A49,A50,B44,B47,B50,C50"
if OLD_NOTE not in content:
    print('PRE-CHECK FAILED: barrel jack text note not found')
    sys.exit(1)
content = content.replace(OLD_NOTE, NEW_NOTE, 1)

print('Removals OK')

# ── helpers ───────────────────────────────────────────────────────────────────
STD = '1    0    0    -1'

def comp(sym, ref, stamp, px, py, mat,
         f0x, f0y, f1x, f1y, f1val, fp, f3='""'):
    return (
        f'$Comp\n'
        f'L {sym} {ref}\n'
        f'U 1 1 {stamp}\n'
        f'P {px} {py}\n'
        f'F 0 "{ref}" H {f0x} {f0y} 50  0000 L CNN\n'
        f'F 1 "{f1val}" H {f1x} {f1y} 50  0000 L CNN\n'
        f'F 2 "{fp}" H {px} {py} 50  0001 C CNN\n'
        f'F 3 {f3} H {px} {py} 50  0001 C CNN\n'
        f'\t1    {px} {py}\n'
        f'\t{mat}\n'
        f'$EndComp'
    )

def gnd(pwr_ref, stamp, px, py):
    return (
        f'$Comp\n'
        f'L power:GND {pwr_ref}\n'
        f'U 1 1 {stamp}\n'
        f'P {px} {py}\n'
        f'F 0 "{pwr_ref}" H {px} {py+50} 50  0001 C CNN\n'
        f'F 1 "GND" H {px} {py+150} 50  0000 C CNN\n'
        f'F 2 "" H {px} {py} 50  0001 C CNN\n'
        f'F 3 "" H {px} {py} 50  0001 C CNN\n'
        f'\t1    {px} {py}\n'
        f'\t{STD}\n'
        f'$EndComp'
    )

def wire(x1, y1, x2, y2):
    return f'Wire Wire Line\n\t{x1} {y1} {x2} {y2}'

def jct(x, y):
    return f'Connection ~ {x} {y}'

def nc(x, y):
    return f'NoConn ~ {x} {y}'

# ── 5. Build new USB-C PD input section ───────────────────────────────────────
# Stamp range: 0x6C000095 onwards (DEC-034 used up to 0x6C000094)
# GND range: #PWR062 onwards (DEC-034 used up to #PWR061)
#
# Layout (schematic coords, y increases downward):
#
#  J5 USB_C_Receptacle  P=1000,3000
#    VBUS pin1 at lib(-450,250) with STD [1,0,0,-1] → sch=(550, 2750)
#    GND  pin2 at lib(-450,100) → sch=(550, 2900)
#    CC1  pin3 at lib(-450,-50) → sch=(550, 3050)
#    CC2  pin4 at lib(-450,-200)→ sch=(550, 3200)
#    D_P–SBU2 (right side, NC)
#
#  U6 HUSB238  P=2200,3100
#    VIN  pin1 at lib(-450,200) → sch=(1750, 2900)
#    GND  pin2 at lib(-450,50)  → sch=(1750, 3050)
#    CC1  pin3 at lib(-450,-50) → sch=(1750, 3150)
#    CC2  pin4 at lib(-450,-200)→ sch=(1750, 3300)
#    VOUT pin5 at lib(450,200)  → sch=(2650, 2900) → wire to VIN bus
#    PG   pin6 at lib(450,50)   → sch=(2650, 3050) → pullup R40 → VOUT
#    CFG1 pin7 at lib(450,-50)  → sch=(2650, 3150) → GND
#    CFG2 pin8 at lib(450,-150) → sch=(2650, 3250) → GND
#    CFG3 pin9 at lib(450,-250) → sch=(2650, 3350) → GND
#
#  C7 10uF VBUS bulk: P=900,3400  pin1(top)=(900,3250) pin2(bot)=(900,3550)
#  C8 100nF VBUS HF:  P=1200,3400 pin1(top)=(1200,3250) pin2(bot)=(1200,3550)
#
#  R40 10k PG pullup: P=2950,3050 pin1(top)=(2950,2900) pin2(bot)=(2950,3200)
#    pin1 taps VOUT net at 2950,2900 (tied to VIN bus via junction)
#    pin2 connects to PG at 2650,3050 via wire
#
# VBUS net: J5-VBUS(550,2750) → wire up → (550,2750)→(900,2750) h-wire →
#   (900,2750)→(900,3250) vert → C7-pin1 junction
#   (900,2750)→(1200,2750) h-wire → C8-pin1 (1200,3250) vert
#   (1200,2750)→(1750,2750) h-wire → U6-VIN(1750,2900) vert
#
# VIN bus entry: U6-VOUT(2650,2900) → wire right → (2800,2900) → existing VIN bus

blks = []

# J5 USB-C receptacle
FP_USBC = 'UZEV_Connectors:USB_C_Receptacle_GCT_USB4135'
blks.append(comp('UZEV_Connectors:USB_C_Receptacle', 'J5', '6C000095',
                 1000, 3000, STD,
                 1050, 2800,
                 1050, 3200, 'USB4135-GF-A', FP_USBC))

# U6 HUSB238
FP_HUSB = 'UZEV_Connectors:SOT-23-9_Hynetek_HUSB238'
blks.append(comp('UZEV_Connectors:HUSB238', 'U6', '6C000096',
                 2200, 3100, STD,
                 2250, 2850,
                 2250, 3400, 'HUSB238', FP_HUSB))

# C7 10uF VBUS bulk
FP_C1210 = 'Capacitor_SMD:C_1210_3225Metric'
blks.append(comp('Device:C', 'C7', '6C000097',
                 900, 3400, STD,
                 950, 3250,
                 950, 3550, '10uF/25V', FP_C1210))

# C8 100nF VBUS HF
FP_C0402 = 'Capacitor_SMD:C_0402_1005Metric'
blks.append(comp('Device:C', 'C8', '6C000098',
                 1200, 3400, STD,
                 1250, 3250,
                 1250, 3550, '100nF/25V', FP_C0402))

# R40 10k PG pullup
FP_R0402 = 'Resistor_SMD:R_0402_1005Metric'
blks.append(comp('Device:R', 'R40', '6C000099',
                 2950, 3050, STD,
                 3000, 2900,
                 3000, 3050, '10k', FP_R0402, f3='"~"'))

# GND symbols
blks.append(gnd('#PWR062', '6C00009A', 900,  3700))   # C7 bottom
blks.append(gnd('#PWR063', '6C00009B', 1200, 3700))   # C8 bottom
blks.append(gnd('#PWR064', '6C00009C', 550,  3350))   # J5 GND pin
blks.append(gnd('#PWR065', '6C00009D', 1750, 3200))   # U6 GND pin
blks.append(gnd('#PWR066', '6C00009E', 2650, 3550))   # CFG1/2/3 common GND

# NoConn on J5 right-side pins (D_P, D_N, SBU1, SBU2)
# J5 P=1000,3000 STD; right-side pins at lib(450,200/50/-100/-250):
#   D_P  pin5 sch=(1450,2800)
#   D_N  pin6 sch=(1450,2950)
#   SBU1 pin7 sch=(1450,3100)
#   SBU2 pin8 sch=(1450,3250)
blks.append(nc(1450, 2800))
blks.append(nc(1450, 2950))
blks.append(nc(1450, 3100))
blks.append(nc(1450, 3250))

# VBUS horizontal bus at y=2750
blks.append(wire(550, 2750, 1750, 2750))   # J5-VBUS → U6-VIN top
blks.append(wire(900, 2750, 900, 3250))    # → C7 top
blks.append(wire(1200, 2750, 1200, 3250))  # → C8 top
blks.append(jct(900, 2750))
blks.append(jct(1200, 2750))

# U6 VIN vertical: VBUS bus → U6 VIN pin
blks.append(wire(1750, 2750, 1750, 2900))

# J5 GND pin: J5-GND(sch)=(550,2900) → down to #PWR064
# J5 GND pin2 at lib(-450,100) STD → sch=(550, 2900)
blks.append(wire(550, 2900, 550, 3350))

# C7 bottom → GND
blks.append(wire(900, 3550, 900, 3700))

# C8 bottom → GND
blks.append(wire(1200, 3550, 1200, 3700))

# U6 GND pin2 at sch=(1750,3050) → down
blks.append(wire(1750, 3050, 1750, 3200))

# U6 CC1 → J5 CC1: U6-CC1 sch=(1750,3150), J5-CC1 sch=(550,3050)
blks.append(wire(550, 3050, 1750, 3150))

# U6 CC2 → J5 CC2: U6-CC2 sch=(1750,3300), J5-CC2 sch=(550,3200)
blks.append(wire(550, 3200, 1750, 3300))

# U6 VOUT → VIN bus: VOUT sch=(2650,2900) → right → (2800,2900) existing bus start
blks.append(wire(2650, 2900, 2800, 2900))

# R40 PG pullup: pin1(top)=(2950,2900) → tap VOUT net; pin2(bot)=(2950,3200)→wire→PG
blks.append(wire(2650, 2900, 2950, 2900))   # VOUT net → R40 pin1
blks.append(jct(2650, 2900))                 # junction at VOUT→VIN bus→R40
blks.append(wire(2950, 3200, 2950, 3050))   # R40 pin2 down to PG level
blks.append(wire(2950, 3050, 2650, 3050))   # → U6 PG pin

# CFG1/2/3 → common GND at x=2650, y=3550
blks.append(wire(2650, 3150, 2650, 3350))   # CFG1→CFG3 vertical stub
blks.append(wire(2650, 3250, 2650, 3350))   # CFG2 tap (already covered by above, but explicit)
blks.append(wire(2650, 3350, 2650, 3550))   # → GND
blks.append(jct(2650, 3150))
blks.append(jct(2650, 3250))

print(f'Generated {len(blks)} blocks')

# ── 6. Insert before $EndSCHEMATC ────────────────────────────────────────────
insertion = '\n'.join(blks) + '\n'
if content.count('$EndSCHEMATC') != 1:
    print(f'PRE-CHECK FAILED: $EndSCHEMATC count = {content.count("$EndSCHEMATC")}')
    sys.exit(1)
new_content = content.replace('$EndSCHEMATC', insertion + '$EndSCHEMATC', 1)

# ── 7. Post-checks ────────────────────────────────────────────────────────────
for ref in ['J5', 'U6', 'C7', 'C8', 'R40']:
    if f'F 0 "{ref}"' not in new_content:
        print(f'POST-CHECK FAILED: {ref} not found')
        sys.exit(1)

for sym in ['UZEV_Connectors:USB_C_Receptacle', 'UZEV_Connectors:HUSB238']:
    if sym not in new_content:
        print(f'POST-CHECK FAILED: {sym} not found')
        sys.exit(1)

if 'Barrel_Jack' in new_content:
    print('POST-CHECK FAILED: Barrel_Jack still present')
    sys.exit(1)

if 'Connector_BarrelJack' in new_content:
    print('POST-CHECK FAILED: Connector_BarrelJack footprint still present')
    sys.exit(1)

if 'USB-C PD (HUSB238' not in new_content:
    print('POST-CHECK FAILED: updated text note not found')
    sys.exit(1)

if new_content.count('$EndSCHEMATC') != 1:
    print('POST-CHECK FAILED: $EndSCHEMATC count wrong')
    sys.exit(1)

print('Post-checks OK')

# ── 8. Atomic write ───────────────────────────────────────────────────────────
tmp = SCH + '.tmp'
with open(tmp, 'w') as f:
    f.write(new_content)
os.replace(tmp, SCH)

post_md5 = hashlib.md5(open(SCH, 'rb').read()).hexdigest()
print(f'Done. post_md5={post_md5}  size={os.path.getsize(SCH)}')
