# Session Transition — UZEV ADRV9009 Carrier
**Date:** 2026-06-22
**Phase:** Layout prep — placement locked, constraints doc written, awaiting external replies

---

## A. VERIFIED ON-DISK STATE

All MD5s confirmed at session end. `.kicad_pcb` not modified in this session.

### A.1 PCB File

| File | MD5 |
|---|---|
| `uzev_adrv9009_carrier.kicad_pcb` | `9097228f0dc5b63238fbbdabb8b22d90` |

- **179 modules** (175 netlist components + 4 NPTH mounting holes)
- **997 nets**
- **8 copper layers:** F.Cu / In1.Cu(GND) / In2.Cu(signal) / In3.Cu(GND) / In4.Cu(power) / In5.Cu(signal) / In6.Cu(GND) / B.Cu
- **Edge.Cuts:** closed rectangle 152.4 × 101.6 mm; origin = board top-left corner
- **Datum:** (0, 0) = top-left corner of board in KiCad coordinate space (Y-down)

### A.2 Seven Locked Positions

All locked (`locked` flag set in .kicad_pcb); verified post-FPID-fix session.

| Ref | Footprint | X (mm) | Y (mm) | Rot | Notes |
|---|---|---|---|---|---|
| J1 | SEAF-40-05.0-S-10-2-A-K-TR_200P | 55.714 | 66.115 | 0° | JX1 carrier socket; rotation **[OPEN ITEM #1]** |
| J2 | SEAF-40-05.0-S-10-2-A-K-TR_200P | 55.714 | 13.410 | 0° | JX2 carrier socket; rotation **[OPEN ITEM #1]** |
| J3 | SEAF-30-05.0-S-10-2-A-K-TR_120P | 104.215 | 39.725 | 0° | JX3 carrier socket; rotation **[OPEN ITEM #1]** |
| MH1 | MountingHole_2.7mm_NPTH | 12.191 | 67.309 | 0° | PTH+GND conversion deferred **[OPEN ITEM #3]** |
| MH2 | MountingHole_2.7mm_NPTH | 12.191 | 12.191 | 0° | PTH+GND conversion deferred **[OPEN ITEM #3]** |
| MH3 | MountingHole_2.7mm_NPTH | 105.409 | 67.309 | 0° | PTH+GND conversion deferred **[OPEN ITEM #3]** |
| MH4 | MountingHole_2.7mm_NPTH | 105.409 | 12.191 | 0° | PTH+GND conversion deferred **[OPEN ITEM #3]** |

Connector centroids computed via Option B transform: x_b = 8 + y_som_mm;
y_b = 8 + (63.5 − x_som_mm). Handedness det=+1 (verified correct, DEC-053).
MH Ø2.7 mm is provisional for M2.5 — confirm before conversion (OPEN ITEM #2).

### A.3 Schematics

ERC-clean: 0 errors / 0 warnings (last verified in DEC-028/029 gate period).

| File | MD5 |
|---|---|
| `uzev_adrv9009_carrier.sch` | `363602f75afa263240faecf894250bbd` |
| `connectors.sch` | `8bf6a39c2a888e497db3b5661472a5ec` |
| `power.sch` | `5cc2bc8720f66a9cf5d3e3c98180e88b` |
| `support_io.sch` | `e70251275550c5dfe948771d6e977589` |
| `adrv9009_signals.sch` | `c82b3b734693b0aff4969f1d0e45fcf3` |

### A.4 Libraries & Footprints

| File | MD5 |
|---|---|
| `UZEV_Connectors.lib` | `2a9c65a24565d51680e5020695fb03da` |
| `uzev_adrv9009_carrier-cache.lib` | `cb0ba72300fb9f006d8508b6a0a499e3` |

`UZEV_Connectors.pretty/` contains 6 `.kicad_mod` files (SEAF-30, SEAF-40,
HVSSOP-8, USB-C, VQFN-14, WQFN-38). SEAF-40 footprint: NPTH lugs Ø1.45 mm
at ±21.28 mm from centroid (DEC-052). All FPIDs fully-qualified after FPID
normalization pass (B6, B7, L5, L6 fixed).

### A.5 Constraints & Decisions

| File | MD5 | Lines |
|---|---|---|
| `LAYOUT_CONSTRAINTS.md` | `64f7a9ead7477db3d5dfeaed7deb88ae` | 271 |
| `DECISIONS_LOG.md` | `f281aa6ec20cd4aede178f4ad79b7ae3` | — |
| `CLAUDE.md` | `0f5ff47b507b0970ccea787fa42c195f` | — |

DECISIONS_LOG.md: DEC-001 through DEC-053. Current highest = DEC-053 (SOM
placement, Option B, transform, handedness proof). Next free = DEC-054.

### A.6 Stray Files — Cleanup Needed (Not Urgent)

Two files exist that are bash-error artifacts (created when `ls --help.sch` ran
with a stray glob expansion):

- `--help.sch`
- `--help-cache.lib`

These are empty or near-empty. Delete before any future KiCad GUI open to avoid
confusing the project parser. Safe to `rm` without backup.

---

## B. LOCKED DECISIONS

### B.1 Board Geometry (DEC-053)

- **Board size:** 152.4 × 101.6 mm (6 × 4 in), datum = top-left origin
- **SOM width (authoritative):** 63.5 mm — the 63.5 mm is correct; UG figure
  showing 60.96 mm is a documentation typo (DEC-053; cross-checked from SEAM8
  footprint pin pitch × row count)
- **Orientation:** Option B — SOM long axis (101.6 mm) along board X, N-end
  to right, W-edge at board bottom
- **8mm inset:** all 7 locked positions use 8 mm board-edge clearance minimum
- **Transform (SOM→board coords):**
  x_b = 8 + y_som;  y_b = 8 + (63.5 − x_som)
  Jacobian [[0,1],[−1,0]], det = +1

### B.2 Transform Handedness (DEC-053)

det = +1 is correct. Derivation: physical mating (SOM bottom-face to carrier
top-face) introduces a mirror, det = −1. KiCad Y-down convention vs designer
Y-up introduces a second sign flip, det = −1. Product = +1 (pure rotation).
Concrete example verified: SOM pin A1 maps to computed centroid within 0.025 mm.

### B.3 Eight-Layer Stackup (DEC-053)

`CopperLayerCount` keyword rejected by KiCad 5.1.5 (KiCad 6 syntax). Layer
count is implicit from the `(layers ...)` block. Keyword was removed. File
re-verified to load clean in pcbnew.

### B.4 First-Boot Gate — ALL 7 ITEMS PASS

Per CLAUDE.md §FIRST-BOOT-READINESS GATE:

| Gate | Status | DEC | Date |
|---|---|---|---|
| 1. Rail completeness | PASS | DEC-046 | 2026-06-16 |
| 2. Rail sequencing | PASS | DEC-046 | 2026-06-16 |
| 3. Enables + power-good | PASS | DEC-046 | 2026-06-16 |
| 4. Boot config | PASS | DEC-047 | 2026-06-16 |
| 5. Reset / POR | PASS | DEC-048 | 2026-06-16 |
| 6. Decoupling caps | PASS | DEC-046 | 2026-06-16 |
| 7. Diff-pair integrity | PASS | DEC-049 | 2026-06-16 |

Gate is CLEAR as of 2026-06-16. No regressions introduced in this session
(no schematic edits made).

### B.5 Other Locked Decisions

- **tx_sync_1 RTL-unused:** DEF-26 CLOSED. Signal exists in carrier schematic
  but is not driven by JESD204B IP core default configuration. Accepted as DNI.
  World A confirmed (§0a gate passed).
- **MH GND-net approach:** Option (a) approved — convert to PTH with GND net,
  annular ring 0.2 mm, all copper layers. Write deferred pending MH diameter
  confirmation (OPEN ITEM #2/#3).
- **AC coupling caps C21–C28:** On TX JESD lanes only (FPGA C2M direction).
  100 nF, 0201. On carrier, near J4 (FMC). RX lanes and refclks: no carrier
  caps (SOM-side coupling; DEC-049).
- **Netlist source:** `uzev_carrier.net` (MD5: 7762ec8dbcc8da5028d237ab52b527b6,
  dated Jun 17 10:33) is authoritative for pad-to-net assignments.

---

## C. OPEN ITEMS — GATED ON EXTERNAL REPLIES

### C.1 Connector Rotation (JX1/JX2/JX3) — awaiting Avnet

J1, J2, J3 are currently placed at 0°. Actual rotation ∈ {0°, 180°} is
determined by the SEAM8 orientation on the SOM bottom face. Resolve from:
- Avnet UltraZed-EV reference PCB layout files, OR
- Physical SOM inspection (note which edge of SEAM8 has the A1 chamfer)

**Edit when resolved:** one `(at X Y ROT)` change per connector, atomic write,
pre/post MD5. No other position changes needed.

### C.2 MH Diameter (M2.5 vs M3) — awaiting Avnet

Provisional: Ø2.7 mm (M2.5 clearance). M3 would require Ø3.2 mm drill.
Confirm from: Avnet mechanical drawing for UltraZed-EV SOM standoff spec.

### C.3 MH PTH+GND Conversion — batched with C.2

**Approved (Option a):** convert MH1–MH4 from NPTH to PTH with GND net,
annular ring 0.2 mm minimum, all copper layers, courtyard unchanged.
Write is batched: single atomic Python script after C.2 diameter confirmed.
Script must: back up .kicad_pcb, change drill to confirmed dia, add copper
annular pads, assign net GND, save, report pre/post MD5.

### C.4 Fab Stackup → Real Trace Geometry — critical-path dependency

LAYOUT_CONSTRAINTS.md specifies Zdiff = 100 Ω ±10% with indicative geometry
(5 mil trace / 15 mil edge-to-edge from ADRV9009 DS). Actual trace width and
gap must be computed from the fab's dielectric thickness and Dk for our 8-layer
stackup. This must resolve before routing begins — it sets the DRC rules file.

**Action:** once fab candidate is chosen, run impedance calculator (e.g., Saturn
PCB) for both In2.Cu (JESD, dual GND ref) and In5.Cu (LVDS, single GND ref).
Update §3 of LAYOUT_CONSTRAINTS.md with actual geometry; flag as sourced.

### C.5 Quilter KiCad 5.1.5 Compatibility — awaiting reply

Unknown whether Quilter autorouter ingests KiCad 5.1.5 `.kicad_pcb` natively
or requires KiCad 6/7 format. If migration required:
- Migrate with `kicad-cli pcb upgrade` (KiCad 7 CLI), verify module count 179,
  net count 997, all 7 locked positions preserved post-migrate
- Re-run FPID check — KiCad 7 format changes FPID representation

**Gates:** tool-path selection and constraint-package format for Quilter.

---

## D. CONSTRAINTS SPEC [TO CONFIRM] FLAGS

These are carried forward from LAYOUT_CONSTRAINTS.md Rev 0.1 and must be
resolved with primary-source citations before Gerber sign-off. Do NOT treat
as sourced until confirmed.

| Flag | Current placeholder | Required source |
|---|---|---|
| rx_data[0]=DP1 non-sequential lane mapping | Stated in adrv9009_signals.sch comment | Verify against RTL XSA / JESD204B IP port list before routing; a wrong mapping routes a broken link |
| Intra-pair skew ≤ 5 mil | From capture guide | Confirm vs UG576 §PCB Guidelines or JESD204B transport layer spec |
| Inter-lane length matching budget | Not specified | UG576 §Multi-lane matching; ballpark 100–200 mil at 12.5 Gbps, needs confirmation |
| GTH carrier termination | "None, FPGA internal" | UG576 §GTH Termination; confirm no external resistors needed on carrier |
| VITA 57.1 LVDS impedance | 100 Ω from capture guide | Cross-check VITA 57.1 §6; expected to match, needs cite |
| Actual trace geometry | Indicative 5 mil / 15 mil (ADRV9009 DS Figure 444, 4-layer baseline) | Fab stackup required (see OPEN ITEM C.4) |

**Critical:** the rx_data lane mapping flag is the highest-risk item. A wrong
JESD204B lane assignment is ERC-invisible and produces a dead link on first
power-up. Verify against the ADI hdl_2022_r2 ADRV9009/ZCU102 IP port map
before routing begins.

---

## E. NEXT-SESSION SEQUENCE

Ordered by dependency:

1. **On Avnet reply (C.2 + C.1):**
   - Write batched MH edit: PTH+GND at confirmed diameter, all 4 holes
   - Set connector rotations for J1/J2/J3 (single `(at X Y ROT)` per connector)
   - Run visual DRC sanity check (no routing rules set yet, courtyard + silkscreen only)
   - Board is then Gerber-ready pending D flags and fab stackup

2. **On Quilter reply (C.5):**
   - If KiCad 5 compatible: prepare constraint package (DRC rules file + layer
     assignments from LAYOUT_CONSTRAINTS.md §5)
   - If migration required: run `kicad-cli pcb upgrade`, verify 179 modules /
     997 nets / 7 locked positions, update project to KiCad 7

3. **On fab stackup (C.4):**
   - Compute actual trace width/gap for In2.Cu and In5.Cu
   - Update LAYOUT_CONSTRAINTS.md §3 tables, remove "[TO CONFIRM]" from geometry rows
   - Write DRC rules file (`.kicad_dru`) with impedance-controlled width constraints

4. **Resolve D flags before Gerber:**
   - Confirm rx_data lane mapping against RTL (highest priority)
   - UG576 for intra-pair skew, inter-lane budget, GTH termination
   - VITA 57.1 for LVDS impedance cite
   - When all D flags cleared: LAYOUT_CONSTRAINTS.md Rev 1.0 is Gerber-ready

---

## F. WORKING DISCIPLINE (carry forward)

- **Atomic Python writes:** `os.replace()` with `.tmp` intermediate; backup file
  before every edit; pre/post MD5 reported after every file touch
- **Per-edit approval gate:** every proposed change requires diagnosis + primary
  source citation + proposed diff + explicit user approval before execution.
  "Pending in a transition doc" = ready to propose, NOT ready to apply.
- **Primary sources win ties:** VITA 57.1 → Avnet Designer's Guide → SOM
  schematic → library; cached memory is never authoritative for boot-critical values
- **No GUI saves on schematics:** schematic files modified only by Python atomic
  scripts; GUI save changes modification timestamp and can silently rewrite content
- **No DRC sign-off this session:** DRC not run; no routing rules file exists yet
- **This chat = verification/approval layer:** Claude Code is the local edit
  agent; all edits execute only after explicit per-edit approval in chat
- **KiCad 5.1.5 format constraints:** `module` keyword (not `footprint`);
  no `CopperLayerCount` keyword; Y-down coordinate convention
- **On context resume:** first action is to confirm current approval state with
  user before any tool call touches project files

---

*TRANSITION_2026-06-22.md — end of document*
