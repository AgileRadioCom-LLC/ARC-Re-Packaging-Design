# UZEV Carrier — Pending Task Checklist

**As of:** post-DEC-036 session resume
**Schematic:** ERC clean (4 cosmetic warnings, 0 errors), DEF-11/12 closed
**PCB:** `uzev_adrv9009_carrier.kicad_pcb` exists (May 26), stale by 3 days vs power.sch

---

## Immediate — Unblock PCB Layout (forced sequence, do in order)

- [x] **T1.** Verify NC intent for J1-B36, J1-B37, J4-H31, J4-H32 against Avnet Designer's Guide + pin mapping spreadsheet + VITA 57.1
- [x] **T2.** Add `no_connect` flags to those 4 pins in `connectors.sch` (only after T1 confirms NC-by-design)
- [ ] **T3.** Re-run ERC — confirm 0/0
- [x] **T4.** Log DEC-037 — NC flag additions, with citation to NC-by-design source
- [ ] **T5.** Export netlist from clean schematic
- [ ] **T6.** Update PCB from netlist — pulls TPS25730D + TPS7A1633 footprints into layout
- [ ] **T7.** Verify footprint assignments for all DEC-036 new parts (TPS25730D, TPS7A1633, any bootstrap caps/resistors added)

---

## Pre-Layout Architectural Decisions (must close before copper)

- [ ] **T8.** Resolve stackup conflict — memory says 8-layer FR-4, fab brief says 12-layer. Log DEC-038 with final choice.
- [ ] **T9.** Controlled impedance targets logged per layer pair (50Ω SE, 100Ω diff, 85Ω USB if applicable)
- [ ] **T10.** Confirm board outline still locked at 101.6 x 152.4 x 1.6 mm per DEC-034
- [ ] **T11.** Component placement strategy doc — SOM keepout, FMC daughter card envelope, RF/digital separation, regulator thermal zones

---

## PCB Layout Phase (after T1-T11 closed)

- [ ] **T12.** Mechanical — board outline, mounting holes, SOM keepout, FMC HPC daughter envelope, casing clearance per 33.2 mm assembly stack
- [ ] **T13.** Placement — SOM connectors (JX1/JX2/JX3 SEARAY), FMC HPC, ADRV9009 carrier region, power tree, USB-C, JTAG, SD card
- [ ] **T14.** Power plane partitioning — define plane shapes per rail, place stitching vias
- [ ] **T15.** SEARAY 0.8 mm pitch breakout — fanout strategy, via-in-pad if needed
- [ ] **T16.** GT stripline routing — MGTAVCC/MGTAVTT rail routing, GT pair length matching
- [ ] **T17.** JESD204B differential pair routing — controlled impedance, matched length, reference plane continuity
- [ ] **T18.** Power tree routing — buck input/output, LDO traces, sense lines per DEC-036 part choices
- [ ] **T19.** USB-C PD routing — TPS25730D, VBUS current path sizing for PD power level
- [ ] **T20.** SI critical signals — clocks, JTAG, I2C, GPIO
- [ ] **T21.** Decoupling cap placement per SOM and ADRV9009 requirements
- [ ] **T22.** Test points — power rails, key signals, JTAG
- [ ] **T23.** DRC clean — 0 errors before fab handoff
- [ ] **T24.** TDR coupons added per fabricator brief

---

## Parallel / External-Dependency Tasks

- [ ] **T25.** ITAR determination — blocks final CM vendor selection (Presco vs. MacroFab/Sierra). Not a layout blocker, but blocks fab quote.
- [ ] **T26.** NDA execution with chosen fabricator before sharing classified end-use specifics
- [ ] **T27.** Fab brief update — reconcile 12-layer brief vs T8 outcome; update IPC-6012 Class 3, ENIG, via-in-pad, back-drilling, controlled impedance, TDR coupon specs

---

## ZCU106 Parity Gap — Documented Deferrals (no action this rev)

- Deferred to Rev 2: GbE, USB host
- Permanently deferred: DisplayPort, SATA
- Confirmed not needed on carrier: QSPI (SOM-provided)
- Included this rev: SD card slot (DEC-021/022)

---

## Risk Watch (active monitoring, not action items)

- DEC-036 reverse-validation: confirm TPS25730D + TPS7A1633 cover all six SOM rails (1.5/1.8/2.0/3 A). If DEC-036 only addressed USB-C PD path and not the full SOM power tree, **DEF-11 may not be fully closed** despite the log entry.
- External AI audit findings standing protocol: any new audit results require adversarial review before action.
- Primary-source-wins protocol holds for any new part selection.

---

**Critical-path next action:** T1 (diagnostic running below). Everything else is gated on it.
