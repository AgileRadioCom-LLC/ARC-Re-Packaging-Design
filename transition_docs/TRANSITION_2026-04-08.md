# UZEV ADRV9009 Carrier Board — Transition Document
**Generated:** 2026-04-08
**Session type:** End-of-session handoff to next chat
**Status:** Mid-verification phase, 2 documentation bugs fixed, design work NOT YET RESUMED

---

## 0. Opening instructions for the next chat

Start the new chat inside the same RPKG project so the Designer's Guide PDF and this document are available in project knowledge. Recommended opening message:

> Continuing UZEV ADRV9009 carrier board work. Attached is the transition
> document from the previous session. Please read it first, then ask me
> for the current state snapshot before making any decisions.

The next chat should **not** trust any claim in this document without first confirming the on-disk state matches. Use the "State verification" commands in Section 6 before taking any action.

---

## 1. Project identity (immutable)

- **Project**: Defense-grade SDR datalink carrier board for UAV/GCS
- **Platform**: Avnet UltraZed-EV SOM (XCZU7EV-1FBVB900E) + ADI ADRV9009-W/PCBZ
- **SOM↔RFIC interface**: FMC HPC (custom ADRV9009 FMC card plugs into carrier)
- **SOM↔carrier interface**: Samtec SEARAY micro-headers JX1 (200-pin), JX2 (200-pin), JX3 (120-pin)
- **FPGA toolchain**: Vivado 2022.2 Standard Edition (free tier; XCZU7EV qualifies)
- **ADI HDL branch**: `hdl_2022_r2`, tag `2022_r2_p1`
- **Schematic tool**: KiCad 5.1.5 (system package at `/usr/bin/`, NOT KiCad 9 AppImage which is broken on this Ubuntu 20.04)
- **Project directory**: `/home/arc/projects/uzev_carrier_v5/`
- **HDL working tree**: `/home/arc/adrv9009_uzev/hdl/` (do not touch `/home/arc/projects/hdl/`, `/home/arc/adi/hdl/`, `/home/arc/adi_project/hdl/`)

---

## 2. Authoritative sources (ranked)

When any two sources disagree, resolve in this order:

1. **ANSI/VITA 57.1-2008 standard** — ultimate authority for FMC HPC connector pinout (DP lanes, LA pairs, HA pairs, power/ground pins)
2. **Avnet UltraZed-EV Designer's Guide** (`UGAESZU7EVSOMGV1_2.pdf` in project knowledge) — authoritative for SOM-side mappings (FPGA ball → JX pin)
3. **`UZEV_Connectors.lib`** at `/home/arc/projects/uzev_carrier_v5/UZEV_Connectors.lib` — VERIFIED CORRECT for all non-power JX1/JX2/JX3 pin-to-signal mappings and all 65 FMC signal pins
4. **XDC file** `system_constr.xdc` — authoritative for what the bitstream was built against. `set_property PACKAGE_PIN` directives are correct. The `##` comments WERE wrong in two places; both fixed in this session (see DEC-001 and DEC-002).
5. **Pin mapping spreadsheet** `ADRV9009_UltraZed_EV_Pin_Mapping.xlsx` — mostly correct. Tab 4 "PROPOSED MAPPING" has the SAME off-by-one GPIO error as the old XDC comments. Not fixed (reference document, not build input). See Known Issues.

**Do not trust these without re-verification:**
- power.sch comments (e.g., line 27 about VIN pins — claims 12 pins, library has 8, Designer's Guide has ~7)
- Any commentary in older transition documents from March

---

## 3. Verification status at session end

| Category | Scope | Status | Notes |
|---|---|---|---|
| **V1** | XDC ↔ library non-GT signals | ✅ **45/45 verified** | After DEC-001 fix |
| **V1b** | XDC ↔ FMC_HPC_ADRV9009 GT signals | ✅ **20/20 verified** | After DEC-002 fix |
| **V2** | FMC HPC power pins in symbol | ❌ Pending | FMC_3P3V, VADJ missing from FMC_HPC_ADRV9009 symbol |
| **V3** | VIN pin list reconciliation on JX1 | ❌ Pending | 3 sources disagree (7/8/12 pins) |
| **V4** | JESD rx/tx label tie strategy | ❌ Pending | Design decision needed |
| **V5** | Sheet 1 wiring populated | ❌ Not started | Depends on V2/V3/V4 |

**Headline result: the 65 functional SOM-side signals are electrically verified between XDC, library, and Designer's Guide. The bitstream physically drives the correct carrier pins.**

---

## 4. Decisions taken this session

### DEC-001 (2026-04-07 17:30) — GPIO 04/05/09/10 pin-mapping authority
The library is authoritative. XDC `##` comments and spreadsheet Tab 4 had an off-by-one error on JX1 pin numbers for these four GPIOs:

| Signal | Ball | Correct JX1 pin | Wrong value |
|---|---|---|---|
| adrv9009_gpio_04 / HP_DP_27_P | AF12 | **A24** | A25 |
| adrv9009_gpio_05 / HP_DP_27_N | AF11 | **A25** | A26 |
| adrv9009_gpio_09 / HP_DP_25_P | AJ10 | **C24** | C25 |
| adrv9009_gpio_10 / HP_DP_25_N | AK10 | **C25** | C26 |

Fix applied to XDC comments only. `set_property` directives unchanged. Bitstream unaffected. Verified against Designer's Guide Table 26, pages 32-33, cross-checked visually by Ravv.

### DEC-002 (2026-04-07 17:45) — XDC GT lane DP label corrections
The library, Sheet 3 labels, and spreadsheet "ADRV9009 FMC Signals" tab were all correct per VITA 57.1 HPC. The XDC `##` comments on 10 GT lines had wrong DP numbers (rx/tx lanes 1 and 2 had DP labels swapped relative to the standard).

Fixes:

| Port | FMC Pin | Wrong → Correct |
|---|---|---|
| rx_data_p/n[1] | A06/A07 | DP0 → **DP2** |
| rx_data_p/n[2] | C06/C07 | DP2 → **DP0** |
| tx_data_p/n[0] | A22/A23 | DP0 → **DP1** |
| tx_data_p/n[1] | A26/A27 | DP1 → **DP2** |
| tx_data_p/n[2] | C02/C03 | DP2 → **DP0** |

Fix applied to XDC comments only. `set_property` directives unchanged. Bitstream unaffected. Verified against ANSI/VITA 57.1-2008 standard (page 48), cross-checked against Xilinx AC701 User Manual Appendix B and HiTechGlobal FMC module datasheet.

### Non-decision: Step 2 (pin rename) and Step 2b (symbol swap on Sheet 1)
These were executed earlier in the session before the architectural bug was discovered. The `FMC_HPC_ADRV9009` symbol in `UZEV_Connectors.lib` has 65 FMC pin names correctly renamed from stock `Pin_N` format. The `connectors.sch` J4 component uses the new symbol (10 units, L-line reference `UZEV_Connectors:FMC_HPC_ADRV9009`, verified by diff). These remain valid and should NOT be reverted.

---

## 5. Critical architectural finding (not a "bug", a "missing work")

**Sheet 1 (`connectors.sch`) is electrically empty.**

Per-sheet element counts:

| Sheet | Components | GLabels | Wires | NoConn | Junctions |
|---|---|---|---|---|---|
| connectors.sch | 22 | 0 | 0 | 0 | 0 |
| power.sch | 54 | 20 | 3 | 0 | 0 |
| adrv9009_signals.sch | 8 | 130 | 57 | 0 | 0 |
| support_io.sch | 22 | 21 | 28 | 0 | 1 |

Sheets 2/3/4 have 151 unique global labels that expect to connect to Sheet 1's connectors. Sheet 1 has zero labels and zero wires. **Every signal on Sheets 2/3/4 is currently dangling** because nothing on Sheet 1 matches their names.

This is why the ERC showed 148 "Global label not connected to any other global label" errors. The original transition doc from March 24 diagnosed this as a pin-name mismatch on J4, which was wrong. The real issue is that Sheet 1 was stubbed with bare connector symbols and the label/wire work was never done.

**The fix is V5: populate Sheet 1 with wire stubs + global labels at each used connector pin.** This is not yet started. It requires V2 (FMC power pins in symbol), V3 (VIN pin list resolved), and V4 (JESD tie strategy) to be decided first so we know which labels go where.

---

## 6. State verification commands for next session

Run these in the next chat BEFORE taking any action. They confirm the on-disk state matches this document.

```bash
# A. Confirm we're in the right project
ls -la /home/arc/projects/uzev_carrier_v5/
cat /home/arc/projects/uzev_carrier_v5/DECISIONS_LOG.md | head -30

# B. Confirm the XDC fixes survived
grep -c 'JX1.A24.*HP_DP_27_P' /home/arc/adrv9009_uzev/hdl/projects/adrv9009/zcu102/system_constr.xdc
grep -c 'JX1.A25.*HP_DP_27_N' /home/arc/adrv9009_uzev/hdl/projects/adrv9009/zcu102/system_constr.xdc
grep -c 'JX1.C24.*HP_DP_25_P' /home/arc/adrv9009_uzev/hdl/projects/adrv9009/zcu102/system_constr.xdc
grep -c 'JX1.C25.*HP_DP_25_N' /home/arc/adrv9009_uzev/hdl/projects/adrv9009/zcu102/system_constr.xdc
# Each should return 1

grep -c 'A06  DP2_M2C_P' /home/arc/adrv9009_uzev/hdl/projects/adrv9009/zcu102/system_constr.xdc
grep -c 'C06  DP0_M2C_P' /home/arc/adrv9009_uzev/hdl/projects/adrv9009/zcu102/system_constr.xdc
grep -c 'A22  DP1_C2M_P' /home/arc/adrv9009_uzev/hdl/projects/adrv9009/zcu102/system_constr.xdc
# Each should return 1

# C. Confirm Step 2b J4 swap survived
grep -c 'UZEV_Connectors:FMC_HPC_ADRV9009' /home/arc/projects/uzev_carrier_v5/connectors.sch
grep -c 'Samtec_ASP-134602-01' /home/arc/projects/uzev_carrier_v5/connectors.sch
# Expected: 10, 0

# D. Confirm FMC_HPC_ADRV9009 symbol in library has 65 renamed pins
awk '/^DEF FMC_HPC_ADRV9009/,/^ENDDEF/' /home/arc/projects/uzev_carrier_v5/UZEV_Connectors.lib | grep -c '^X FMC_'
# Expected: 65

# E. Re-run the full V1 + V1b verification to confirm 65/65
python3 << 'PYEOF'
import re
XDC="/home/arc/adrv9009_uzev/hdl/projects/adrv9009/zcu102/system_constr.xdc"
LIB="/home/arc/projects/uzev_carrier_v5/UZEV_Connectors.lib"
# Parse XDC
all_sigs=[]
with open(XDC) as f:
    for line in f:
        m=re.match(r'set_property\s+-dict\s+\{PACKAGE_PIN\s+(\S+).*?\}\s+\[get_ports\s+(\S+?)\]\s*;\s*##\s*(\S+)\s+(\S+)(?:\s+(JX\d\.\S+))?(?:\s+(\S+))?',line)
        if m:
            all_sigs.append((m.group(2),m.group(1),m.group(3),m.group(4),m.group(5) or "",m.group(6) or ""))
# Parse library
lib_pins={}
cur=None
with open(LIB) as f:
    for line in f:
        if line.startswith("DEF "): cur=line.split()[1]
        elif line.startswith("X ") and cur:
            p=line.split()
            if len(p)>=10: lib_pins.setdefault(p[1],[]).append((cur,p[2]))
# Verify
v=0; m=0
for port,ball,fmc_pin,fmc_name,jx,hp in all_sigs:
    if hp and jx:  # non-GT
        exp=jx.split(".")[1]
        if hp in lib_pins and exp in [n for _,n in lib_pins[hp]]: v+=1
        else: m+=1
    elif "MGT" in hp or hp.startswith("MGT"):  # GT
        lbl=f"FMC_{fmc_pin}_{fmc_name}"
        exp=f"{fmc_pin[0]}{int(fmc_pin[1:])}"
        if lbl in lib_pins and exp in [n for _,n in lib_pins[lbl]]: v+=1
        else: m+=1
print(f"Full verification: {v} verified, {m} mismatches (expected 65/0)")
PYEOF
```

If any of those return unexpected values, **stop and investigate before proceeding**.

---

## 7. Pending verifications (priority order)

### V2 — FMC HPC power pins in `FMC_HPC_ADRV9009` symbol
**Problem**: Sheet 2 has global labels `FMC_3P3V` (6 instances) and `VADJ` (1 instance). Neither label exists as a pin name in the `FMC_HPC_ADRV9009` symbol — those pins are still named `Pin_N`.

**What needs to happen**:
1. Look up the authoritative VITA 57.1 HPC power pin assignments from the standard (search already done in prior session — DP lane assignments from page 48, but power pins on pages ~47-48 need separate lookup)
2. Extend the Step 2 rename script to also rename the power pins on the FMC symbol: likely FMC_3P3V, VADJ, +12V, GND, VREF_A_M2C, VREF_B_M2C
3. Re-verify that all Sheet 2 power labels targeting the FMC connector find matching pins

**Approach**: Write `step2c_add_fmc_power_pins.py` modeled on `step2_fix_j4_pin_names.py`. Uses the same rename mechanism, but with a hardcoded table of VITA 57.1 power pin assignments. Back up library, apply, diff, verify.

**Authoritative source**: ANSI/VITA 57.1-2008 standard, pages 47-48 (HPC signal definitions table). Available via web search if not in project knowledge.

### V3 — VIN pin list reconciliation
**Problem**: Three sources disagree on how many JX1 pins carry VIN:

- `power.sch` line 27 comment: *"Barrel jack -> VIN net -> J1 pins A43,A46,A49,A50,B43,B44,B46,B47,B49,B50,C50,D50"* → 12 pins
- `UZEV_Connectors.lib` JX1 symbol: 8 pins named VIN (A43, A46, A49, A50, B44, B47, B50, C50 — confirmed earlier this session)
- Designer's Guide Table 26 Page 33 (user-confirmed during session): VIN appears at A43, A46, A49, A50 on the A-side and B44, B47, B50 on the B-side — that's 7 pins visible on the page 33 excerpt; page 32 may have more (D50, C50 area not yet inspected)

**What needs to happen**:
1. Have Ravv read page 32 of the Designer's Guide (Table 26 continued, the upper half with D-column and lower rows) and list all VIN entries
2. Reconcile: if Designer's Guide shows N pins and library shows the same N pins, library wins and the power.sch comment gets corrected as a documentation fix (DEC-003)
3. If library has a pin that DG doesn't mention as VIN, that's a library bug — fix with a backup and a log entry
4. Update power.sch line 27 comment to match truth (low priority)

**Do not proceed with V5 (Sheet 1 wiring) until V3 is resolved** — VIN is a multi-drop power net and the wire count matters for layout current-carrying.

### V4 — JESD rx/tx label tie strategy on Sheet 3
**Problem**: Sheet 3 has two labels for each JESD lane:
- `FMC_A02_DP1_M2C_P` (the FMC connector side)
- `rx_data_0_DP1_P` (the logical JESD lane index after ADI's non-sequential reordering)

Both are supposed to be the SAME net. But KiCad treats different label text as different nets, so currently they're floating.

**The non-sequential mapping (confirmed from XDC after DEC-002 fix):**

| Logical lane | FMC DP | FMC pins (P/N) |
|---|---|---|
| rx_data[0] | DP1 | A02/A03 |
| rx_data[1] | DP2 | A06/A07 |
| rx_data[2] | DP0 | C06/C07 |
| rx_data[3] | DP3 | A10/A11 |
| tx_data[0] | DP1 | A22/A23 |
| tx_data[1] | DP2 | A26/A27 |
| tx_data[2] | DP0 | C02/C03 |
| tx_data[3] | DP3 | A30/A31 |

**Proposed design decision (needs Ravv approval)**: Tie the labels together on Sheet 3 with short wires. For each of the 16 JESD signals, draw a wire segment between the two labels so they share a net. This keeps both names visible for documentation (FMC side for board readers, JESD side for FPGA/firmware engineers) while making them electrically equivalent. The alternative (rename one set to match the other) loses information.

**Approach**: Script that identifies each pair of labels on Sheet 3 and draws a 2.54mm wire between them. Requires reading the current label positions from the `.sch` file.

### V5 — Sheet 1 wiring (the big one)
**Scope**: 151 unique global labels need to be placed on Sheet 1 at the correct connector pins, each with a short wire stub. Breakdown from earlier analysis:

| Label group | Count | Target connector |
|---|---|---|
| FMC_*_<signal> (signal pins) | 65 | J4 (FMC_HPC_ADRV9009) |
| FMC_3P3V | 1 | J4 (after V2) |
| HP_DP_* | 45 | J1 (JX1) |
| GTH_REFCLK[01]_[PN] | 4 | J2 (JX2) |
| rx/tx_data_* | 16 | J2 (JX2) — ALSO need V4 ties |
| Power rails (MGT*, VCCO*, VADJ, VIN...) | 7 | Multi-drop J1/J2/J3 |
| Control/JTAG/MIO | 12 | J1/J3 |
| VIN | 1 | J1 multi-drop (after V3) |

**Approach**: Script that:
1. Parses each J1/J2/J3/J4 `$Comp` block to get anchor position, unit, orientation
2. Parses each symbol's pin definitions to get local pin offsets
3. Computes absolute pin coordinates
4. For each global label name on Sheets 2/3/4, finds matching pin(s) via library name match (we verified the chain holds, so this is mechanical)
5. Emits `Wire Wire Line` + `Text GLabel` for each pin
6. Writes updated `connectors.sch` with backup

**Do not start V5 until V2, V3, V4 are resolved.**

### After V5
- Re-run ERC and check for remaining errors
- Add no-connect flags to unused connector pins (~800)
- Add PWR_FLAG to any undriven power net
- Assign footprints to all components
- Generate netlist
- Begin PCB layout (8-layer stackup, GT impedance, power pours)

---

## 8. Known issues (logged, not fixed)

### KI-001 — Spreadsheet Tab 4 has same GPIO off-by-one as pre-DEC-001 XDC
**File**: `/home/arc/Transition Docs/March 16, 2026/ADRV9009_UltraZed_EV_Pin_Mapping.xlsx`, tab "PROPOSED MAPPING", "Assigned JX1 Pin" column
**Rows**: adrv9009_gpio_04 (A25→A24), gpio_05 (A26→A25), gpio_09 (C25→C24), gpio_10 (C26→C25)
**Status**: Not fixed. The spreadsheet is reference documentation, not a build input. Fix during documentation cleanup phase.

### KI-002 — Spreadsheet Tab 4 may have same DP label swap as pre-DEC-002 XDC
**Status**: Not verified. Tab 4 full dump showed FPGA ball column but didn't explicitly list DP numbers in the format V1b checked. Worth a targeted check during V2 work.

### KI-003 — power.sch line 27 comment about VIN pin count may be wrong
**File**: `/home/arc/projects/uzev_carrier_v5/power.sch` line 27
**Claim**: VIN goes to 12 J1 pins
**Reality**: Library has 8, Designer's Guide page 33 excerpt shows 7 (page 32 not yet inspected)
**Status**: Resolved as part of V3.

### KI-004 — FMC_HPC_ADRV9009 symbol missing power pin names
**File**: `/home/arc/projects/uzev_carrier_v5/UZEV_Connectors.lib`
**Pins affected**: ~40 pins still named `Pin_N` that should be `FMC_3P3V`, `VADJ`, `+12V`, `GND`, `VREF_A_M2C`, `VREF_B_M2C`
**Status**: Resolved as part of V2.

---

## 9. File state at session end

### Files modified this session
- `/home/arc/adrv9009_uzev/hdl/projects/adrv9009/zcu102/system_constr.xdc`
  - Modified by DEC-001 (4 GPIO comment fixes) and DEC-002 (10 GT comment fixes)
  - `set_property` directives byte-identical to pre-session state
  - Only `##` annotation comments changed (14 total line changes)
  - Backups preserved
- `/home/arc/projects/uzev_carrier_v5/UZEV_Connectors.lib`
  - Modified by Step 2 (FMC_HPC_ADRV9009 symbol added with 65 renamed pins)
  - Backup: `UZEV_Connectors.lib.bak.20260407_152830`
- `/home/arc/projects/uzev_carrier_v5/connectors.sch`
  - Modified by Step 2b (J4 symbol swap, 20 line changes)
  - Then touched by eeschema save (cosmetic whitespace reformat)
  - Backup: `connectors.sch.bak.20260407_154023`
- `/home/arc/projects/uzev_carrier_v5/DECISIONS_LOG.md`
  - NEW file created this session, contains DEC-001 and DEC-002

### Backup files to preserve (do not delete)
/home/arc/adrv9009_uzev/hdl/projects/adrv9009/zcu102/system_constr.xdc.bak.20260407_171827
/home/arc/adrv9009_uzev/hdl/projects/adrv9009/zcu102/system_constr.xdc.bak.before_comment_fix.20260407_173322
/home/arc/adrv9009_uzev/hdl/projects/adrv9009/zcu102/system_constr.xdc.bak.before_dec002.20260408_103058
/home/arc/projects/uzev_carrier_v5/UZEV_Connectors.lib.bak.20260407_152830
/home/arc/projects/uzev_carrier_v5/connectors.sch.bak.20260407_154023
### Files NOT touched this session
- `power.sch`, `adrv9009_signals.sch`, `support_io.sch` — untouched (eeschema did a cosmetic save-pass at 15:57 on 2026-04-07 that changed byte positions but not content)
- The pin mapping spreadsheet — untouched
- All HDL source files — untouched
- The bitstream `system_top.xsa` — untouched and still valid (WNS=+0.438ns from Step 7)

---

## 10. Working agreements (inherited from this session)

1. **Primary sources win ties.** VITA 57.1 standard → Designer's Guide → library. Anything else is a hypothesis to be checked.
2. **Backup before edit.** Every file modification gets a timestamped `.bak` first. Every fix script has sanity checks before writing.
3. **Diff after edit.** Confirm only intended changes were made.
4. **Decisions log entries for any non-trivial change.** `DECISIONS_LOG.md` at project root, newest at bottom, numbered DEC-NNN.
5. **Claude has decision authority** for technical execution. Claude asks Ravv to verify only when the check requires physical eyes on a document Claude can't read reliably (e.g., reading multi-column PDF tables).
6. **When eeschema touches a file, diff and checksum afterward** before trusting anything.
7. **Zero-tolerance verification on correctness. Startup speed on everything else.**
8. **If Claude finds itself reframing a request to make it work, that's a signal to stop and ask.**

---

## 11. Big-picture project status

| Phase | % Complete | Notes |
|---|---|---|
| HDL / bitstream (Steps 1–7) | 100% | Clean build, WNS=+0.438ns, TNS=0, 0 DRC errors |
| Schematic capture — library | ~95% | All non-power JX pins correct, FMC signal pins correct, FMC power pins missing (V2) |
| Schematic capture — Sheet 1 (Connectors) | ~5% | Symbols placed, zero wiring, zero labels |
| Schematic capture — Sheet 2 (Power) | ~90% | Complete, has 20 global labels, needs V3 resolution |
| Schematic capture — Sheet 3 (ADRV9009 Signals) | ~95% | 130 labels, needs V4 JESD ties |
| Schematic capture — Sheet 4 (Support I/O) | ~95% | 21 labels, minor cleanup expected |
| PCB layout | 0% | Not started |
| Bring-up (Petalinux, drivers) | 0% | Post-fabrication |

Estimate: after V2/V3/V4/V5, schematic capture is done, ERC should be clean (or near-clean), and the project shifts into PCB layout. That's the next major milestone.

---

*End of transition document.*
