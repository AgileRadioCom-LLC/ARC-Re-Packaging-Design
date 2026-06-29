# UZEV ADRV9009 Carrier Board — Session Transition v6

**Generated:** 2026-04-29  
**Session type:** End-of-session handoff  
**Status:** Phase 5c pending (power tree feedback resistors); all other sheets stable

---

## 0. Opening protocol for next session

1. Read this document first.
2. Run state verification commands from Section 6.
3. Confirm approval state with user before any bash/edit/write on project files.

---

## 1. Project identity

- **Project:** Defense-grade SDR datalink carrier board for UAV/GCS
- **Design intent (locked, DEC-020):** Sized-down ZCU106 — same capabilities as ZCU106
  except those physically unavailable due to UltraZed-EV SOM FBVB900E package restrictions.
  Same FPGA silicon (XCZU7EV), different package (FBVB900E vs FFVC1156 on ZCU106).
  ZCU106 schematics and power architecture are primary references for all interface,
  power, and peripheral decisions.
- **Platform:** Avnet UltraZed-EV SOM (XCZU7EV-1FBVB900E) + ADI ADRV9009-W/PCBZ
- **SOM↔RFIC interface:** FMC HPC (custom ADRV9009 FMC card plugs into carrier J4)
- **SOM↔carrier interface:** Samtec SEARAY micro-headers JX1/JX2/JX3 (J1/J2/J3)
- **FPGA toolchain:** Vivado 2022.2 Standard Edition
- **ADI HDL branch:** `hdl_2022_r2`, tag `2022_r2_p1`
- **Schematic tool:** KiCad 5.1.5 at `/usr/bin/` (NOT KiCad 9 AppImage — broken)
- **Project directory:** `/home/arc/projects/uzev_carrier_v5/`
- **HDL working tree:** `/home/arc/adrv9009_uzev/hdl/`

---

## 2. Authoritative sources (ranked)

1. ANSI/VITA 57.1-2008 — FMC HPC pinout authority
2. Avnet UltraZed-EV Designer's Guide (`UGAESZU7EVSOMGV1_2.pdf`) — SOM pin mappings
3. ZCU106 schematics (AMD/Xilinx public) — interface and power architecture reference
4. `UZEV_Connectors.lib` — verified correct for JX1/JX2/JX3 and FMC signal pins
5. XDC `system_constr.xdc` — `set_property` directives correct; `##` comments corrected by DEC-001/002/008

**Wrong sources:**
- `ADRV9009_UltraZed_EV_Pin_Mapping.xlsx` Tab 4: off-by-one on gpio_04/05/09/10 (KI-001)

---

## 3. Schematic state at session end

| Sheet | File | Status | Notes |
|-------|------|--------|-------|
| 1 — Connectors | connectors.sch | Stubs emitted (DEC-011) | ~351 wire/label lines; no-connect flags not yet added to unused pins |
| 2 — Power | power.sch | Architecture B placed (DEC-019) | Phase 5c incomplete: Rfb resistors missing |
| 3 — ADRV9009 Signals | adrv9009_signals.sch | Complete | JESD ties done (DEC-005/007) |
| 4 — Support I/O | support_io.sch | Complete | JTAG (DEC-015/017), UART, LED, reset |

**ERC state (last run — pre DEC-019 rewrite, stale):**
- 875 ErrType(2): unused pins without no-connect flags (expected, deferred)
- 6 ErrType(3): VIN and J2 power pins not driven by PWR_FLAG

---

## 4. Open defects and pending work

### DEF-11 — ACTIVE — BLOCKS PCB LAYOUT
Power tree Phase 5c incomplete. Missing from power.sch:
- Rfb dividers for B1–B4 (TPS54320) to set intermediate voltages:
  - B1: VMGTAVCC_PRE = 1.5V
  - B2: VMGTAVTT_PRE = 1.8V
  - B3: VVCCO65_PRE = 2.5V
  - B4: VVCCO64_PRE = 2.5V
- Rfb dividers for L1–L4 (TPS7A85) to set final rail voltages:
  - L1: MGTAVCC = 0.9V
  - L2: MGTAVTT = 1.2V
  - L3: VCCO_HP_65 = VADJ = 1.8V (FIXED — never adjustable)
  - L4: VCCO_HP_64 = 1.8V
- Rfb for B5 (TPS54531) for FMC_3P3V = 3.3V (direct buck, no LDO)

### DEF-12 — OPEN (lower priority)
C4/C5/C6 duplicate-refdes conflict in power.sch (VIN bulk caps and stage caps share refdes).
Three ERC errors will result. Fix: rename conflicting caps to C17/C18/C19 or next available.

### Pending — ERC cleanup (after Phase 5c)
- Add ~870 no-connect flags to unused JX/FMC pins
- Add PWR_FLAG to VIN net and J2 power pins (6 ErrType(3) errors)

---

## 5. Decisions summary (all sessions)

| DEC | Date | Summary |
|-----|------|---------|
| DEC-001 | 2026-04-07 | GPIO 04/05/09/10 JX1 pin authority → library |
| DEC-002 | 2026-04-07 | XDC GT lane DP label corrections (comments only) |
| DEC-003 | 2026-04-08 | FMC power/control pin rename in library |
| DEC-004 | 2026-04-08 | VIN pin list reconciliation (8 pins confirmed) |
| DEC-005 | 2026-04-08 | JESD label tie strategy — short wire approach |
| DEC-006 | 2026-04-13 | J2/J3 reference label swap in connectors.sch |
| DEC-007 | 2026-04-13 | Sheet 3 topology fix: misplaced labels + 47 tie wires |
| DEC-008 | 2026-04-13 | XDC comment typo fix (superseded by DEC-009) |
| DEC-009 | 2026-04-13 | DEC-008 invalidated; Designer's Guide is authoritative |
| DEC-010 | 2026-04-13 | FMC library completeness fix (6 pin renames) |
| DEC-011 | 2026-04-13 | V5 Phase 3: stub emission to connectors.sch |
| DEC-012 | 2026-04-14 | connectors.sch cosmetic re-save accepted |
| DEC-013 | 2026-04-14 | Phase 5b Q1-Q6 verified, DEF-11 opened, option γ approved |
| DEC-014 | 2026-04-16 | Phase 5b cleanup: PWR_FLAG for GND and VIN |
| DEC-014b | 2026-04-16 | support_io.sch: second floating GND symbol fixed |
| DEC-015 | 2026-04-16 | JTAG programmer (Digilent JTAG-HS3) and J7 pinout selected |
| DEC-016 | 2026-04-22 | power.sch baseline drift accepted |
| DEC-017 | 2026-04-22 | JTAG J7 wiring via Option C Python scripts |
| DEC-018 | 2026-04-22 | support_io.sch design notes refdes corrections |
| DEC-019 | 2026-04-27 | DEF-11: Architecture B adopted (TPS54320+TPS7A85) |
| DEC-020 | 2026-04-29 | Design intent locked to ZCU106 parity; references adopted |
| DEC-021 | 2026-04-29 | Mission-driven scope triage: SD ADD_REV1, eMMC/GbE/USB DEFER_REV2 |
| DEC-022 | 2026-04-29 | SOM QSPI confirmed PROVIDED_BY_SOM; SD card sole carrier storage addition Rev 1 |

---

## 6. Next steps (ordered, dependency-sequenced)

Boot path: JTAG+Vitis for bring-up → SOM onboard QSPI for production flight.
QSPI boot requires no carrier change (DEC-022: SOM has 256Mb Micron QSPI on PS MIO0–5,
not exposed to JX; standard FSBL/PetaLinux boot source). See bringup_boot_flow.md.

### Step 1 — Close J7 JTAG wiring (Phase 5b finalization)
Verify J7 JTAG header is fully wired in support_io.sch per DEC-015/017. Confirm
no-connect flags on unused J7 pins. Resolve DEF-12 (C4/C5/C6 duplicate-refdes in
power.sch — rename to next available refdes). Re-run ERC baseline.

### Step 2 — Add SD card slot to schematic (ADD_REV1 per DEC-021/022)
Source: ZCU106 schematic PS peripherals sheet (SD1 card interface); MIO assignment
per UG1085 Chapter 29 (SD/eMMC Controller, Table 29-3: SD1 MIO pin functions).
- MIO46: SD1_CLK, MIO47: SD1_CMD, MIO48–51: SD1_DATA[0:3]
- Optional: MIO45 card-detect, MIO43 write-protect (confirm JX3 availability first)
Add micro-SD slot symbol + footprint to support_io.sch.
Route MIO46–51 from JX3 on connectors.sch.
Verify MIO46–51 appear on JX3 in Designer's Guide Table 26 before any edit.
DNP (Do Not Populate) option: add BOM note for flight builds.
ESD: use ZCU106 reference topology (PRTR5V0U2X or equivalent TVS on data lines).
Voltage level: PS MIO bank for SD1 is powered at 1.8V on UltraZed-EV; micro-SD
cards running at 1.8V UHS-I mode are compatible — confirm with card spec before fab.

### Step 3 — Phase 5c power redesign (sized for SOM + SD card load)
SD card adds ≤100 mA to 3.3V rail (UHS-I max). B5 (TPS54531, 5A) headroom is
adequate — existing 3A FMC allocation >> SD addition. No resizing required.
Primary work: add Rfb resistor networks for all 5 buck stages and 4 LDO stages.
Compute Rfb values from TPS54320, TPS54531, TPS7A85 datasheets.
Add MGTVCCAUX PWR_FLAG on connectors.sch.
Fix DEF-11; close it. DEF-11 closure unblocks PCB layout.

### Step 4 — CRIT-1 Sheet 3 / adrv9009_signals.sch audit (parallel with Step 3)
Verify all JESD tie wires are electrically correct after DEC-007. Confirm no orphaned
labels. Re-run ERC on Sheet 3 only. Parallel with power work; no dependencies.

### Step 5 — Footprint assignment
Assign footprints to any NEEDS_FOOTPRINT items (check BOM_snapshot_v2). Verify all
power-tree ICs have correct VQFN/PowerPAD footprints per their package codes.

### Step 6 — Phase 6 no-connect flag sweep
Add no-connect flags to ~870 unused JX/FMC connector pins (ErrType(2) errors).
Target: ERC zero errors or documented accepted exceptions only.

### Step 7 — PCB layout
DEF-11 must be closed before starting. 8-layer stackup, GT impedance, power pours.
ZCU106 layer stack and power plane arrangement is primary reference.

---

## 7. State verification commands

```bash
# Confirm power.sch is Rev 2.0 (DEC-019)
head -15 /home/arc/projects/uzev_carrier_v5/power.sch | grep Rev

# Confirm component counts (all four sheets)
for f in connectors adrv9009_signals power support_io; do
  echo -n "$f: "; grep -c "^\$Comp" /home/arc/projects/uzev_carrier_v5/${f}.sch 2>/dev/null || \
  python3 -c "import re; c=open('/home/arc/projects/uzev_carrier_v5/${f}.sch').read(); print(len(re.findall(r'\\\$Comp\n', c)))"
done

# Confirm DECISIONS_LOG has DEC-020 through DEC-022
grep "DEC-02[012]" /home/arc/projects/uzev_carrier_v5/DECISIONS_LOG.md | head -3

# Confirm CLAUDE.md has Design intent section
grep "## Design intent" /home/arc/projects/uzev_carrier_v5/CLAUDE.md
```

---

## 8. File hashes at session end

| File | md5 |
|------|-----|
| CLAUDE.md | (run md5sum to verify) |
| DECISIONS_LOG.md | 26c39a7c360effe157d31b6b3410da5b |
| power.sch | 36675a02ad64a536ff21468faaddae66 (post DEC-019) |
| connectors.sch | (verify against last known good) |
| support_io.sch | ac1a54d99fdde60ed5836ed443eb38e2 (post DEC-018) |
| UZEV_Connectors.lib | 4c2cf0499241e8e2dbc28cd304ca8162 (post DEC-019) |

---

## 9. Big-picture status

| Phase | % Complete | Blocking on |
|-------|-----------|-------------|
| HDL / bitstream | 100% | — |
| Library | 98% | — |
| Sheet 1 — Connectors | ~60% | No-connect flags; Phase 5c gotcha (new rails need PWR_FLAG here too) |
| Sheet 2 — Power | ~70% | Phase 5c (DEF-11 ACTIVE) |
| Sheet 3 — ADRV9009 | 98% | — |
| Sheet 4 — Support I/O | 99% | — |
| ERC clean | ~10% | Phase 5c + no-connect sweep |
| PCB layout | 0% | DEF-11 closed |

---

*End of transition document v6.*
