#!/usr/bin/env python3
"""DEC-036: Append log entry to DECISIONS_LOG.md (atomic write)."""
import os, hashlib

PROJ = os.path.dirname(os.path.abspath(__file__))
LOG  = os.path.join(PROJ, 'DECISIONS_LOG.md')

PRE_MD5 = '44b2e47d94f8146dea389bb87f769320'
actual = hashlib.md5(open(LOG, 'rb').read()).hexdigest()
if actual != PRE_MD5:
    print(f'PRE-CHECK FAILED: md5={actual} expected={PRE_MD5}')
    import sys; sys.exit(1)

ENTRY = """

## 2026-05-29 — DEC-036 — Replace HUSB238 with TPS25730D USB-C PD sink + TPS7A1633 bootstrap LDO

**Status:** APPLIED

**Decision:** Remove HUSB238 (Hynetek, Chinese-made) from DEC-035 USB-C PD input section.
Replace with TPS25730D (Texas Instruments, US) + TPS7A1633 (TI) bootstrap LDO.

**Rationale:** Defense UAV supply chain requires US-made components. HUSB238 is manufactured by
Hynetek Semiconductor (Shenzhen, China). TPS25730D is a TI product (Dallas, TX, USA) with
equivalent or superior functionality: integrated PPHV power switch (no external PMOS needed),
hardware-only ADCINx strap configuration, 7A continuous / 10A pulsed VBUS sink capability.

**TPS25730D configuration (verified vs SLVSGP9, Table 8-x):**
- ADCIN1 (pin 2): 91kΩ/11kΩ divider from LDO_3V3 → value=2 → PDO min = 12V
- ADCIN2 (pin 3): wire to LDO_1V5 (pin 4) → value=5 → PDO max = 15V (Table 8-1 shortcut)
- ADCIN3 (pin 5): 82kΩ/20kΩ divider → value=3 → operating current = 3A
- ADCIN4 (pin 7): 100kΩ/4.7kΩ divider → value=1 → max current = 3A
- RESERVED (pins 26,27,36): 10kΩ each to GND per datasheet Table 5-1
- FAULT_IN (pin 18): 10kΩ pullup to LDO_3V3 (maintains connection on VBUS loss)
- CC1/CC2 (pins 28,29): 330pF filter caps to GND

**TPS7A1633 bootstrap LDO (verified vs SBVS171F):**
- Required because TPS25730D VIN_3V3 (pin 38) must be driven before PD negotiation begins.
  Without external VIN_3V3, ADCIN2=5 config means "USB PD disabled until I2C load" — dead-battery mode.
  TPS7A1633 (60V-in, 3.3V fixed, 100mA, HVSSOP-8) driven from VBUS provides VIN_3V3 at power-on,
  bypassing dead-battery mode so hardware ADCINx straps are read immediately.
- IN: VBUS rail. OUT: VIN_3V3 net → TPS25730D pin 38.
- EN: tied to IN (always-on while VBUS present).
- DELAY: 100nF cap to GND.
- DNC (pin 4): left open.

**Footprint sources:**
- TPS25730D: WQFN-38 REF0038A, 5.90×3.90mm, 0.4mm pitch (SLVSGP9 packaging chapter)
- TPS7A1633: HVSSOP-8 DDC, 3.0×3.0mm, 0.65mm pitch (SBVS171F)
- USB4135-GF-A: corrected per GCT Drawing USB4135 Rev A2 13/09/24 (6 signal pads only;
  prior footprint incorrectly included D+/D-/SBU1/SBU2 pads which do not exist on power-only connector)

**Files modified:**
- `DECISIONS_LOG.md`: this entry
- `UZEV_Connectors.lib`: removed HUSB238 symbol; updated USB_C_Receptacle (remove D+/D-/SBU pins);
  added TPS25730D (38-pin + 2 thermal) and TPS7A1633 (7-pin + thermal) symbols
- `UZEV_Connectors.pretty/SOT-23-9_Hynetek_HUSB238.kicad_mod`: deleted
- `UZEV_Connectors.pretty/USB_C_Receptacle_GCT_USB4135.kicad_mod`: corrected pad layout
  (6 signal pads per GCT drawing: VBUS×2, GND×2, CC1, CC2; 4 shell tabs)
- `UZEV_Connectors.pretty/WQFN-38_TPS25730D.kicad_mod`: added
- `UZEV_Connectors.pretty/HVSSOP-8_TPS7A1633.kicad_mod`: added
- `power.sch`: removed HUSB238 circuit (U6/C60/C61/R40/#PWR062-066 + wires/junctions/noconns);
  added TPS25730D (U6) + TPS7A1633 (U7) + all passives
- `phase7_prepcb_audit.py`: EXPECTED_HASHES updated

**Bitstream impact:** None (schematic-level change only).
"""

content = open(LOG).read()
new_content = content + ENTRY

tmp = LOG + '.tmp'
with open(tmp, 'w') as f:
    f.write(new_content)
os.replace(tmp, LOG)

post_md5 = hashlib.md5(open(LOG, 'rb').read()).hexdigest()
print(f'Done. post_md5={post_md5}  size={os.path.getsize(LOG)}')
