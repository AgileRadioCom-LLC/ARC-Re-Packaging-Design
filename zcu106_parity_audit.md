# ZCU106 Feature Parity Audit — UZEV ADRV9009 Carrier

**Date:** 2026-04-29  
**Updated:** 2026-04-29 (DEC-022 — QSPI confirmed PROVIDED_BY_SOM)  
**Basis:** ZCU106 Evaluation Board User Guide (UG1244), AMD public schematics;
Avnet UltraZed-EV Designer's Guide (UGAESZU7EVSOMGV1_2.pdf);
current schematic state (post DEC-019).  
**Purpose:** Master scope definition for remaining carrier design work.  
**Status:** TRIAGED — dispositions locked per DEC-021 UAV datalink mission triage.

---

## Scope note

"Parity" means functional equivalence from the perspective of a developer plugging in an
ADRV9009 FMC card and running firmware. It does not mean identical component count or
identical pinout. Where the FBVB900E package exposes equivalent PS/PL resources, we
implement them. Where the package physically cannot expose the resource, the interface is
deferred forever.

**Disposition key:**

| Code | Meaning |
|------|---------|
| `KEEP` | Already in schematic; no action needed |
| `KEEP-PENDING` | In schematic but incomplete; finish in current phase |
| `ADD_REV1` | Add to carrier schematic before first fab |
| `PROVIDED_BY_SOM` | Requirement satisfied by SOM onboard hardware; no carrier addition required or possible |
| `DEFER_REV2` | Intentionally deferred; revisit for second board revision |
| `NICE_TO_HAVE` | Add if board space and schedule permit; not blocking |
| `DEFER_FOREVER` | Physically impossible on FBVB900E; never implement |

---

## Table 1 — Interfaces ZCU106 has that current schematic IMPLEMENTS

| # | Interface | ZCU106 ref | UZEV carrier implementation | Disposition | Source |
|---|-----------|-----------|----------------------------|-------------|--------|
| 1 | FMC HPC | Sheet 3 (FMC), UG1244 §FMC | J4, Samtec ASP-134602-01, Sheet 1/3; 65 signal pins verified (DEC-001–010) | `KEEP` | INFERRED — ZCU106 schematic FMC section |
| 2 | 12V DC power input | Sheet 1 (Power), UG1244 §Power | J5 barrel jack, power.sch | `KEEP` | INFERRED — ZCU106 schematic power input section |
| 3 | JTAG | Sheet 6 (Prog/JTAG), UG1244 pp.43–45 | J7 6-pin header, Digilent JTAG-HS3 pinout (DEC-015/017) | `KEEP` | INFERRED — ZCU106 schematic JTAG section |
| 4 | UART/console | Sheet 6 (Prog/JTAG), UG1244 pp.52–53 | J6 4-pin 2.54mm header, UART0 TX/RX | `KEEP` | INFERRED — ZCU106 schematic UART section |
| 5 | Power-good / sequencing | Sheet 1 (Power) | SOM_PG_OUT → Buck EN → Buck PG → LDO EN (DEC-019) | `KEEP-PENDING` | INFERRED — ZCU106 power tree topology |
| 6 | MGTAVCC 0.9V | Sheet 1 (Power) | B1 (TPS54320) + L1 (TPS7A85); Phase 5c Rfb pending | `KEEP-PENDING` | INFERRED — ZCU106 MGT supply section |
| 7 | MGTAVTT 1.2V | Sheet 1 (Power) | B2 + L2; Phase 5c Rfb pending | `KEEP-PENDING` | INFERRED |
| 8 | VCCO HP 65 / VADJ 1.8V | Sheet 1 (Power) | B3 + L3, VADJ alias (DEC-013 Q2) | `KEEP-PENDING` | INFERRED |
| 9 | VCCO HP 64 1.8V | Sheet 1 (Power) | B4 + L4; Phase 5c Rfb pending | `KEEP-PENDING` | INFERRED |
| 10 | FMC 3.3V supply | Sheet 1 (Power) | B5 (TPS54531 direct, DEC-019) | `KEEP-PENDING` | INFERRED |
| 11 | Power LED | Sheet 6 (Misc) | D1 GREEN LED, support_io | `KEEP` | INFERRED |
| 12 | Reset pushbutton | Sheet 6 (Misc) | SW1 RESET, support_io | `KEEP` | INFERRED |
| 13 | JESD204B 4 RX + 4 TX | Sheet 3 (FMC) | FMC HPC GTH lanes, Sheet 3, ties done (DEC-005/007) | `KEEP` | INFERRED — ZCU106 FMC/JESD section |
| 14 | ADRV9009 SPI / GPIO | Sheet 3 (FMC) | FMC LA pairs, JX1 HP bank 65; all 45 pairs verified | `KEEP` | INFERRED |

---

## Table 2 — Interfaces ZCU106 has that current schematic DOES NOT implement (gap list)

| # | Interface | ZCU106 ref | Gap description | Disposition | Path to implement | Source |
|---|-----------|-----------|-----------------|-------------|-------------------|--------|
| 1 | QSPI flash boot | Sheet 11 (PS peripherals), UG1244 §Memory | SOM has 256Mb Micron QSPI on PS MIO0–5, not exposed to JX. Standard FSBL/PetaLinux boot source. No carrier addition required or possible. | `PROVIDED_BY_SOM` | No carrier action. See bringup_boot_flow.md for FSBL programming procedure. | INFERRED — ZCU106 sch sheet 11; UG1244 memory section |
| 2 | SD card (PS MIO) | Sheet 11 (PS peripherals), UG1244 §SD | No SD slot; MIO46–51 available on JX3 | `ADD_REV1` | Add micro-SD slot to support_io.sch; DNP option for flight builds; route MIO46–51 from JX3 | INFERRED — ZCU106 sch sheet 11; UG1244 SD section |
| 3 | GbE (PS GEM0) | Sheet 9 (Ethernet), UG1244 pp.28–32 | No PHY or RJ45; GEM0 MDIO/RGMII signals on JX3 PS MIO | `DEFER_REV2` | Add 88E1512 or KSZ9031 PHY + RJ45; route MIO50–77 from JX3 | INFERRED — ZCU106 sch sheet 9 |
| 4 | USB 2.0 OTG (PS USB0) | Sheet 10 (USB), UG1244 pp.34–37 | No USB connector; MIO52–63 available on JX3 | `DEFER_REV2` | Add USB2 Micro-B + TUSB1106 PHY; route MIO52–63 from JX3 | INFERRED — ZCU106 sch sheet 10 |
| 5 | I2C (PS I2C0/1) | Sheet 14 (I2C/PMBus), UG1244 pp.55–58 | No I2C header or devices; MIO10–11 / MIO14–15 on JX3 | `NICE_TO_HAVE` | Add I2C header or board-ID EEPROM on support_io; route from JX3 | INFERRED — ZCU106 sch sheet 14 |
| 6 | MGTVCCAUX PWR_FLAG | Sheet 1 (Power) | Wired as VCCO_HP_65 alias (DEC-013 Q2) but PWR_FLAG missing on connectors.sch | `KEEP-PENDING` | Add PWR_FLAG on connectors.sch in Phase 5c pass | INFERRED |
| 7 | CAN (PS CAN0/1) | Not on ZCU106 base board | MIO available on JX3 | `NICE_TO_HAVE` | Add CAN transceiver (SN65HVD230) + connector | INFERRED |
| 8 | Second GbE (PS GEM1) | Sheet 9 (Ethernet), UG1244 pp.28–32 | Same as GEM0 gap | `DEFER_REV2` | Same path as GEM0 | INFERRED |
| 9 | eMMC (PS MIO) | Sheet 11 (PS peripherals) | MIO available; SOM already has 4GB onboard eMMC | `DEFER_REV2` | Redundant with SOM onboard eMMC; add only if external eMMC needed | INFERRED |
| 10 | Fan / thermal control | Sheet 6 (Misc), UG1244 §Thermal | No fan header | `NICE_TO_HAVE` | Add 4-pin fan header + optional PS GPIO PWM control | INFERRED |
| 11 | PMBus / power monitoring | Sheet 14 (PMBus), UG1244 pp.55–58 | No PMBus or current monitoring | `NICE_TO_HAVE` | Add INA3221 or PMBus header; route I2C from JX3 | INFERRED — ZCU106 sch sheet 14 |
| 12 | PMOD headers | Sheet 6 (PMOD) | No PMOD on carrier | `NICE_TO_HAVE` | Add 2×12 PMOD headers; route spare HP bank 65 pairs from JX1 | INFERRED |

**QSPI note (DEC-022):** SOM has 256Mb Micron QSPI on PS MIO0–5, not exposed to JX.
Standard FSBL/PetaLinux boot source. No carrier addition required or possible.
Disposition confirmed `PROVIDED_BY_SOM`. See `bringup_boot_flow.md` for FSBL/QSPI
programming procedure. If a larger boot flash is ever required, that is an SOM-level change.

---

## Table 3 — Interfaces ZCU106 has that are PHYSICALLY IMPOSSIBLE on UltraZed-EV

| # | Interface | ZCU106 impl | Why impossible on FBVB900E | Missing resource | Disposition |
|---|-----------|-------------|---------------------------|-----------------|-------------|
| 1 | DisplayPort Tx | DP++ (J7) via PS DP block | FBVB900E does not bond out PS DP pins | PS_DP_AUX_OUT, PS_DP_HPD_IN, DP_TX_P/N[0:1] not in FBVB900E | `DEFER_FOREVER` |
| 2 | USB 3.0 SuperSpeed | USB 3.0 Type-A (J2) via PS GTR lane 2 | PS GTR lanes not routed to JX on UltraZed-EV SOM | PS_GTR_TX/RX[2] not on JX | `DEFER_FOREVER` |
| 3 | PCIe Gen2 x4 | PCIe edge connector (J6) | PS GTR lanes not on JX; PL GTH lanes committed to ADRV9009 JESD204B | PS GTR lanes not on JX; GTH quads committed | `DEFER_FOREVER` |
| 4 | SATA | SATA (J33) via PS GTR lane 0 | Same GTR lane exposure issue | PS_GTR_TX/RX[0] not on JX | `DEFER_FOREVER` |
| 5 | HDMI 2.0 Tx/Rx | HDMI Tx (J14), Rx (J15) via GTH | All usable GTH quads committed to ADRV9009; residual 4 lanes marginal and not ZCU106-parity-relevant for radio | GTH quads committed to ADRV9009 | `DEFER_FOREVER` |
| 6 | FMC LPC (second FMC) | FMC LPC (J4), 160-pin | After FMC HPC uses bank 65, insufficient contiguous LA pairs remain | HP IO insufficient for FMC LPC LA[00:33] | `DEFER_FOREVER` |
| 7 | SFP+ ×4 | 4× SFP+ (J1/J8/J23/J24) via GTH | After 8 ADRV9009 JESD lanes, only 4 GTH lanes remain (1 quad); not enough for ×4 SFP+; not required for radio datalink | GTH count insufficient; application doesn't require it | `DEFER_FOREVER` |

---

## Mission-driven disposition summary (DEC-021, 2026-04-29)

**Bring-up path:** JTAG + Vitis. Production flight: autonomous boot from SOM QSPI.

| Interface | Disposition | Rev |
|-----------|-------------|-----|
| JTAG (J7) | `KEEP` | Rev 1 |
| UART (J6) | `KEEP` | Rev 1 |
| QSPI flash boot | `PROVIDED_BY_SOM` — SOM has 256Mb Micron QSPI on PS MIO0–5, not exposed to JX. Standard FSBL/PetaLinux boot source. | Rev 1 |
| SD card slot | `ADD_REV1` — DNP for flight, populated for dev/field update | Rev 1 |
| eMMC | `DEFER_REV2` — SOM onboard sufficient | Rev 2 |
| GbE | `DEFER_REV2` — ground dev only | Rev 2 |
| USB 2.0 OTG | `DEFER_REV2` — ground dev only | Rev 2 |
| I2C | `NICE_TO_HAVE` | Rev 1 if space permits |
| PMBus | `NICE_TO_HAVE` | Rev 1 if space permits |
| DisplayPort | `DEFER_FOREVER` | — |
| SATA | `DEFER_FOREVER` | — |

---

*Updated per DEC-021. Supersedes all earlier informal scope discussion.*
