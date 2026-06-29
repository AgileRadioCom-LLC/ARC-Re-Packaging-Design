# UZEV ADRV9009 Carrier Board Project

Defense-grade SDR datalink carrier. Zero-tolerance for correctness errors.

## Design intent

UZEV carrier card design intent (locked): a sized-down ZCU106 with the
same capabilities, except those physically unavailable due to the
UltraZed-EV SOM's pin/package restrictions. Same FPGA silicon family
as ZCU106 (XCZU7EV) but in FBVB900E package vs ZCU106's FFVC1156.
ZCU106 schematics and power architecture are the primary reference
for all interface, power, and peripheral decisions.

## Methodology preference

For schematic edits, prefer Python atomic-edit scripts (read-modify-
write with .tmp + os.replace, pre-write verification, hash logging)
over manual KiCad GUI work. Pattern proven in DEC-017 Option C J7
wiring. Manual GUI is fallback only.

## Reference materials

- Primary hardware reference: ZCU106 schematics (download from AMD/
  Xilinx documentation, public)
- Primary HDL reference: ADI hdl_2022_r2 branch, adrv9009/zcu102 sub-
  project (functional, retarget to zcu106 sources is future work)
- Power architecture reference: ZCU106 power tree (TI WEBENCH-derived
  reference designs, public schematic)
- Pin assignment reference: ZCU106 XDC + UltraZed-EV Designer's Guide
  (cross-reference for pin availability)

## Working agreements
- Primary sources outrank derived artifacts: VITA 57.1 → Designer's Guide → SOM schematic → library
- Backup before edit, diff after edit, every time
- All decisions logged as DEC-NNN in DECISIONS_LOG.md
- Stop and ask if reframing the user's request to make it work
- Log edits use python with atomic write (os.replace), never bash heredoc
- DEF-11 is CLOSED (DEC-028/029). Footprint assignment (Phase 7) is the gate before PCB layout.

## Always read at session start
- `transition_docs/uzev_session_transition_v6.md` for current state
- DECISIONS_LOG.md for decision history (confirm DEC-032 present, 33 headings)
- Terse replies always. No preamble. No tables unless asked. No examples unless asked.

## Authoritative sources (read-only, in project knowledge)
- ANSI/VITA 57.1 spec
- Avnet UltraZed-EV Designer's Guide (UGAESZU7EVSOMGV1_2.pdf)
- Avnet SOM Schematics (PRJUS2SOM10103SchematicPrints.pdf)
- ADP7104, TLV1117, TPS7A49, TPS54320, TPS54531, TPS7A85 datasheets
- ZCU106 schematics (AMD/Xilinx, public) — primary interface/power reference

## Known wrong sources
- ADRV9009_UltraZed_EV_Pin_Mapping.xlsx — wrong on gpio_04/05/09/10, use Designer's Guide

## Edit approval protocol
- NEVER make schematic edits without explicit per-edit approval from user
- If a new bug is discovered mid-task, STOP and report. Do not auto-fix.
- Every edit must be preceded by: diagnosis + primary source + proposed diff + wait for approval
- After context compaction, re-verify approval boundary before any edit
- NEVER apply edits without explicit per-edit approval, even if diagnosed from prior sessions or listed in transition docs
- "Pending" in a transition doc means "ready to propose," not "ready to apply"
- On session resume after compaction, FIRST action is to confirm current approval state with user, before any bash/edit/write tool call touches project files
- If a new bug is discovered during verification, STOP and report. Do not auto-fix.

## Proactive investigation is encouraged

When working on a specific task, Claude Code should:
- Look for related issues in the same area (other floating symbols
  when fixing one, sibling bugs when fixing one, pattern instances
  when fixing one case)
- Audit beyond the literal request when the scope is tightly related
- Report ANY findings beyond the immediate task, including ones that
  seem unimportant

When findings are made:
- STOP before any edit or fix
- Report the finding with full context (location, evidence, hypothesized
  cause, severity)
- Present options (fix now / defer / investigate further / ignore)
- Wait for user decision

The goal: user gets surprise-free transparency into the project state.
Claude Code finds problems early but never acts unilaterally on them.

Examples of desired behavior:
- Fixing one floating GND → sweep for all floating power symbols →
  report each one found
- Fixing one wire gap → check nearby wires for similar generation
  artifacts → report patterns
- Resolving one label mismatch → check for other instances of the
  same naming convention → report scope

## FIRST-BOOT-READINESS GATE (NON-NEGOTIABLE)

This project demands 100% confidence the board works on the FIRST
fab spin. No Rev A failure is acceptable. Gerbers do not ship until
this gate passes.

CORE PRINCIPLE: ERC-clean is NOT boot-ready. ERC verifies
connectivity only. The defects that kill a first boot are almost all
ERC-INVISIBLE. This project has already found five such defects that
passed ERC clean (DEF-14 MGTVCCAUX noise, DEF-19 missing MGTRAVCC/
RAVTT rails, DEF-21 D20 sense-pin shorted to GND, DEF-22 floating
LDO enables, DEF-15 series-cap short). Every one would have produced
a dead or marginal board. Assume more remain until verified.

Before netlist export / before layout / before Gerber, a pre-layout
boot-readiness verification MUST pass on all seven items. Each is a
known first-boot killer. None is caught by ERC:

1. RAIL COMPLETENESS — every rail the SOM expects is present at
   correct V and I. Verify Designer's Guide Table 18 + SOM HW User
   Guide Table 32/33 LINE BY LINE against power.sch. Confirm each
   rail is either carrier-supplied-and-present or SOM-internal. A
   single missing rail = dead boot (this is how DEF-19 happened).

2. SEQUENCING — bring-up order matches SOM requirement (Designer's
   Guide §4.16 groups, DS925 GTH order). Wrong order = fails to exit
   reset or out-of-spec ramp current. (DEF-20.)

3. ENABLES + POWER-GOOD — no floating enables; open-drain PG pins
   have pull-ups to a defined rail; PG→EN chain levels defined at
   every phase. (DEF-22 pattern.)

4. BOOT CONFIG — boot-mode strap pins set correctly for the intended
   boot source, AND that boot source is actually populated (not DNP).
   A board with no configured/populated boot path boots to nothing.
   [STATUS: VERIFIED PASS 2026-06-16 — DEC-047. Boot mode = SW2 on SOM
   (no carrier straps). JTAG J7: VREF=1.8V, R6-R9 DNP isolation. SD J8:
   7 signals complete, DNP for flight per DEC-021. Source: UG-AES-ZU7EV-
   SOM-G-V1.2 §2.15 Table 30.]

5. RESET / POR — reset chain (SOM_RESET_IN_N, POR) correct, not held
   asserted, not floating; any required POR delay present.
   [STATUS: VERIFIED PASS 2026-06-16 — DEC-048. PS_POR_B SOM-internal.
   SOM_RESET_IN_N: R10+SW1, not held asserted. CC_RESET_OUT_N: R12 pullup.
   Two stale comments flagged (non-blocking). Source: UG-AES-ZU7EV-SOM-
   G-V1.2 §2.13.1/§2.13.3.]

6. DECOUPLING — decoupling cap complement on every rail matches
   UG583 per-rail tables (count + value + voltage). Missing
   decoupling = unstable rails = marginal/no boot.
   [STATUS: VERIFIED PASS 2026-06-16 — DEC-046. All 7 carrier-supplied
   rails meet or exceed UG583/UG576 minimums. 1 GTH group (FBVB900).
   No gaps. Source: UG583 Table 1-10/4-2; UG576 Table 5-5/5-8/5-9.]

7. DIFF-PAIR INTEGRITY — every GT/JESD204B lane and every refclk is
   a COMPLETE P/N pair with CORRECT polarity. A swapped or half-
   missing pair passes ERC and kills the link.
   [STATUS: VERIFIED PASS 2026-06-16 — DEC-049. 8 JESD204B lane pairs
   (4 RX + 4 TX, with AC caps C21-C28 symmetric), 2 GTH refclk pairs,
   5 sync/sysref LVDS pairs — all P/N complete, polarity maintained
   end-to-end. Source: VITA 57.1; adrv9009_signals.sch; connectors.sch.]

WORKING RULE: ALL 7 ITEMS VERIFIED PASS as of 2026-06-16. Gate is
CLEAR. Next step: Phase 7 footprint assignment (DEC-028/029) before
netlist export. When any of items 1-7 is re-checked, update its status
here with the date and the governing citation.

VERIFICATION DISCIPLINE (applies to this gate and all work):
- Primary sources arbitrate: datasheet / Xilinx UG / Avnet guide /
  VITA 57.1 over cached memory, always.
- On-disk artifact + MD5 is ground truth when narrations disagree.
- Cached component specs have been wrong repeatedly on this project;
  never trust a remembered rating for a boot-critical decision.
- Stop and report findings before acting; per-edit approval.
