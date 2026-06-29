#!/usr/bin/env python3
"""DEC-034 Step 2: Add external buck converter components to power.sch.

Adds per-buck: IND (4.7uH), C_BOOT (100nF), R_COMP, C_COMP, C_HF,
R_RT (B1-B4 only), C_SS, D1 catch diode (B5 only).
Total: 35 passives + 1 diode + 20 GND symbols.
"""
import os, hashlib, sys

PROJ = os.path.dirname(os.path.abspath(__file__))
SCH  = os.path.join(PROJ, 'power.sch')
PRE_MD5 = '126da442c9bdf1cb99d62f1e8e0778c3'

# ── pre-condition ─────────────────────────────────────────────────────────────
actual = hashlib.md5(open(SCH, 'rb').read()).hexdigest()
if actual != PRE_MD5:
    print(f'PRE-CHECK FAILED: md5={actual} expected={PRE_MD5}')
    sys.exit(1)
content = open(SCH).read()
if '$EndSCHEMATC' not in content:
    print('PRE-CHECK FAILED: $EndSCHEMATC not found')
    sys.exit(1)
print('Pre-check OK')

# ── footprints / orientations ─────────────────────────────────────────────────
FP_CAP  = 'Capacitor_SMD:C_0402_1005Metric'
FP_RES  = 'Resistor_SMD:R_0402_1005Metric'
FP_IND  = 'Inductor_SMD:L_1210_3225Metric'
FP_DIOD = 'Diode_SMD:D_SOD-123'

# KiCad 5 2×2 transform matrices (line after position in $Comp)
STD   = '1    0    0    -1'    # [1,0,0,-1] normal
IND_H = '0    1    -1   0'     # [0,1,-1,0] horizontal inductor
DIOD_V= '0    1    1    0'     # [0,1,1,0]  vertical diode K-up

# ── block builders ────────────────────────────────────────────────────────────
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
        f'\tSTD\n'
        f'$EndComp'
    ).replace('\tSTD\n', f'\t{STD}\n')

def wire(x1, y1, x2, y2):
    return f'Wire Wire Line\n\t{x1} {y1} {x2} {y2}'

def jct(x, y):   return f'Connection ~ {x} {y}'
def nc(x, y):    return f'NoConn ~ {x} {y}'

# ── counters ──────────────────────────────────────────────────────────────────
_stamp = [0x6C00005E]
_gnd   = [42]          # #PWR042 … #PWR061

def nxt_stamp():
    s = f'{_stamp[0]:08X}'
    _stamp[0] += 1
    return s

def nxt_gnd():
    r = f'#PWR{_gnd[0]:03d}'
    _gnd[0] += 1
    return r

# ── per-buck data ─────────────────────────────────────────────────────────────
#   px,py = Buck_ENPG placement;  pin equations (transform [1,0,0,-1]):
#     SW   = (px+500, py-350)
#     BOOT = (px,     py-650)
#     COMP = (px-500, py+250)
#     RT   = (px-500, py+400)
#     SS   = (px+200, py+650)

bucks = [
    # ref   px      py     has_rt  has_diode  r_comp   c_comp    c_hf
    ('B1',  3500,  5500,   True,   False,   '1.78k', '15nF',   '330pF'),
    ('B2',  3500,  8200,   True,   False,   '1.78k', '15nF',   '330pF'),
    ('B3',  3500, 10900,   True,   False,   '1.78k', '15nF',   '330pF'),
    ('B4', 13500,  5500,   True,   False,   '1.78k', '15nF',   '330pF'),
    ('B5', 13500,  8200,   False,  True,    '37.4k', '2200pF', '22pF'),
]

# running ref numbers
ind_n  = [1]
cbt_n  = [20]   # C_BOOT: C20-C24
rcp_n  = [31]   # R_COMP: R31-R35
ccp_n  = [25]   # C_COMP: C25-C29
chf_n  = [30]   # C_HF:   C30-C34
rrt_n  = [36]   # R_RT:   R36-R39
css_n  = [35]   # C_SS:   C35-C39

blks = []

for (bref, px, py, has_rt, has_diode, r_comp_val, c_comp_val, c_hf_val) in bucks:

    # ── IND  (Device:L, horizontal [0,1,-1,0]) ────────────────────────────────
    # pin2-left = SW = (px+500, py-350), pin1-right = (px+800, py-350)
    icx, icy = px+650, py-350
    ind_ref = f'IND{ind_n[0]}';  ind_n[0] += 1
    blks.append(comp('Device:L', ind_ref, nxt_stamp(),
                     icx, icy, IND_H,
                     icx+50,  icy+100,
                     icx+50,  icy-75, '4.7uH', FP_IND))
    # IND pin1 → pre-reg bus (Py-150)
    blks.append(wire(px+800, py-350, px+800, py-150))
    blks.append(jct(px+800, py-150))
    # C_BOOT wire → SW node
    blks.append(wire(px, py-350, px+500, py-350))
    blks.append(jct(px+500, py-350))   # SW pin + IND pin2 + C_BOOT wire

    # ── C_BOOT (Device:C standard, pin1-top=BOOT, pin2-bottom→SW wire) ────────
    # center=(px, py-500); pin1=(px,py-650)=BOOT; pin2=(px,py-350)
    cbcx, cbcy = px, py-500
    cbt_ref = f'C{cbt_n[0]}';  cbt_n[0] += 1
    blks.append(comp('Device:C', cbt_ref, nxt_stamp(),
                     cbcx, cbcy, STD,
                     cbcx+50, cbcy-150,
                     cbcx+50, cbcy+150, '100nF', FP_CAP))

    # ── COMP routing: COMP-pin → left → down → far-left ──────────────────────
    # Bottom COMP wire at y=py+350; avoids R_RT body (pin1 at py+400)
    blks.append(wire(px-500, py+250, px-600, py+250))
    blks.append(wire(px-600, py+250, px-600, py+350))
    blks.append(wire(px-600, py+350, px-1900, py+350))
    blks.append(jct(px-1700, py+350))          # R_COMP pin1 tap

    # ── R_COMP (Device:R, pin1-top at py+350, pin2-bottom at py+650) ─────────
    rcx, rcy = px-1700, py+500
    rcp_ref = f'R{rcp_n[0]}';  rcp_n[0] += 1
    blks.append(comp('Device:R', rcp_ref, nxt_stamp(),
                     rcx, rcy, STD,
                     rcx+50, rcy-150,
                     rcx+50, rcy, r_comp_val, FP_RES, f3='"~"'))

    # ── C_COMP (Device:C, pin1-top=R_COMP pin2 at py+650, pin2-bottom) ───────
    ccx, ccy = px-1700, py+800
    ccp_ref = f'C{ccp_n[0]}';  ccp_n[0] += 1
    blks.append(comp('Device:C', ccp_ref, nxt_stamp(),
                     ccx, ccy, STD,
                     ccx+50, ccy-150,
                     ccx+50, ccy+150, c_comp_val, FP_CAP))
    blks.append(wire(px-1700, py+950, px-1700, py+1150))
    blks.append(gnd(nxt_gnd(), nxt_stamp(), px-1700, py+1150))

    # ── C_HF  (Device:C, pin1-top=COMP wire end at py+350) ───────────────────
    hfx, hfy = px-1900, py+500
    chf_ref = f'C{chf_n[0]}';  chf_n[0] += 1
    blks.append(comp('Device:C', chf_ref, nxt_stamp(),
                     hfx, hfy, STD,
                     hfx+50, hfy-150,
                     hfx+50, hfy+150, c_hf_val, FP_CAP))
    blks.append(wire(px-1900, py+650, px-1900, py+850))
    blks.append(gnd(nxt_gnd(), nxt_stamp(), px-1900, py+850))

    # ── R_RT (B1-B4) / NoConn RT (B5) ────────────────────────────────────────
    if has_rt:
        rrx, rry = px-800, py+550
        rrt_ref = f'R{rrt_n[0]}';  rrt_n[0] += 1
        blks.append(comp('Device:R', rrt_ref, nxt_stamp(),
                         rrx, rry, STD,
                         rrx+50, rry-150,
                         rrx+50, rry, '100k', FP_RES, f3='"~"'))
        blks.append(wire(px-500, py+400, px-800, py+400))   # RT pin → R_RT pin1
        blks.append(wire(px-800, py+700, px-800, py+900))   # R_RT pin2 → GND
        blks.append(gnd(nxt_gnd(), nxt_stamp(), px-800, py+900))
    else:
        blks.append(nc(px-500, py+400))   # B5 RT NoConn

    # ── C_SS (Device:C, pin1-top=SS pin) ─────────────────────────────────────
    ssx, ssy = px+200, py+800
    css_ref = f'C{css_n[0]}';  css_n[0] += 1
    blks.append(comp('Device:C', css_ref, nxt_stamp(),
                     ssx, ssy, STD,
                     ssx+50, ssy-150,
                     ssx+50, ssy+150, '10nF', FP_CAP))
    blks.append(wire(px+200, py+950, px+200, py+1150))
    blks.append(gnd(nxt_gnd(), nxt_stamp(), px+200, py+1150))

    # ── D1 catch diode (B5 only, Device:D [0,1,1,0] K-up) ───────────────────
    # center=(px+500, py-200); K=(px+500,py-350)=SW; A=(px+500,py-50)
    # Wait: with [0,1,1,0]: K at lib(-150,0)→sch(dx,dy-150); A at lib(150,0)→sch(dx,dy+150)
    # We need K at (px+500,py-350): dx=px+500, dy-150=py-350 → dy=py-200
    if has_diode:
        dx, dy = px+500, py-200
        blks.append(comp('Device:D', 'D1', nxt_stamp(),
                         dx, dy, DIOD_V,
                         dx+50, dy-100,
                         dx+50, dy+100, 'CDBC540-G', FP_DIOD))
        blks.append(wire(dx, dy+150, dx, dy+350))           # A → GND wire
        blks.append(gnd(nxt_gnd(), nxt_stamp(), dx, dy+350))
        # Junction at SW already emitted in IND section above

print(f'Generated {len(blks)} items '
      f'(stamps used: {_stamp[0]-0x6C00005E}, GND symbols: {_gnd[0]-42})')

# ── post-condition sanity: all expected refs present ─────────────────────────
insertion = '\n'.join(blks) + '\n'
new_content = content.replace('$EndSCHEMATC', insertion + '$EndSCHEMATC', 1)

expected_refs = (
    [f'IND{i}' for i in range(1,6)] +
    [f'C{i}'   for i in range(20,40)] +
    [f'R{i}'   for i in range(31,40)] +
    ['D1']
)
for ref in expected_refs:
    if f'F 0 "{ref}"' not in new_content:
        print(f'POST-CHECK FAILED: {ref} not found in generated output')
        sys.exit(1)

if new_content.count('$EndSCHEMATC') != 1:
    print('POST-CHECK FAILED: $EndSCHEMATC count wrong')
    sys.exit(1)

print('Post-checks OK')

# ── atomic write ──────────────────────────────────────────────────────────────
tmp = SCH + '.tmp'
with open(tmp, 'w') as f:
    f.write(new_content)
os.replace(tmp, SCH)

post_md5 = hashlib.md5(open(SCH, 'rb').read()).hexdigest()
print(f'Done. post_md5={post_md5}  size={os.path.getsize(SCH)}')
