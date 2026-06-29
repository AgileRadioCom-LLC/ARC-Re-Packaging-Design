#!/usr/bin/env python3
"""DEC-036 footprints:
  1. Delete SOT-23-9_Hynetek_HUSB238.kicad_mod
  2. Rewrite USB_C_Receptacle_GCT_USB4135.kicad_mod (correct pads per GCT drawing Rev A2)
  3. Create WQFN-38_TPS25730D.kicad_mod (REF0038A, SLVSGP9)
  4. Create HVSSOP-8_TPS7A1633.kicad_mod (DDC package, SBVS171F)
"""
import os, hashlib, sys

PROJ   = os.path.dirname(os.path.abspath(__file__))
FP_DIR = os.path.join(PROJ, 'UZEV_Connectors.pretty')

def write_fp(name, content):
    path = os.path.join(FP_DIR, name)
    tmp  = path + '.tmp'
    with open(tmp, 'w') as f:
        f.write(content)
    os.replace(tmp, path)
    print(f'  Wrote {name}  size={os.path.getsize(path)}')

# ── 1. Delete HUSB238 footprint ──────────────────────────────────────────────
husb_fp = os.path.join(FP_DIR, 'SOT-23-9_Hynetek_HUSB238.kicad_mod')
if os.path.isfile(husb_fp):
    os.remove(husb_fp)
    print('  Deleted SOT-23-9_Hynetek_HUSB238.kicad_mod')
else:
    print('  WARN: HUSB238 footprint not found (already deleted?)')

# ── 2. USB_C_Receptacle_GCT_USB4135.kicad_mod ───────────────────────────────
# Pad layout verified from GCT Drawing USB4135 Rev A2, 13/09/24.
# Coordinate origin: footprint center (X=0, Y=0).
# Y+ = toward board interior (away from connector mating face).
# Footprint total: 10.25mm wide x 6.90mm deep → Y from -3.45 to +3.45mm.
#
# Signal pads (6): all at Y=+2.775mm (pad extends to back edge +3.45mm).
# GCT drawing dimensions:
#   outer span (GND A12/B12): 5.50mm center-to-center → X = ±2.75mm
#   middle span (VBUS A9/B9): 3.04mm center-to-center → X = ±1.52mm
#   inner span (CC A5/B5):    1.00mm center-to-center → X = ±0.50mm
#   pad width: GND=0.76mm, VBUS=0.80mm, CC=0.70mm; pad length=1.35mm.
#
# Shell pads (4): pairs at corners, GND net.
#   X center = ±4.225mm  (outer edge flush with ±5.125mm courtyard)
#   pad size = 1.80mm (X) × 1.50mm (Y)
#   front pair: Y = -1.95mm;  rear pair: Y = +1.35mm

USB4135_FP = """\
(module USB_C_Receptacle_GCT_USB4135 (layer F.Cu) (tedit 20260529)
  (descr "GCT USB4135-GF-A, USB-C power-only receptacle, horizontal mid-mount SMD. Pads per GCT drawing Rev A2 13/09/24. VBUS/GND/CC1/CC2 only; D+/D-/SBU do not exist on this part.")
  (tags "USB USB-C Type-C receptacle SMD power-only")
  (fp_text reference REF** (at 0 -4.5) (layer F.SilkS) (effects (font (size 1 1) (thickness 0.15))))
  (fp_text value USB_C_Receptacle_GCT_USB4135 (at 0 4.5) (layer F.Fab) (effects (font (size 1 1) (thickness 0.15))))

  (fp_line (start -5.25 -3.60) (end  5.25 -3.60) (layer F.CrtYd) (width 0.05))
  (fp_line (start  5.25 -3.60) (end  5.25  3.60) (layer F.CrtYd) (width 0.05))
  (fp_line (start  5.25  3.60) (end -5.25  3.60) (layer F.CrtYd) (width 0.05))
  (fp_line (start -5.25  3.60) (end -5.25 -3.60) (layer F.CrtYd) (width 0.05))

  (fp_line (start -4.47 -3.45) (end  4.47 -3.45) (layer F.Fab) (width 0.10))
  (fp_line (start  4.47 -3.45) (end  4.47  3.45) (layer F.Fab) (width 0.10))
  (fp_line (start  4.47  3.45) (end -4.47  3.45) (layer F.Fab) (width 0.10))
  (fp_line (start -4.47  3.45) (end -4.47 -3.45) (layer F.Fab) (width 0.10))

  (fp_line (start -3.50 -3.45) (end -3.50 -3.60) (layer F.SilkS) (width 0.12))
  (fp_line (start -3.50 -3.60) (end  3.50 -3.60) (layer F.SilkS) (width 0.12))
  (fp_line (start  3.50 -3.60) (end  3.50 -3.45) (layer F.SilkS) (width 0.12))

  (pad 2 smd rect (at -2.75 2.775) (size 0.76 1.35) (layers F.Cu F.Paste F.Mask))
  (pad 1 smd rect (at -1.52 2.775) (size 0.80 1.35) (layers F.Cu F.Paste F.Mask))
  (pad 4 smd rect (at -0.50 2.775) (size 0.70 1.35) (layers F.Cu F.Paste F.Mask))
  (pad 3 smd rect (at  0.50 2.775) (size 0.70 1.35) (layers F.Cu F.Paste F.Mask))
  (pad 1 smd rect (at  1.52 2.775) (size 0.80 1.35) (layers F.Cu F.Paste F.Mask))
  (pad 2 smd rect (at  2.75 2.775) (size 0.76 1.35) (layers F.Cu F.Paste F.Mask))

  (pad 2 smd rect (at -4.225 -1.95) (size 1.80 1.50) (layers F.Cu F.Paste F.Mask))
  (pad 2 smd rect (at  4.225 -1.95) (size 1.80 1.50) (layers F.Cu F.Paste F.Mask))
  (pad 2 smd rect (at -4.225  1.35) (size 1.80 1.50) (layers F.Cu F.Paste F.Mask))
  (pad 2 smd rect (at  4.225  1.35) (size 1.80 1.50) (layers F.Cu F.Paste F.Mask))
)
"""

# ── 3. WQFN-38_TPS25730D.kicad_mod ─────────────────────────────────────────
# REF0038A package (SLVSGP9 packaging chapter).
# Body: 5.90mm(X) x 3.90mm(Y).  Pitch: 0.40mm.
# Pin layout (counterclockwise from pin 1 at top-left):
#   Left  (X=-3.325): pins 1-6,  Y from +1.00 to -1.00  (6 pins, 0.40mm pitch)
#   Bottom(Y=-2.325): pins 7-19, X from -2.40 to +2.40  (13 pins)
#   Right (X=+3.325): pins 20-25,Y from -1.00 to +1.00  (6 pins)
#   Top   (Y=+2.325): pins 26-38,X from +2.40 to -2.40  (13 pins)
# Peripheral pad size: 0.25mm x 0.75mm (long dim perpendicular to body edge).
# Thermal pads: GND_EP(39) 3.40x1.80mm at center; DRAIN_EP(40) 0.60x0.50mm offset.
# NOTE: Verify REF0038A thermal pad dimensions from SLVSGP9 land pattern before fab.

def wqfn38_pad(num, x, y, rx, ry):
    """SMD rect pad, no net assignment."""
    return (f'  (pad {num} smd rect (at {x:.3f} {y:.3f}) '
            f'(size {rx:.2f} {ry:.2f}) (layers F.Cu F.Paste F.Mask))\n')

lines = []
lines.append('(module WQFN-38_TPS25730D (layer F.Cu) (tedit 20260529)\n')
lines.append('  (descr "TPS25730D WQFN-38 REF0038A, 5.90x3.90mm body, 0.40mm pitch. Verified pin numbering from SLVSGP9 Table 5-1. Verify thermal pad dims from land pattern drawing before fab.")\n')
lines.append('  (tags "WQFN QFN TPS25730D USB PD sink TI")\n')
lines.append('  (fp_text reference REF** (at 0 -3.6) (layer F.SilkS) (effects (font (size 1 1) (thickness 0.15))))\n')
lines.append('  (fp_text value WQFN-38_TPS25730D (at 0 3.6) (layer F.Fab) (effects (font (size 1 1) (thickness 0.15))))\n\n')

# Courtyard: body + 0.5mm clearance
lines.append('  (fp_line (start -3.45 -2.45) (end  3.45 -2.45) (layer F.CrtYd) (width 0.05))\n')
lines.append('  (fp_line (start  3.45 -2.45) (end  3.45  2.45) (layer F.CrtYd) (width 0.05))\n')
lines.append('  (fp_line (start  3.45  2.45) (end -3.45  2.45) (layer F.CrtYd) (width 0.05))\n')
lines.append('  (fp_line (start -3.45  2.45) (end -3.45 -2.45) (layer F.CrtYd) (width 0.05))\n\n')
# Fab body outline
lines.append('  (fp_line (start -2.95 -1.95) (end  2.95 -1.95) (layer F.Fab) (width 0.10))\n')
lines.append('  (fp_line (start  2.95 -1.95) (end  2.95  1.95) (layer F.Fab) (width 0.10))\n')
lines.append('  (fp_line (start  2.95  1.95) (end -2.95  1.95) (layer F.Fab) (width 0.10))\n')
lines.append('  (fp_line (start -2.95  1.95) (end -2.95 -1.95) (layer F.Fab) (width 0.10))\n')
# Pin-1 indicator (chamfer top-left)
lines.append('  (fp_line (start -2.95 -1.60) (end -2.60 -1.95) (layer F.Fab) (width 0.10))\n\n')

# Left side: pins 1-6, X=-3.325, Y from +1.00 to -1.00
left_pins = [
    (1, 'LDO_3V3'), (2, 'ADCIN1'), (3, 'ADCIN2'), (4, 'LDO_1V5'),
    (5, 'ADCIN3'), (6, 'CAP_MIS'),
]
for i, (num, name) in enumerate(left_pins):
    y = 1.00 - i * 0.40
    lines.append(wqfn38_pad(num, -3.325, y, 0.75, 0.25))

lines.append('\n')
# Bottom: pins 7-19, Y=-2.325, X from -2.40 to +2.40
bottom_pins = [
    (7,'ADCIN4'),(8,'I2Ct_SDA'),(9,'I2Ct_SCL'),(10,'DBG_ACC'),
    (11,'GND'),(12,'GND'),(13,'PLUG_FLIP'),(14,'GND'),(15,'DRAIN'),
    (16,'GND'),(17,'GND'),(18,'FAULT_IN'),(19,'SINK_EN'),
]
for i, (num, name) in enumerate(bottom_pins):
    x = -2.40 + i * 0.40
    lines.append(wqfn38_pad(num, x, -2.325, 0.25, 0.75))

lines.append('\n')
# Right side: pins 20-25, X=+3.325, Y from -1.00 to +1.00
right_pins = [
    (20,'PPHV'),(21,'PPHV'),(22,'PPHV'),
    (23,'VBUS_IN'),(24,'VBUS_IN'),(25,'VBUS_IN'),
]
for i, (num, name) in enumerate(right_pins):
    y = -1.00 + i * 0.40
    lines.append(wqfn38_pad(num, 3.325, y, 0.75, 0.25))

lines.append('\n')
# Top: pins 26-38, Y=+2.325, X from +2.40 to -2.40
top_pins = [
    (26,'RESERVED'),(27,'RESERVED'),(28,'CC1'),(29,'CC2'),(30,'DRAIN'),
    (31,'GND'),(32,'VBUS'),(33,'VBUS'),(34,'GND'),(35,'GND'),
    (36,'RESERVED'),(37,'PLUG_EVENT'),(38,'VIN_3V3'),
]
for i, (num, name) in enumerate(top_pins):
    x = 2.40 - i * 0.40
    lines.append(wqfn38_pad(num, x, 2.325, 0.25, 0.75))

lines.append('\n')
# Thermal pads
lines.append('  (pad 39 smd rect (at 0.00 0.00) (size 3.40 1.80) (layers F.Cu F.Paste F.Mask))\n')
lines.append('  (pad 40 smd rect (at 1.20 0.00) (size 0.60 0.50) (layers F.Cu F.Paste F.Mask))\n')
lines.append(')\n')
TPS25730D_FP = ''.join(lines)

# ── 4. HVSSOP-8_TPS7A1633.kicad_mod ─────────────────────────────────────────
# DDC package (SBVS171F). Body ~3.0x3.0mm, 8 leads + exposed GND pad.
# Pitch: 0.65mm. Pad size: 0.40x1.25mm.
# Pin 1 top-left; pins 1-4 left (top→bottom); pins 5-8 right (bottom→top).
# Left pad centers: X=-2.40mm; right pad centers: X=+2.40mm.
# Y centers (4 pads): +0.975, +0.325, -0.325, -0.975mm.
# Exposed thermal pad (pin 9): 1.65x1.65mm at center.

HVSSOP8_FP = """\
(module HVSSOP-8_TPS7A1633 (layer F.Cu) (tedit 20260529)
  (descr "TPS7A1633 HVSSOP-8 DDC package, 3.0x3.0mm body, 0.65mm pitch, exposed GND thermal pad. Per SBVS171F.")
  (tags "HVSSOP SSOP TPS7A1633 LDO TI")
  (fp_text reference REF** (at 0 -3.0) (layer F.SilkS) (effects (font (size 1 1) (thickness 0.15))))
  (fp_text value HVSSOP-8_TPS7A1633 (at 0 3.0) (layer F.Fab) (effects (font (size 1 1) (thickness 0.15))))

  (fp_line (start -3.05 -1.80) (end  3.05 -1.80) (layer F.CrtYd) (width 0.05))
  (fp_line (start  3.05 -1.80) (end  3.05  1.80) (layer F.CrtYd) (width 0.05))
  (fp_line (start  3.05  1.80) (end -3.05  1.80) (layer F.CrtYd) (width 0.05))
  (fp_line (start -3.05  1.80) (end -3.05 -1.80) (layer F.CrtYd) (width 0.05))

  (fp_line (start -1.50 -1.50) (end  1.50 -1.50) (layer F.Fab) (width 0.10))
  (fp_line (start  1.50 -1.50) (end  1.50  1.50) (layer F.Fab) (width 0.10))
  (fp_line (start  1.50  1.50) (end -1.50  1.50) (layer F.Fab) (width 0.10))
  (fp_line (start -1.50  1.50) (end -1.50 -1.50) (layer F.Fab) (width 0.10))
  (fp_line (start -1.50 -1.15) (end -1.15 -1.50) (layer F.Fab) (width 0.10))

  (fp_line (start -1.50 -1.80) (end -1.50 -1.65) (layer F.SilkS) (width 0.12))
  (fp_line (start -1.50 -1.65) (end  1.50 -1.65) (layer F.SilkS) (width 0.12))
  (fp_line (start  1.50 -1.65) (end  1.50 -1.80) (layer F.SilkS) (width 0.12))

  (pad 1 smd rect (at -2.40  0.975) (size 0.40 1.25) (layers F.Cu F.Paste F.Mask))
  (pad 2 smd rect (at -2.40  0.325) (size 0.40 1.25) (layers F.Cu F.Paste F.Mask))
  (pad 3 smd rect (at -2.40 -0.325) (size 0.40 1.25) (layers F.Cu F.Paste F.Mask))
  (pad 4 smd rect (at -2.40 -0.975) (size 0.40 1.25) (layers F.Cu F.Paste F.Mask))
  (pad 5 smd rect (at  2.40 -0.975) (size 0.40 1.25) (layers F.Cu F.Paste F.Mask))
  (pad 6 smd rect (at  2.40 -0.325) (size 0.40 1.25) (layers F.Cu F.Paste F.Mask))
  (pad 7 smd rect (at  2.40  0.325) (size 0.40 1.25) (layers F.Cu F.Paste F.Mask))
  (pad 8 smd rect (at  2.40  0.975) (size 0.40 1.25) (layers F.Cu F.Paste F.Mask))
  (pad 9 smd rect (at  0.00  0.000) (size 1.65 1.65) (layers F.Cu F.Paste F.Mask))
)
"""

# ── Execute writes ───────────────────────────────────────────────────────────
write_fp('USB_C_Receptacle_GCT_USB4135.kicad_mod', USB4135_FP)
write_fp('WQFN-38_TPS25730D.kicad_mod', TPS25730D_FP)
write_fp('HVSSOP-8_TPS7A1633.kicad_mod', HVSSOP8_FP)

# Post-checks
fp_dir = os.listdir(FP_DIR)
assert 'WQFN-38_TPS25730D.kicad_mod' in fp_dir
assert 'HVSSOP-8_TPS7A1633.kicad_mod' in fp_dir
assert 'USB_C_Receptacle_GCT_USB4135.kicad_mod' in fp_dir
assert 'SOT-23-9_Hynetek_HUSB238.kicad_mod' not in fp_dir
print('Post-checks OK — all footprints in place, HUSB238 removed')
