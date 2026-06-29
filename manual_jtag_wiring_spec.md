# J7 JTAG Header Wiring Specification — Option C
# Generated: 2026-04-16 | Updated: 2026-04-22 | DEC-015/DEC-017 | DO NOT EDIT .sch files until manual work complete

---

## 1. Programmer and pinout (DEC-015)

Programmer: Digilent JTAG-HS3  
Connector: J7 — Conn_01x06_Male, JTAG_HDR  
Library footprint: Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical  
Convention: B (Digilent 1×6)

| J7 Pin | Sheet position | Signal | Source |
|---|---|---|---|
| 1 | (11300, 7700) | VCC → VCCO_HP_65 (1.8V) | New GLabel instance |
| 2 | (11300, 7800) | TMS | R9 right pin |
| 3 | (11300, 7900) | TCK | R6 right pin |
| 4 | (11300, 8000) | TDO | R8 right pin |
| 5 | (11300, 8100) | TDI | R7 right pin |
| 6 | (11300, 8200) | GND | #PWR020 |

---

## 2. Refdes-signal mapping (FIXED — do not rename)

| RefDes | Signal | Note |
|---|---|---|
| R6 | TCK (JX1.D1) | unchanged |
| R7 | TDI (JX1.C2) | unchanged |
| R8 | TDO (JX1.D2) | unchanged |
| R9 | TMS (JX1.C1) | unchanged |

Physical vertical order after move will be R9/R6/R8/R7 top-to-bottom. This is intentional.
Refdes numeric order does NOT need to match physical order for a defense-grade BOM.

---

## 3. Resistor move table

Component P is the CENTER of the resistor body (P_x = 9100 for all).
Left pin = (P_x−200, P_y) = (8900, P_y).
Right pin = (P_x+200, P_y) = (9300, P_y).
VERIFIED 2026-04-22: empirically confirmed from wire endpoints for all four resistors (DEC-017 Q1).

| RefDes | Signal | P from | P to | Left pin from | Left pin to | Right pin from | Right pin to |
|---|---|---|---|---|---|---|---|
| R9 | TMS | (9100,8500) | (9100,7800) | (8900,8500) | (8900,7800) | (9300,8500) | (9300,7800) |
| R6 | TCK | (9100,7600) | (9100,7900) | (8900,7600) | (8900,7900) | (9300,7600) | (9300,7900) |
| R8 | TDO | (9100,8200) | (9100,8000) | (8900,8200) | (8900,8000) | (9300,8200) | (9300,8000) |
| R7 | TDI | (9100,7900) | (9100,8100) | (8900,7900) | (8900,8100) | (9300,7900) | (9300,8100) |

---

## 4. GLabel move table

All GLabels: orient=0 (pointing right), type=Input, size=40.
Connection point is at the stated (x,y).

| RefDes | Signal | GLabel name | From | To |
|---|---|---|---|---|
| R9 | TMS | JTAG_TMS | (8100,8500) | (8100,7800) |
| R6 | TCK | JTAG_TCK | (8100,7600) | (8100,7900) |
| R8 | TDO | JTAG_TDO | (8100,8200) | (8100,8000) |
| R7 | TDI | JTAG_TDI | (8100,7900) | (8100,8100) |

Note: GLabels are NOT connected to resistors in the current schematic (400-mil gap between
GLabel at x=8100 and left wire start at x=8500). KiCad drag will NOT move GLabels when
dragging resistors. Move GLabels separately.

---

## 5. Wire list — DELETE (old wires to remove)

All old right-side wires must be deleted before or after moving resistors.
Old left-side wires (8500→8900) will move with the resistor if using KiCad move (M key).
If they do not move automatically, delete and redraw at new y.

| Wire | x1 | y1 | x2 | y2 | Notes |
|---|---|---|---|---|---|
| R6 left | 8500 | 7600 | 8900 | 7600 | moves with R6 or delete/redraw |
| R7 left | 8500 | 7900 | 8900 | 7900 | moves with R7 or delete/redraw |
| R8 left | 8500 | 8200 | 8900 | 8200 | moves with R8 or delete/redraw |
| R9 left | 8500 | 8500 | 8900 | 8500 | moves with R9 or delete/redraw |
| R6 right | 9300 | 7600 | 10700 | 7600 | DELETE — replace with longer wire |
| R7 right | 9300 | 7900 | 10700 | 7900 | DELETE — replace with longer wire |
| R8 right | 9300 | 8200 | 10700 | 8200 | DELETE — replace with longer wire |
| R9 right | 9300 | 8500 | 10700 | 8500 | DELETE — replace with longer wire |

---

## 6. Wire list — ADD (new wires to place)

### 6a. Left connecting wires (NEW — fixes pre-existing GLabel gap)
These did not exist in the original schematic. Required to connect GLabel to resistor left pin.

| Signal | x1 | y1 | x2 | y2 |
|---|---|---|---|---|
| TMS (R9) | 8100 | 7800 | 8500 | 7800 |
| TCK (R6) | 8100 | 7900 | 8500 | 7900 |
| TDO (R8) | 8100 | 8000 | 8500 | 8000 |
| TDI (R7) | 8100 | 8100 | 8500 | 8100 |

### 6b. Left resistor body wires (redraw at new y if not dragged automatically)

| Signal | x1 | y1 | x2 | y2 |
|---|---|---|---|---|
| TMS (R9) | 8500 | 7800 | 8900 | 7800 |
| TCK (R6) | 8500 | 7900 | 8900 | 7900 |
| TDO (R8) | 8500 | 8000 | 8900 | 8000 |
| TDI (R7) | 8500 | 8100 | 8900 | 8100 |

### 6c. Right wires — resistor to J7 (straight horizontal, replaces old 9300→10700)

| Signal | x1 | y1 | x2 | y2 | Connects |
|---|---|---|---|---|---|
| TMS (R9) | 9300 | 7800 | 11300 | 7800 | R9 right pin → J7 pin 2 |
| TCK (R6) | 9300 | 7900 | 11300 | 7900 | R6 right pin → J7 pin 3 |
| TDO (R8) | 9300 | 8000 | 11300 | 8000 | R8 right pin → J7 pin 4 |
| TDI (R7) | 9300 | 8100 | 11300 | 8100 | R7 right pin → J7 pin 5 |

### 6d. J7 pin 1 — VCC connection

New GLabel instance (does NOT replace existing GLabel at 11500,8900 — both coexist):
CONFIRMED 2026-04-22: duplicate same-name GLabels on same sheet are valid in KiCad 5.1.5 — no ERC warning (DEC-017 Q2).

| Element | Type | x | y | Orient | Net name |
|---|---|---|---|---|---|
| New GLabel | Input | 11500 | 7700 | 2 (pointing left) | VCCO_HP_65 |
| Wire | — | 11300 | 7700 | 11500 | 7700 |

### 6e. J7 pin 6 — GND connection

Move #PWR020 (no new symbol — preserve refdes):
CONFIRMED 2026-04-22: #PWR020 has NO wires attached at (11100,9100). Move leaves no floating wire. Refdes preserved. (DEC-017 Q3)

| Action | Element | From | To |
|---|---|---|---|
| MOVE | #PWR020 power:GND | P=(11100,9100) | P=(11100,8200) |
| ADD wire | — | (11100,8200) | (11300,8200) |

---

## 7. Text annotation moves (cosmetic — non-electrical)

Right-side text notes are currently at x=9700 at old y-values. Move to new y after resistor moves.

| Text content | From (x,y) | To (x,y) |
|---|---|---|
| JTAG_TCK (JX1.D1) | (9700,7600) | (9700,7900) |
| JTAG_TDI (JX1.C2) | (9700,7900) | (9700,8100) |
| JTAG_TDO (JX1.D2) | (9700,8200) | (9700,8000) |
| JTAG_TMS (JX1.C1) | (9700,8500) | (9700,7800) |

---

## 8. Operational sequence

**Before starting:** Close this spec. Open KiCad, open support_io.sch.
Recommended: work one signal row at a time. Complete all operations for R9/TMS first,
then R6/TCK, then R8/TDO, then R7/TDI, then do VCC/GND last.

### Phase 1: Delete old right-side wires (all 4)
Delete: (9300,7600)→(10700,7600), (9300,7900)→(10700,7900),
        (9300,8200)→(10700,8200), (9300,8500)→(10700,8500)
Reason: deleting first prevents wire-stretch confusion during moves.

### Phase 2: Move resistors to new y-positions
WARNING — ORDERING CONFLICT: R7 currently occupies y=7900. R6 must move TO y=7900.
Move R7 FIRST to vacate y=7900 before moving R6.

Required move order:
  Step 1: R7 (9100,7900) → (9100,8100)  [vacates y=7900]
  Step 2: R6 (9100,7600) → (9100,7900)  [y=7900 now free]
  Step 3: R8 (9100,8200) → (9100,8000)
  Step 4: R9 (9100,8500) → (9100,7800)

For each move:
  a. Select component only (click on body)
  b. Press M (Move) to move component + attached left wire together
  c. Type exact new coordinates or count grid steps
  d. Confirm placement

If left wire does NOT move with component:
  - Delete old left wire manually
  - Redraw at new position from Section 6b

Final P coordinates after all moves:
  R9: (9100,7800)  |  R6: (9100,7900)  |  R8: (9100,8000)  |  R7: (9100,8100)

### Phase 3: Move GLabels to new y-positions
For each GLabel (move independently — not attached to resistors):
WARNING — ORDERING CONFLICT: JTAG_TDI currently at (8100,7900). JTAG_TCK must move TO y=7900.
Move JTAG_TDI FIRST.

  Step 1: JTAG_TDI:  (8100,7900) → (8100,8100)  [vacates y=7900]
  Step 2: JTAG_TCK:  (8100,7600) → (8100,7900)  [y=7900 now free]
  Step 3: JTAG_TDO:  (8100,8200) → (8100,8000)
  Step 4: JTAG_TMS:  (8100,8500) → (8100,7800)

### Phase 4: Add left connecting wires (Section 6a)
Draw 4 new horizontal wires connecting GLabel connection points to left wire segments:
  (8100,7800)→(8500,7800)  [TMS]
  (8100,7900)→(8500,7900)  [TCK]
  (8100,8000)→(8500,8000)  [TDO]
  (8100,8100)→(8500,8100)  [TDI]

### Phase 5: Add right wires — resistor to J7 (Section 6c)
Draw 4 new horizontal wires from resistor right pins to J7 pin faces:
  (9300,7800)→(11300,7800)  [TMS → J7 pin 2]
  (9300,7900)→(11300,7900)  [TCK → J7 pin 3]
  (9300,8000)→(11300,8000)  [TDO → J7 pin 4]
  (9300,8100)→(11300,8100)  [TDI → J7 pin 5]

### Phase 6: VCC and GND connections
  a. Place new VCCO_HP_65 GLabel at (11500,7700), orient=2 (left-pointing), type=Input
  b. Draw wire (11300,7700)→(11500,7700)
  c. Move #PWR020 from (11100,9100) to (11100,8200)
  d. Draw wire (11100,8200)→(11300,8200)

### Phase 7: Text annotation moves (optional, cosmetic)
Move 4 text notes from Section 7 to new y-positions.

---

## 9. Post-work sanity checklist

Run this check BEFORE running ERC. Verify each item visually in KiCad.

**Resistor positions (P coordinates):**
- [ ] R9 (TMS): P = (9100, 7800)
- [ ] R6 (TCK): P = (9100, 7900)
- [ ] R8 (TDO): P = (9100, 8000)
- [ ] R7 (TDI): P = (9100, 8100)

**GLabel positions:**
- [ ] JTAG_TMS at (8100, 7800)
- [ ] JTAG_TCK at (8100, 7900)
- [ ] JTAG_TDO at (8100, 8000)
- [ ] JTAG_TDI at (8100, 8100)

**Left connecting wires (8100→8500, new):**
- [ ] Wire at y=7800 from x=8100 to x=8500
- [ ] Wire at y=7900 from x=8100 to x=8500
- [ ] Wire at y=8000 from x=8100 to x=8500
- [ ] Wire at y=8100 from x=8100 to x=8500

**Left resistor body wires (8500→8900):**
- [ ] Wire at y=7800 from x=8500 to x=8900
- [ ] Wire at y=7900 from x=8500 to x=8900
- [ ] Wire at y=8000 from x=8500 to x=8900
- [ ] Wire at y=8100 from x=8500 to x=8900

**Right wires (9300→11300, straight horizontal):**
- [ ] Wire at y=7800 from x=9300 to x=11300
- [ ] Wire at y=7900 from x=9300 to x=11300
- [ ] Wire at y=8000 from x=9300 to x=11300
- [ ] Wire at y=8100 from x=9300 to x=11300

**VCC (J7 pin 1):**
- [ ] New VCCO_HP_65 GLabel at (11500, 7700), orient=2 (left-pointing)
- [ ] Wire from (11300,7700) to (11500,7700)
- [ ] Original VCCO_HP_65 GLabel at (11500,8900) still present (do NOT delete)

**GND (J7 pin 6):**
- [ ] #PWR020 located at P=(11100, 8200) — NOT at (11100,9100)
- [ ] Wire from (11100,8200) to (11300,8200)
- [ ] No old wire remnant at (11100,9100)

**No remnants at old positions:**
- [ ] No wires at y=7600 in x=8100–11300 range (old R6/TCK row)
- [ ] No wires at y=8200 in x=8100–10700 range (old R8/TDO right wire)
- [ ] No wires at y=8500 in x=8100–10700 range (old R9/TMS right wire)
- [ ] GLabel JTAG_TCK NOT at (8100,7600)
- [ ] GLabel JTAG_TMS NOT at (8100,8500)

**ERC expectations after manual work:**
- ErrType(3): 0 (was 1 — #PWR020 now connected)
- ErrType(2): ~839 or fewer (was 849; J7 6 pins + R6-R9 4 left pins = −10 minimum)
- ErrType(8): 0
- If ErrType(2) > 845: investigate for wire gap or missed connection
- If ErrType(3) != 0: diagnose before closing J7 work

---

## 10. Known pre-existing issues NOT fixed by this work

- J6 UART pins 1–3 (TX/RX/VCC): wires terminate at x=4100, J6 pins at x=4700 — deferred to Phase 6
- Design note line 423 in support_io.sch: incorrectly states "R9-R12 are 0-ohm DNP" — actual JTAG resistors are R6–R9. Stale note; cosmetic only, no electrical impact.
- VCCO_HP_65 GLabel at (11500,8900): left in place after this work — it was connecting to nothing before and will continue to connect to nothing (no wire attached). It is electrically harmless but visually orphaned. Address in Phase 6 cleanup or Sheet 4 audit.

---

*This document is a reference only. All changes are manual KiCad GUI operations.
After completing manual work, save the schematic, run ERC, and report counts.*
