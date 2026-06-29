# UZEV ADRV9009 Carrier Board — Transition Doc v6 FINAL

**Generated:** 2026-05-25
**Status:** FINAL — ERC 14 confirmed 0 errors, 0 warnings. All phases through ADD_REV1 complete.
**Supersedes:** v6 DRAFT (2026-04-16). v2/v3/v4/v5 still valid for historical context.
**Project:** Defense-grade SDR datalink carrier for UAV/GCS comms

---

## 0. READ FIRST

You are continuing a defense-grade carrier board project. **Zero tolerance for correctness errors.** Primary sources outrank all derived artifacts.

**First actions:**
1. Read CLAUDE.md — edit approval protocol is mandatory. Re-confirm approval state before any file edit.
2. Read this doc fully.
3. `cat /home/arc/projects/uzev_carrier_v5/DECISIONS_LOG.md` — confirm DEC-032 is present.
4. Run opening audit (Section 7).
5. If audit GREEN → proceed to Section 6 (next steps).

**DO NOT:**
- Make any schematic edit without explicit per-edit user approval (CLAUDE.md protocol).
- Trust v2 memory's "ADP7104 (2A)" or "TPS7A4901 (1A)" claims — both are FALSE (DEC-013).
- Use `bash_tool` heredoc for log edits — has caused triple-append in this project. Use Python with idempotency guards (DEC-013 pattern).
- Add PWR_FLAGs only to power.sch for new voltage rails — see Section 3 KiCad gotcha.
- Start PCB layout before footprint assignment is complete (Phase 7, next step).

---

## 1. Project identity

- **SOM:** Avnet UltraZed-EV (XCZU7EV-1FBVB900E)
- **RFIC:** ADI ADRV9009-W/PCBZ via FMC HPC
- **Toolchain:** Vivado 2022.2 Standard, KiCad 5.1.5, ADI HDL `hdl_2022_r2`
- **OS:** Ubuntu 20.04, all project files under `/home/arc/`
- **Bitstream:** built clean, WNS=+0.438ns. Unchanged since v4.
- **KiCad project:** `/home/arc/projects/uzev_carrier_v5/uzev_adrv9009_carrier.pro`
- **Sheets:** connectors.sch (1), power.sch (2), adrv9009_signals.sch (3), support_io.sch (4)
- **Design intent:** Sized-down ZCU106 with same capabilities except those physically unavailable on FBVB900E package. ZCU106 schematics and power architecture are the primary reference.

---

## 2. Authoritative sources (rank order)

| Rank | Source | Authority for |
|---|---|---|
| 1 | ANSI/VITA 57.1 (`FMCAV57DOT1.pdf`) | FMC HPC pins, power, signaling |
| 2 | Avnet Designer's Guide (`UGAESZU7EVSOMGV1_2.pdf`) | JX pins, SOM voltages, currents |
| 3 | Avnet SOM Schematics (`PRJUS2SOM10103SchematicPrints.pdf`) | FPGA-ball ↔ JX physical routing |
| 4 | Datasheets (`TPS54320.pdf`, `TPS54531.pdf`, `TPS7A85.pdf`, `ADP7104.pdf`, `tlv1117.pdf`) | Buck/LDO part specs |
| 5 | ZCU106 schematics (AMD/Xilinx, public) | Interface/power reference for parity decisions |
| 6 | `UZEV_Connectors.lib` | KiCad pin coords (verified) |
| 7 | `system_constr.xdc` | PACKAGE_PIN bindings |
| — | `ADRV9009_UltraZed_EV_Pin_Mapping.xlsx` | **WRONG on gpio_04/05/09/10** — reference only |

---

## 3. Working agreements

- Primary sources win ties.
- Backup before edit, diff after edit.
- DEC-NNN entries in DECISIONS_LOG.md for every decision.
- Stop and ask if reframing user's request.
- **Log edits:** python-only with idempotency guards. Pattern from DEC-013 fix:
  1. Read clean baseline backup
  2. Build new content in memory
  3. Verify counts pre-write
  4. Write to `.tmp`, then `os.replace()` for atomic swap
- Hash mismatches require structural parse, not reflexive restore (DEC-012).
- **Edit approval (CLAUDE.md):** Every schematic edit requires explicit per-edit user approval. Diagnosis + primary source citation + proposed diff → wait. "Pending" in a doc means "ready to propose," not "ready to apply."

### KiCad 5.1.5 gotcha — cross-sheet PWR_FLAG scope (DEC-014)

**PWR_FLAGs are sheet-local in KiCad 5.1.5 ERC.** A PWR_FLAG on power.sch does NOT satisfy W-type (power input) pins on connectors.sch for the same named net. Component `w`-type output pins (e.g., LDO/Buck output pins) propagate globally and satisfy W-type pins on every sheet.

**Current state:** VIN is the only net whose sole driver is a PWR_FLAG (#FLG_V01 on power.sch, #FLG01 on connectors.sch — added DEC-014). All power rail outputs (MGTAVCC, MGTAVTT, VCCO_HP_65/64, FMC_3P3V) are driven by LDO/Buck `w`-type output pins in power.sch — globally propagated, no replication needed. +3V3 for SD card J8 has #FLG_SD01 on support_io.sch (DEC-032).

**Rule:** Any new net whose only driver is a PWR_FLAG must have that flag on every sheet where the net has W-type pins.

---

## 4. State at end of this session (2026-05-25)

### Phase completion summary

| Phase | Status | Key DECs |
|-------|--------|----------|
| 1–4: Connector/signal stubs | COMPLETE ✓ | DEC-001 through DEC-012 |
| 5a: Symbol library | COMPLETE ✓ | DEC-010, DEC-019 (Buck_ENPG/LDO_ENPG added) |
| 5b: LDO wiring (legacy) | COMPLETE ✓ | DEC-013/014 — superseded by 5c rewrite |
| 5c: Power tree redesign (Architecture B) | COMPLETE ✓ — DEF-11 CLOSED | DEC-019 through DEC-028 |
| 6: NoConn flag sweep (810 flags) | COMPLETE ✓ | DEC-029 |
| CRIT-1: tx_sync_1 routing | COMPLETE ✓ | DEC-030/031 |
| ADD_REV1: SD card J8 (MIO45-51) | COMPLETE ✓ | DEC-032 |
| **Phase 7: Footprint assignment** | **PENDING — next step** | — |

### File hashes (post DEC-032)

| File | Bytes | MD5 |
|---|---|---|
| `UZEV_Connectors.lib` | 64313 | `55a6352265bd284d8ffab7a67f2f0e08` |
| `connectors.sch` | 43070 | `0377a743d1d3fc07bb2aeb4394f67ba2` |
| `power.sch` | 32495 | `4922751bd9b52f966b395b021c877bc9` |
| `adrv9009_signals.sch` | 21227 | `e0d870dacab2bcf0028b8c255f9fb0f6` |
| `support_io.sch` | 14504 | `34c0a2aeb89bbd37e8e34374e4718a6d` |

### ERC state

**ERC 14** (`14uzev_adrv9009_carrier.erc`, 2026-05-25 14:16): **0 errors, 0 warnings.** All four sheets clean.

ERC history: 798 → 836 → 831 → 826 → 835 → 826 → 838 → 0 → 0 (+4W) → 0 → **0/0**

### Power tree (Architecture B, DEC-019)

| Component | Part | Role | Output |
|-----------|------|------|--------|
| B1 TPS54320 | 3A sync buck | 12V → VMGTAVCC_PRE (1.5V) | L1 input |
| B2 TPS54320 | 3A sync buck | 12V → VMGTAVTT_PRE (1.8V) | L2 input |
| B3 TPS54320 | 3A sync buck | 12V → VVCCO65_PRE (2.5V) | L3 input |
| B4 TPS54320 | 3A sync buck | 12V → VVCCO64_PRE (2.5V) | L4 input |
| B5 TPS54531 | 5A buck | 12V → FMC_3P3V (3.3V) | direct |
| L1 TPS7A85 | 4A LDO | VMGTAVCC_PRE → MGTAVCC (0.9V) | SOM |
| L2 TPS7A85 | 4A LDO | VMGTAVTT_PRE → MGTAVTT (1.2V) | SOM |
| L3 TPS7A85 | 4A LDO | VVCCO65_PRE → VCCO_HP_65 (1.8V) | SOM |
| L4 TPS7A85 | 4A LDO | VVCCO64_PRE → VCCO_HP_64 (1.8V) | SOM |

Rfb networks: R13–R30 (18 resistors, 9 divider pairs), 100kΩ lower, upper sets Vout (DEC-028).
Sequencing: SOM_PG_OUT → Buck EN → Buck PG → LDO EN.

### connectors.sch state

- JX1/JX2/JX3/FMC stubs: 175 Wire+GLabel pairs (DEC-011)
- 753 NoConn flags on unused pins (DEC-029)
- tx_sync_1: J1-B36 = FMC_H31_LA28_P, J1-B37 = FMC_H32_LA28_N (direct naming, DEC-031)
- SD1 MIO45-51: 7 GLabel stubs on J3 (DEC-032)
- VIN: #FLG01 PWR_FLAG (DEC-014)

### support_io.sch state

- J7 JTAG (6-pin): fully wired via R6–R9 isolation resistors (DEC-017)
- J6 UART: NoConn flags on pins 1–3 (TX/RX/VCC) — these signals remain unrouted
- J8 SD card (Micro_SD_Card_Det): added DEC-032, MIO45-51, DNP for flight builds
- 22 NoConn flags on other unused pins (DEC-029)
- All 5 GND symbols connected to global GND net (DEC-014/DEC-014b)

### adrv9009_signals.sch state

- All ADRV9009 FMC signals routed (DEC-007)
- tx_sync_1 floating wire stubs present (cosmetic, harmless — routing handled in connectors.sch per DEC-031)
- 0 NoConn flags needed (all pins used)

---

## 5. Decisions log summary (DEC-001 through DEC-032)

Full log at `/home/arc/projects/uzev_carrier_v5/DECISIONS_LOG.md` (33 headings).

**DEC-001 through DEC-018:** see v6 DRAFT for detail.

Recent decisions (new since v6 DRAFT):

| DEC | Date | Summary |
|-----|------|---------|
| DEC-019 | 2026-04-27 | DEF-11: Architecture B adopted — TPS54320 bucks + TPS7A85 LDOs; power.sch rewritten Rev 2.0 |
| DEC-020 | 2026-04-29 | Design intent locked: ZCU106 parity target; Python atomic scripts as preferred methodology |
| DEC-021 | 2026-04-29 | Scope triage: JTAG/UART/SD keep; eMMC/GbE/USB deferred; SD DNP for flight |
| DEC-022 | 2026-04-29 | SOM QSPI confirmed as primary boot (not carrier); SD1 sole carrier storage |
| DEC-023 | 2026-04-29 | C4/C5/C6 duplicate refdes → C17/C18/C19; hash drift accepted |
| DEC-024 | 2026-04-30 | Deleted redundant PWR_FLAGs #FLG_P01–P05 (ErrType(5) fix) |
| DEC-025 | 2026-04-30 | Renamed duplicate #PWR001–004 → #PWR026–029 (ErrType(3) fix) |
| DEC-026 | 2026-05-05 | Added GND tie wires for L1/L4 isolated GND clusters |
| DEC-027 | 2026-05-06 | Fixed C10/C11 50-mil wire endpoint error; added #FLG_V02 PWR_FLAG for GND net |
| DEC-028 | 2026-05-06 | Rfb divider networks R13–R30 added to power.sch — closes DEF-11 |
| DEC-029 | 2026-05-06 | NoConn sweep: 753+35+22=810 flags; ERC 10 → 0/0; DEF-11 officially closed |
| DEC-030 | 2026-05-22 | tx_sync_1 GLabels added to adrv9009_signals.sch + connector stubs — net merge failed |
| DEC-031 | 2026-05-25 | tx_sync_1 fixed via direct naming in connectors.sch; DEC-030 changes reverted |
| DEC-032 | 2026-05-25 | ADD_REV1: J8 SD card added to support_io.sch; MIO45-51 wired on J3; ERC 14 → 0/0 |

---

## 6. NEXT STEPS

### Phase 7 — Footprint assignment (CURRENT PRIORITY)

All schematic symbols need PCB footprints before netlist export → PCB layout.

**Unassigned / needs verification:**

| Component | Value | Current footprint | Action needed |
|-----------|-------|------------------|---------------|
| B1–B4 | TPS54320 | — | Assign `Package_TO_SOT_SMD:SOT-23-8` or TI `DDA` pkg (WSON-8 per datasheet) |
| B5 | TPS54531 | — | Assign TI `DDA` pkg (HSOP-8 PowerPAD) |
| L1–L4 | TPS7A85 | — | Assign TI `DDA` pkg (WSON-10) |
| R13–R30 | various kΩ | — | Assign `Resistor_SMD:R_0402_1005Metric` (per DEC-028) |
| J8 | Micro_SD_Card_Det | Hirose DM3AT-SF-PEJM5 | Verify footprint exists in lib; may need custom |
| J7 | JTAG Conn_01x06 | — | Assign standard 2.54mm THT footprint |
| J6 | UART Conn_01x04 | — | Assign standard 2.54mm THT footprint |
| C17–C19 | 100nF/47µF/10µF | — | Assign `Capacitor_SMD:C_0402` / `C_0805` per value |
| C10–C11 | MGTVCCAUX bypass | — | Assign appropriate SMD cap footprint |

**Process (KiCad 5.1.5):**
- Open project → eeschema → Tools → Edit Symbol Fields → assign footprint column
- Or: CvPcb tool (Assign Footprints) for bulk assignment
- After all footprints assigned: File → Export Netlist → KiCad format → open in pcbnew

**After footprint assignment:**
- Run ERC again to catch any footprint-pin count mismatches
- Export BOM (File → Export → BOM) — cross-check against BOM_snapshot_20260428_v2.xlsx
- Export netlist → import into pcbnew for layout

### Parallel items

- **J6 UART wiring:** Pins 1–3 currently have NoConn flags. If UART is to be functional, extend wires 600 mils to reach J6 pins and wire TX/RX/VCC before PCB. Low priority; can DNP J6 if JTAG console is sufficient.
- **DEF-5:** XDC missing sysref clock constraint — still open, low priority, does not block PCB.
- **CLAUDE.md:** Working agreement "Do not send to PCB layout while DEF-11 is open" is now stale — DEF-11 is closed. Update when convenient.
- **BOM:** J8 and ESD array (PRTR5V0U2X or equiv) must be marked DNP for flight builds per DEC-021/022.

---

## 7. Opening audit (paste at start of next session)

```bash
cd /home/arc/projects/uzev_carrier_v5
python3 << 'PYEOF'
import os, hashlib, re
EXP={
 'UZEV_Connectors.lib':  ('55a6352265bd284d8ffab7a67f2f0e08', 64313),
 'connectors.sch':       ('0377a743d1d3fc07bb2aeb4394f67ba2', 43070),
 'power.sch':            ('4922751bd9b52f966b395b021c877bc9', 32495),
 'adrv9009_signals.sch': ('e0d870dacab2bcf0028b8c255f9fb0f6', 21227),
 'support_io.sch':       ('34c0a2aeb89bbd37e8e34374e4718a6d', 14504),
}
ok=True
for f,(em,es) in EXP.items():
    if not os.path.exists(f): print(f'MISSING {f}'); ok=False; continue
    am=hashlib.md5(open(f,'rb').read()).hexdigest(); az=os.path.getsize(f)
    s='OK' if (am==em and az==es) else 'DRIFT'
    print(f'{s}: {f} size={az} md5={am}')
    if s!='OK': ok=False
log=open('DECISIONS_LOG.md').read()
heads=len(re.findall(r'^## ',log,re.MULTILINE))
print(f'{"OK" if heads==33 else "DRIFT"}: log headings={heads} expect=33')
print(f'{"OK" if "DEC-032" in log else "MISSING"}: DEC-032 present')
cs=open('connectors.sch').read()
nc=cs.count('NoConn ~')
print(f'connectors.sch: NoConn flags={nc} (expect 753)')
ps=open('power.sch').read()
pw=ps.count('Wire Wire Line')
print(f'power.sch: wires={pw}')
ss=open('support_io.sch').read()
j8=ss.count('Micro_SD_Card_Det')
print(f'support_io.sch: J8 SD card present={j8>0}')
print('AUDIT COMPLETE' if ok else 'AUDIT DRIFT — investigate before editing')
PYEOF
```

---

## 8. Open defects

| ID | Priority | Status | Notes |
|---|---|---|---|
| DEF-1 | low | known | Spreadsheet wrong on gpio_04/05/09/10 — use Designer's Guide |
| DEF-2 | low | RESOLVED | SOM_PG_OUT gating handles MGT sequencing |
| DEF-3..10 | low | open | See v2 doc Section 9 |
| DEF-5 | med | open | XDC missing sysref clock constraint |
| DEF-11 | HIGH | **CLOSED** (DEC-028/029) | Power tree redesign complete; Architecture B applied |
| DEF-12 | med | CLOSED | J7 JTAG wired (DEC-017); tx_sync_1 routed (DEC-031) |

---

## 9. Token-efficiency note for next Claude

User has explicitly requested terse replies and minimal token usage. Standard mode:
- User asks → short response + script to paste
- User pastes output → analyze + next script
- No long prose unless explicitly requested
- No restating what user already knows
- For log edits: always python+atomic, never bash heredoc

---

## 10. Key file paths

- Project: `/home/arc/projects/uzev_carrier_v5/`
- HDL: `/home/arc/adrv9009_uzev/hdl/`
- XDC: `/home/arc/Desktop/system_constr.xdc` (not in project dir)
- Backups in project dir: `*.bak.*`

---

## 11. ERC workflow note (KiCad 5.1.5)

`kicad-cli` is not available in this installation. ERC must be run via the GUI:
- Open project in KiCad → eeschema → Tools → Electrical Rules Checker → Run
- Static analysis (Python hash + structural parse) can validate geometry and predict results, but final confirmation requires GUI ERC
- When reporting ERC results, paste exact counts in format: `ErrType(N): count`

---

**END v6 FINAL**
