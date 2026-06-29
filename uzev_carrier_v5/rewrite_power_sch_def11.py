#!/usr/bin/env python3
"""
rewrite_power_sch_def11.py
DEF-11: Complete rewrite of power.sch with Architecture B two-stage power.
  B1-B4: TPS54320 (sync buck 3A) + L1-L4: TPS7A85 (LDO 4A)
  B5: TPS54531 (5A buck direct) for FMC_3P3V — no LDO.
Sequencing: SOM_PG_OUT -> Buck EN -> Buck PG -> LDO EN.
Atomic write via .tmp + os.replace.
"""
import os, hashlib, sys

SCH = '/home/arc/projects/uzev_carrier_v5/power.sch'
EXPECTED_MD5  = 'a5dcd58d428b5b819cb387695ad11aaf'
EXPECTED_SIZE = 23484

def file_md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()

sz  = os.path.getsize(SCH)
md5 = file_md5(SCH)
if sz != EXPECTED_SIZE or md5 != EXPECTED_MD5:
    print(f'PREFLIGHT FAIL: expected size={EXPECTED_SIZE} md5={EXPECTED_MD5}')
    print(f'                actual   size={sz} md5={md5}')
    sys.exit(1)
print(f'PREFLIGHT OK: size={sz} md5={md5}')

# ── UID counter ───────────────────────────────────────────────────────────────
_uid = [0x6C000001]
def uid():
    u = _uid[0]; _uid[0] += 1
    return f'{u:08X}'

# ── refdes counters ───────────────────────────────────────────────────────────
_b = [1]; _l = [1]; _c = [1]; _g = [1]; _f = [1]
def B():  r = f'B{_b[0]}';  _b[0] += 1; return r
def L():  r = f'L{_l[0]}';  _l[0] += 1; return r
def C():  r = f'C{_c[0]}';  _c[0] += 1; return r
def G():  r = f'#PWR{_g[0]:03d}'; _g[0] += 1; return r
def FL(): r = f'#FLG_P{_f[0]:02d}'; _f[0] += 1; return r

C_0402 = 'Capacitor_SMD:C_0402_1005Metric'
C_0805 = 'Capacitor_SMD:C_0805_2012Metric'
C_1210 = 'Capacitor_SMD:C_1210_3225Metric'
FP_BUCK_TPS54320  = 'Package_DFN_QFN:VQFN-14-1EP_3.5x4.5mm_P0.65mm_EP2.1x3.1mm'
FP_BUCK_TPS54531  = 'Package_TO_SOT_SMD:PowerPAD_SO-8_EP_3.9x4.9mm_P1.27mm'
FP_LDO_TPS7A85    = 'Package_DFN_QFN:VQFN-20-1EP_3.5x3.5mm_P0.5mm_EP2.1x2.1mm'

# ── primitive generators ───────────────────────────────────────────────────────
def W(x1,y1,x2,y2): return f'Wire Wire Line\n\t{x1} {y1} {x2} {y2}\n'
def J(x,y):         return f'Connection ~ {x} {y}\n'
def NC(x,y):        return f'NoConn ~ {x} {y}\n'
def GL(x,y,d,sz,kind,name): return f'Text GLabel {x} {y} {d}    {sz}   {kind} ~ 0\n{name}\n'
def NL(x,y,name):   return f'Text Label {x} {y} 0 40 ~ 0\n{name}\n'
def TN(x,y,sz,txt): return f'Text Notes {x} {y} 0    {sz}   ~ 0\n{txt}\n'

def _comp(lib, ref, val, fp, px, py, f0x=None, f0y=None, f1x=None, f1y=None):
    f0x = f0x if f0x is not None else px+50
    f0y = f0y if f0y is not None else py-200
    f1x = f1x if f1x is not None else px+50
    f1y = f1y if f1y is not None else py+200
    return (f'$Comp\nL {lib} {ref}\nU 1 1 {uid()}\nP {px} {py}\n'
            f'F 0 "{ref}" H {f0x} {f0y} 50  0000 L CNN\n'
            f'F 1 "{val}" H {f1x} {f1y} 50  0000 L CNN\n'
            f'F 2 "{fp}" H {px} {py} 50  0001 C CNN\n'
            f'F 3 "" H {px} {py} 50  0001 C CNN\n'
            f'\t1    0    0    -1  \n$EndComp\n')

def gnd(ref, px, py):
    return (f'$Comp\nL power:GND {ref}\nU 1 1 {uid()}\nP {px} {py}\n'
            f'F 0 "{ref}" H {px} {py+50} 50  0001 C CNN\n'
            f'F 1 "GND" H {px} {py+150} 50  0000 C CNN\n'
            f'F 2 "" H {px} {py} 50  0001 C CNN\n'
            f'F 3 "" H {px} {py} 50  0001 C CNN\n'
            f'\t1    0    0    -1  \n$EndComp\n')

def pwr_flag(ref, px, py):
    return (f'$Comp\nL power:PWR_FLAG {ref}\nU 1 1 {uid()}\nP {px} {py}\n'
            f'F 0 "{ref}" H {px} {py+25} 50  0001 C CNN\n'
            f'F 1 "PWR_FLAG" H {px} {py+75} 50  0000 C CNN\n'
            f'F 2 "" H {px} {py} 50  0001 C CNN\n'
            f'F 3 "~" H {px} {py} 50  0001 C CNN\n'
            f'\t1    0    0    -1  \n$EndComp\n')

def cap(ref, val, fp, px, py):
    return _comp('Device:C', ref, val, fp, px, py,
                 f0x=px+50, f0y=py-150, f1x=px+50, f1y=py+150)

def buck_comp(ref, val, fp, px, py):
    return _comp('UZEV_Connectors:Buck_ENPG', ref, val, fp, px, py,
                 f0x=px+50, f0y=py-350, f1x=px+50, f1y=py+350)

def ldo_comp(ref, val, fp, px, py):
    return _comp('UZEV_Connectors:LDO_ENPG', ref, val, fp, px, py,
                 f0x=px+50, f0y=py-300, f1x=px+50, f1y=py+300)

# ── cap helper: vertical cap on a horizontal net wire ─────────────────────────
# Net wire runs at y=net_y. Cap is centered at (cx, net_y+300).
# Pin 1 (top) at (cx, net_y+200) -- wire from (cx, net_y) down to pin 1.
# Pin 2 (bot) at (cx, net_y+400) -- wire to GND at (cx, net_y+500).
# Returns (component block, wires, gnd block) as one string.
def cap_on_net(val, fp, net_y, cx):
    ref = C(); gref = G()
    out  = cap(ref, val, fp, cx, net_y + 300)
    out += W(cx, net_y,     cx, net_y + 200)  # net -> cap pin1
    out += W(cx, net_y+400, cx, net_y + 500)  # cap pin2 -> GND
    out += gnd(gref, cx, net_y + 500)
    out += J(cx, net_y)
    return out

# ── two-stage rail ────────────────────────────────────────────────────────────
# Buck symbol pin conn-points (AR 1 0 0 -1):
#   VIN=(Bx-500, Y-150)  EN=(Bx-500, Y+100)
#   VOUT=(Bx+500,Y-150)  PG=(Bx+500, Y+100)
#   GND=(Bx, Y+500)
# LDO symbol pin conn-points:
#   VIN=(Lx-450, Y-150)  EN=(Lx-450, Y+100)
#   VOUT=(Lx+450,Y-150)  PG=(Lx+450, Y+100)
#   GND=(Lx, Y+450)

def two_stage_rail(title, rail_net, inter_net,
                   buck_val, buck_fp, ldo_val,
                   Bx, Lx, Y, extra=''):
    """Generate a full two-stage (Buck+LDO) rail section."""
    bref = B(); lref = L()
    flg  = FL()

    VIN_X   = Bx - 900   # VIN GLabel x
    SOM_X   = Bx - 900   # SOM_PG_OUT GLabel x
    CIN_X   = Bx - 700   # Input cap x
    CINT_X  = (Bx + 500 + Lx - 450) // 2  # Intermediate cap (midpoint)
    COUT_X  = Lx + 650   # Output cap x
    RAIL_X  = Lx + 900   # Rail output GLabel x

    NET_Y   = Y - 150    # main power line y
    EN_Y    = Y + 100    # enable line y

    out = []
    out.append(TN(VIN_X, Y - 550, 60, title))

    # Components
    out.append(buck_comp(bref, buck_val, buck_fp, Bx, Y))
    out.append(ldo_comp(lref,  ldo_val,  FP_LDO_TPS7A85, Lx, Y))
    out.append(pwr_flag(flg, COUT_X, NET_Y))

    # GLabels
    out.append(GL(VIN_X,  NET_Y, 0, 50, 'Input',  'VIN'))
    out.append(GL(SOM_X,  EN_Y,  0, 50, 'Input',  'SOM_PG_OUT'))
    out.append(GL(RAIL_X, NET_Y, 2, 50, 'Output', rail_net))

    # Intermediate net label at midpoint
    out.append(NL(CINT_X - 150, NET_Y - 80, inter_net))

    # ── VIN input wiring ──────────────────────────────────────────────────────
    # GLabel(VIN_X,NET_Y) -- wire -- Cin tap -- wire -- Buck VIN (Bx-500, NET_Y)
    out.append(W(VIN_X,   NET_Y, CIN_X,   NET_Y))
    out.append(W(CIN_X,   NET_Y, Bx - 500, NET_Y))
    out.append(W(CIN_X,   NET_Y, CIN_X,   NET_Y + 200))  # tap -> cap pin1
    out.append(W(CIN_X,   NET_Y + 400, CIN_X, NET_Y + 500))  # cap pin2 -> GND
    out.append(cap('C' + str(_c[0]), '100nF', C_0402, CIN_X, NET_Y + 300)); _c[0] += 1
    out.append(gnd(G(), CIN_X, NET_Y + 500))
    out.append(J(CIN_X, NET_Y))

    # ── SOM_PG_OUT -> Buck EN ─────────────────────────────────────────────────
    out.append(W(SOM_X, EN_Y, Bx - 500, EN_Y))

    # ── Buck GND ─────────────────────────────────────────────────────────────
    out.append(W(Bx, Y + 500, Bx, Y + 600))
    out.append(gnd(G(), Bx, Y + 600))

    # ── Buck VOUT -> intermediate cap -> LDO VIN ──────────────────────────────
    out.append(W(Bx + 500, NET_Y, CINT_X, NET_Y))
    out.append(W(CINT_X, NET_Y, Lx - 450, NET_Y))
    out.append(W(CINT_X, NET_Y, CINT_X, NET_Y + 200))  # tap -> cap pin1
    out.append(W(CINT_X, NET_Y + 400, CINT_X, NET_Y + 500))
    out.append(cap('C' + str(_c[0]), '47uF', C_1210, CINT_X, NET_Y + 300)); _c[0] += 1
    out.append(gnd(G(), CINT_X, NET_Y + 500))
    out.append(J(CINT_X, NET_Y))

    # ── Buck PG -> LDO EN ────────────────────────────────────────────────────
    out.append(W(Bx + 500, EN_Y, Lx - 450, EN_Y))

    # ── LDO GND ──────────────────────────────────────────────────────────────
    out.append(W(Lx, Y + 450, Lx, Y + 550))
    out.append(gnd(G(), Lx, Y + 550))

    # ── LDO VOUT -> output cap -> Rail GLabel ────────────────────────────────
    out.append(W(Lx + 450, NET_Y, COUT_X, NET_Y))
    out.append(W(COUT_X, NET_Y, RAIL_X, NET_Y))
    out.append(W(COUT_X, NET_Y, COUT_X, NET_Y + 200))  # tap -> cap pin1
    out.append(W(COUT_X, NET_Y + 400, COUT_X, NET_Y + 500))
    out.append(cap('C' + str(_c[0]), '10uF', C_0805, COUT_X, NET_Y + 300)); _c[0] += 1
    out.append(gnd(G(), COUT_X, NET_Y + 500))
    out.append(J(COUT_X, NET_Y))

    # LDO PG no-connect
    out.append(NC(Lx + 450, EN_Y))

    out.append(extra)
    return ''.join(out)


def fmc_rail(title, rail_net, buck_val, Bx, Y):
    """Single-stage TPS54531 buck for FMC_3P3V."""
    bref = B(); flg = FL()

    VIN_X  = Bx - 900
    SOM_X  = Bx - 900
    CIN_X  = Bx - 700
    COUT_X = Bx + 700
    RAIL_X = Bx + 900

    NET_Y  = Y - 150
    EN_Y   = Y + 100

    out = []
    out.append(TN(VIN_X, Y - 600, 60, title))
    out.append(TN(VIN_X, Y - 420, 35,
        'Direct buck, no LDO (FMC is digital — no noise spec, VITA57.1 only needs +-5%)'))

    out.append(buck_comp(bref, buck_val, FP_BUCK_TPS54531, Bx, Y))
    out.append(pwr_flag(flg, COUT_X, NET_Y))

    out.append(GL(VIN_X,  NET_Y, 0, 50, 'Input',  'VIN'))
    out.append(GL(SOM_X,  EN_Y,  0, 50, 'Input',  'SOM_PG_OUT'))
    out.append(GL(RAIL_X, NET_Y, 2, 50, 'Output', rail_net))

    # VIN wiring
    out.append(W(VIN_X, NET_Y, CIN_X,    NET_Y))
    out.append(W(CIN_X, NET_Y, Bx - 500, NET_Y))
    out.append(W(CIN_X, NET_Y, CIN_X,    NET_Y + 200))
    out.append(W(CIN_X, NET_Y + 400, CIN_X, NET_Y + 500))
    out.append(cap('C' + str(_c[0]), '100nF', C_0402, CIN_X, NET_Y + 300)); _c[0] += 1
    out.append(gnd(G(), CIN_X, NET_Y + 500))
    out.append(J(CIN_X, NET_Y))

    # SOM_PG_OUT -> EN
    out.append(W(SOM_X, EN_Y, Bx - 500, EN_Y))

    # Buck GND
    out.append(W(Bx, Y + 500, Bx, Y + 600))
    out.append(gnd(G(), Bx, Y + 600))

    # VOUT -> Cout -> Rail GLabel
    out.append(W(Bx + 500, NET_Y, COUT_X, NET_Y))
    out.append(W(COUT_X, NET_Y, RAIL_X, NET_Y))
    out.append(W(COUT_X, NET_Y, COUT_X, NET_Y + 200))
    out.append(W(COUT_X, NET_Y + 400, COUT_X, NET_Y + 500))
    out.append(cap('C' + str(_c[0]), '47uF', C_1210, COUT_X, NET_Y + 300)); _c[0] += 1
    out.append(gnd(G(), COUT_X, NET_Y + 500))
    out.append(J(COUT_X, NET_Y))

    # PG no-connect
    out.append(NC(Bx + 500, EN_Y))

    return ''.join(out)


# ── VIN input section ─────────────────────────────────────────────────────────
def vin_section():
    out = []
    out.append(TN(1000, 800,  100, 'SHEET 2: POWER RAIL DESIGN (DEF-11 Rev 2.0)'))
    out.append(TN(1000, 1100, 40,  'Architecture B: 12V->Buck(pre-reg)->LDO for noise-sensitive rails'))
    out.append(TN(1000, 1400, 40,  'FMC_3P3V: 12V->Buck direct (digital, no noise spec)'))
    out.append(TN(1000, 1700, 40,  'Sequencing: SOM_PG_OUT->Buck EN->Buck PG->LDO EN'))
    out.append(TN(1000, 2000, 50,  'CRITICAL: VCCO_HP_65 = VADJ = 1.8V FIXED. Never adjustable.'))
    out.append(TN(2000, 2550, 60,  '=== VIN: 12V Input Power ==='))
    out.append(TN(1450, 2700, 35,
        'Barrel jack -> VIN -> J1 pins A43,A46,A49,A50,B44,B47,B50,C50'))

    # Barrel jack J5
    J5 = 'UZEV_Connectors:Barrel_Jack'
    out.append(_comp(J5, 'J5', '12V_DC_IN',
        'Connector_BarrelJack:BarrelJack_Horizontal', 2000, 3000))

    # Input bulk + bypass caps on VIN line at y=2900
    out.append(cap('C4', '33uF',  C_1210, 2800, 3200))
    out.append(cap('C5', '33uF',  C_1210, 3200, 3200))
    out.append(cap('C6', '100nF', C_0402, 3600, 3200))
    out.append(gnd('#PWR001', 2800, 3500))
    out.append(gnd('#PWR002', 3200, 3500))
    out.append(gnd('#PWR003', 3600, 3500))
    out.append(gnd('#PWR004', 2400, 3100))
    out.append(pwr_flag('#FLG_V01', 3000, 2900))
    out.append(GL(4000, 2900, 2, 50, 'Output', 'VIN'))

    out.append(W(2400, 2900, 2800, 2900))
    out.append(W(2800, 2900, 3200, 2900))
    out.append(W(3200, 2900, 3600, 2900))
    out.append(W(3600, 2900, 4000, 2900))
    out.append(W(2800, 3100, 2800, 2900))
    out.append(W(2800, 3300, 2800, 3500))
    out.append(W(3200, 3100, 3200, 2900))
    out.append(W(3200, 3300, 3200, 3500))
    out.append(W(3600, 3100, 3600, 2900))
    out.append(W(3600, 3300, 3600, 3500))
    out.append(J(2800, 2900))
    out.append(J(3200, 2900))
    out.append(J(3600, 2900))

    out.append(TN(2000, 4150, 50,  '=== SOM_PG_OUT Enable ==='))
    out.append(TN(2000, 4400, 35,
        'SOM_PG_OUT open-drain. HIGH when SOM power good. Gates all buck ENs.'))
    out.append(TN(2000, 4600, 35,
        'Buck PWRGD then gates each LDO EN for proper two-stage sequencing.'))

    return ''.join(out)


# ── MGTVCCAUX section ──────────────────────────────────────────────────────────
def mgtvccaux_section(Y=12800):
    """MGTVCCAUX tied to VCCO_HP_65 — same 1.8V net, no separate regulator."""
    NET_Y = Y
    X1 = 1000; X2 = 4000
    CX1 = 1800; CX2 = 2600

    out = []
    out.append(TN(X1, Y - 400, 50, '=== MGTVCCAUX: 1.8V (GT Auxiliary) ==='))
    out.append(TN(X1, Y - 200, 35, 'Shared with VCCO_HP_65 (same 1.8V). No separate regulator.'))

    out.append(GL(X1, NET_Y, 0, 50, 'Input',  'VCCO_HP_65'))
    out.append(GL(X2, NET_Y, 2, 50, 'Output', 'MGTVCCAUX'))
    out.append(W(X1, NET_Y, CX1, NET_Y))
    out.append(W(CX1, NET_Y, CX2, NET_Y))
    out.append(W(CX2, NET_Y, X2, NET_Y))

    # 4.7uF bulk at CX1
    out.append(cap('C' + str(_c[0]), '4.7uF', C_0805, CX1, NET_Y + 300)); _c[0] += 1
    out.append(W(CX1, NET_Y, CX1, NET_Y + 200))   # net -> cap pin1
    out.append(W(CX1, NET_Y + 400, CX1, NET_Y + 500))  # cap pin2 -> GND
    out.append(gnd(G(), CX1, NET_Y + 500))
    out.append(J(CX1, NET_Y))

    # 100nF bypass at CX2
    out.append(cap('C' + str(_c[0]), '100nF', C_0402, CX2, NET_Y + 300)); _c[0] += 1
    out.append(W(CX2, NET_Y, CX2, NET_Y + 200))
    out.append(W(CX2, NET_Y + 400, CX2, NET_Y + 500))
    out.append(gnd(G(), CX2, NET_Y + 500))
    out.append(J(CX2, NET_Y))

    return ''.join(out)


# ── design notes ──────────────────────────────────────────────────────────────
def design_notes(Y=13700):
    out = []
    out.append(TN(1000, Y,      60, '=== DESIGN NOTES ==='))
    out.append(TN(1000, Y+300,  40, '1. TPS54320 (B1-B4): 3A sync buck Vin=4.5-17V; set via R-divider'))
    out.append(TN(1000, Y+600,  40, '2. TPS54531 (B5): 5A buck Vin=3.5-28V; direct to FMC_3P3V=3.3V'))
    out.append(TN(1000, Y+900,  40, '3. TPS7A85 (L1-L4): 4A LDO 4.4uVrms VQFN-20 ANY-OUT pin-strap'))
    out.append(TN(1000, Y+1200, 40, '4. Pre-reg voltages: MGTAVCC=1.5V MGTAVTT=1.8V VCCO65/64=2.5V'))
    out.append(TN(1000, Y+1500, 40, '5. VADJ = VCCO_HP_65 = 1.8V FIXED (protects Bank 65 FPGA I/Os)'))
    out.append(TN(1000, Y+1800, 40, '6. MGTVCCAUX shared with VCCO_HP_65 (both 1.8V, same net)'))
    out.append(TN(1000, Y+2100, 40, '7. SOM_RESET_IN_N (JX1.A2): hold LOW until all rails stable (Sheet 4)'))
    return ''.join(out)


# ── assemble schematic ────────────────────────────────────────────────────────
# Layout:
#   Left  side (x ~1000-9500): MGTAVCC Y=5500, MGTAVTT Y=8200, VCCO_HP_65 Y=10900
#   Right side (x ~11500-19500): VCCO_HP_64 Y=5500, FMC_3P3V Y=8200
BX_L = 3500; LX_L = 7500   # left buck / LDO X centres
BX_R = 13500; LX_R = 17500 # right buck / LDO X centres

body = []
body.append(vin_section())

# ── Left column ───────────────────────────────────────────────────────────────

body.append(two_stage_rail(
    '=== MGTAVCC: 0.9V (GT Transceiver Core) | JX2: C1,C2,D4,D7,D10,D13 ===',
    'MGTAVCC', 'VMGTAVCC_PRE',
    'TPS54320', FP_BUCK_TPS54320, 'TPS7A85',
    BX_L, LX_L, 5500))

body.append(two_stage_rail(
    '=== MGTAVTT: 1.2V (GT Termination) | JX2: A1,A2,B4,B7,B10,B13 ===',
    'MGTAVTT', 'VMGTAVTT_PRE',
    'TPS54320', FP_BUCK_TPS54320, 'TPS7A85',
    BX_L, LX_L, 8200))

# VCCO_HP_65 needs VADJ alias — inject as extra wiring after the rail
VCCO65_Y     = 10900
VCCO65_NET_Y = VCCO65_Y - 150  # 10750
VCCO65_RAIL_X = LX_L + 900     # 8400
VADJ_Y       = VCCO65_NET_Y + 200  # 10950

vcco65_extra = (
    W(VCCO65_RAIL_X, VCCO65_NET_Y, VCCO65_RAIL_X, VADJ_Y) +  # vertical branch to VADJ
    J(VCCO65_RAIL_X, VCCO65_NET_Y) +                          # T-junction at output node
    GL(VCCO65_RAIL_X, VADJ_Y, 2, 50, 'Output', 'VADJ') +
    TN(VCCO65_RAIL_X + 100, VADJ_Y + 50, 35,
       'VADJ = VCCO_HP_65 (same net, 1.8V fixed)')
)

body.append(two_stage_rail(
    '=== VCCO_HP_65: 1.8V (Bank 65 + FMC VADJ) | JX1: C3,D3,D4 ===',
    'VCCO_HP_65', 'VVCCO65_PRE',
    'TPS54320', FP_BUCK_TPS54320, 'TPS7A85',
    BX_L, LX_L, VCCO65_Y,
    extra=vcco65_extra))

body.append(mgtvccaux_section(Y=12800))

# ── Right column ──────────────────────────────────────────────────────────────

body.append(two_stage_rail(
    '=== VCCO_HP_64: 1.8V (Bank 64 Expansion) | JX1: A3,B3,B4 ===',
    'VCCO_HP_64', 'VVCCO64_PRE',
    'TPS54320', FP_BUCK_TPS54320, 'TPS7A85',
    BX_R, LX_R, 5500))

body.append(fmc_rail(
    '=== FMC_3P3V: 3.3V (FMC Card Peripherals) | J4: 3P3V pins ===',
    'FMC_3P3V', 'TPS54531',
    BX_R, 8200))

body.append(design_notes(Y=13700))

# ── write schematic file ──────────────────────────────────────────────────────
header = (
    'EESchema Schematic File Version 4\n'
    'EELAYER 30 0\n'
    'EELAYER END\n'
    '$Descr A2 23386 16535\n'
    'encoding utf-8\n'
    'Sheet 3 5\n'
    'Title "Sheet 2: Power"\n'
    'Date "2026-04-27"\n'
    'Rev "2.0"\n'
    'Comp "ADRV9009 + UltraZed-EV Carrier Board"\n'
    'Comment1 "DEF-11: Architecture B two-stage power redesign"\n'
    'Comment2 "TPS54320+TPS7A85 for MGT/VCCO | TPS54531 direct for FMC"\n'
    'Comment3 ""\n'
    'Comment4 ""\n'
    '$EndDescr\n'
)

content = header + ''.join(body) + '$EndSCHEMATC\n'

tmp = SCH + '.tmp'
with open(tmp, 'w') as f:
    f.write(content)
os.replace(tmp, SCH)

new_sz  = os.path.getsize(SCH)
new_md5 = file_md5(SCH)
print(f'\nAFTER: size={new_sz} md5={new_md5}')
print('DONE')
