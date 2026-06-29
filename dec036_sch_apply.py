#!/usr/bin/env python3
"""
DEC-036 Step B: Add TPS25730D + TPS7A1633 USB-C PD circuit to power.sch.
Adds: J5 (USB_C_Receptacle), U6 (TPS25730D), U7 (TPS7A1633), all passives,
wires, labels, junctions, and NoConns.
On success: updates DEC-036 status to APPLIED and closes DEF-13 in DECISIONS_LOG.md.
"""

import hashlib
import os
import re
import sys

SCH_FILE  = "power.sch"
BAK_FILE  = "power.sch.bak.before_dec036"
DEC_LOG   = "DECISIONS_LOG.md"
EXPECTED_MD5 = "7d6ac0765d06dfabdd172d3b7dfa40af"


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def md5sum(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def wire(x1, y1, x2, y2):
    return f"Wire Wire Line\n\t{x1} {y1} {x2} {y2}"

def noconn(x, y):
    return f"NoConn ~ {x} {y}"

def junction(x, y):
    return f"Connection ~ {x} {y}"

def label(x, y, orient, net, size=40):
    """Local net label. orient: 0=right, 2=left."""
    return f"Text Label {x} {y} {orient}    {size}   ~ 0\n{net}"

def gnd_comp(pwr_ref, stamp, px, py):
    return (
        f"$Comp\n"
        f"L power:GND #{pwr_ref}\n"
        f"U 1 1 {stamp}\n"
        f"P {px} {py}\n"
        f"F 0 \"#{pwr_ref}\" H {px} {py+50} 50  0001 C CNN\n"
        f"F 1 \"GND\" H {px} {py+150} 50  0000 C CNN\n"
        f"F 2 \"\" H {px} {py} 50  0001 C CNN\n"
        f"F 3 \"\" H {px} {py} 50  0001 C CNN\n"
        f"\t1    {px} {py}\n"
        f"\t1    0    0    -1  \n"
        f"$EndComp"
    )

def res_comp(ref, stamp, px, py, value):
    fp = "Resistor_SMD:R_0402_1005Metric"
    return (
        f"$Comp\n"
        f"L Device:R {ref}\n"
        f"U 1 1 {stamp}\n"
        f"P {px} {py}\n"
        f"F 0 \"{ref}\" H {px+50} {py-150} 50  0000 L CNN\n"
        f"F 1 \"{value}\" H {px+50} {py} 50  0000 L CNN\n"
        f"F 2 \"{fp}\" H {px} {py} 50  0001 C CNN\n"
        f"F 3 \"~\" H {px} {py} 50  0001 C CNN\n"
        f"\t1    {px} {py}\n"
        f"\t1    0    0    -1  \n"
        f"$EndComp"
    )

def cap_comp(ref, stamp, px, py, value, fp="Capacitor_SMD:C_0402_1005Metric"):
    return (
        f"$Comp\n"
        f"L Device:C {ref}\n"
        f"U 1 1 {stamp}\n"
        f"P {px} {py}\n"
        f"F 0 \"{ref}\" H {px+50} {py-100} 50  0000 L CNN\n"
        f"F 1 \"{value}\" H {px+50} {py+100} 50  0000 L CNN\n"
        f"F 2 \"{fp}\" H {px} {py} 50  0001 C CNN\n"
        f"F 3 \"\" H {px} {py} 50  0001 C CNN\n"
        f"\t1    {px} {py}\n"
        f"\t1    0    0    -1  \n"
        f"$EndComp"
    )


# ---------------------------------------------------------------------------
# Schematic elements
# All placements use standard transform: sch_x = Px + lx, sch_y = Py - ly
# ---------------------------------------------------------------------------

def build_elements():
    elems = []

    # -----------------------------------------------------------------------
    # J5: USB_C_Receptacle at P=(800,650)
    # VBUS(1): (350,500), GND(2): (350,650), CC1(3): (350,750), CC2(4): (350,850)
    # -----------------------------------------------------------------------
    elems.append(
        "$Comp\n"
        "L UZEV_Connectors:USB_C_Receptacle J5\n"
        "U 1 1 6C00009F\n"
        "P 800 650\n"
        "F 0 \"J5\" H 800 350 50  0000 C CNN\n"
        "F 1 \"USB_C_Receptacle\" H 800 950 50  0000 C CNN\n"
        "F 2 \"\" H 800 650 50  0001 C CNN\n"
        "F 3 \"~\" H 800 650 50  0001 C CNN\n"
        "\t1    800  650\n"
        "\t1    0    0    -1  \n"
        "$EndComp"
    )
    # J5 VBUS -> label
    elems.append(wire(350, 500, 200, 500))
    elems.append(label(200, 500, 0, "VBUS"))
    # J5 GND
    elems.append(gnd_comp("PWR062", "6C0000C0", 350, 650))
    # J5 CC1 -> label
    elems.append(wire(350, 750, 200, 750))
    elems.append(label(200, 750, 0, "CC1"))
    # J5 CC2 -> label
    elems.append(wire(350, 850, 200, 850))
    elems.append(label(200, 850, 0, "CC2"))

    # -----------------------------------------------------------------------
    # VBUS bulk decoupling caps (near J5 area, labelled VBUS)
    # C65: 47uF at P=(2200,1300), C66: 100nF at P=(2400,1300)
    # pin1=Py-100 (VBUS), pin2=Py+100 (GND)
    # -----------------------------------------------------------------------
    elems.append(cap_comp("C65", "6C0000A7", 2200, 1300, "47uF",
                           "Capacitor_SMD:C_1210_3225Metric"))
    elems.append(label(2200, 1200, 0, "VBUS"))
    elems.append(gnd_comp("PWR076", "6C0000C1", 2200, 1400))

    elems.append(cap_comp("C66", "6C0000A8", 2400, 1300, "100nF"))
    elems.append(label(2400, 1200, 0, "VBUS"))
    elems.append(gnd_comp("PWR077", "6C0000C2", 2400, 1400))

    # -----------------------------------------------------------------------
    # U7: TPS7A1633 at P=(800,2000)
    # IN(1): (300,1800), EN(3): (300,1900), DNC(4): (300,2000)
    # DELAY(5): (300,2100), GND(2): (800,2500), GND_EP(9): (800,2700)
    # PG(6): (1300,2100), OUT(7): (1300,1800), OUT(8): (1300,1900)
    # -----------------------------------------------------------------------
    elems.append(
        "$Comp\n"
        "L UZEV_Connectors:TPS7A1633 U7\n"
        "U 1 1 6C0000A0\n"
        "P 800 2000\n"
        "F 0 \"U7\" H 850 1700 50  0000 L CNN\n"
        "F 1 \"TPS7A1633\" H 850 2300 50  0000 L CNN\n"
        "F 2 \"\" H 800 2000 50  0001 C CNN\n"
        "F 3 \"~\" H 800 2000 50  0001 C CNN\n"
        "\t1    800  2000\n"
        "\t1    0    0    -1  \n"
        "$EndComp"
    )

    # VBUS horizontal bus at y=1800: x=100..300 (covers IN stub)
    # IN pin at (300,1800), EN pin at (300,1900)
    # Text Label "VBUS" at left end
    elems.append(wire(100, 1800, 300, 1800))
    elems.append(label(100, 1800, 0, "VBUS"))
    # EN wire up to IN (both on VBUS)
    elems.append(wire(300, 1900, 300, 1800))
    elems.append(junction(300, 1800))   # IN pin + EN stub + VBUS bus endpoint

    # IN bypass cap C60: 10uF, P=(200,1950), pin1=1850 (VBUS), pin2=2050 (GND)
    elems.append(cap_comp("C60", "6C0000A2", 200, 1950, "10uF",
                           "Capacitor_SMD:C_0805_2012Metric"))
    elems.append(wire(200, 1850, 200, 1800))
    elems.append(junction(200, 1800))   # cap stub + VBUS bus T-junction
    elems.append(gnd_comp("PWR063", "6C0000C3", 200, 2050))

    # DNC -> NoConn
    elems.append(noconn(300, 2000))

    # DELAY -> 100nF cap to GND
    # Cap C61: P=(300,2350), pin1=2250 (DELAY side), pin2=2450 (GND)
    elems.append(wire(300, 2100, 300, 2250))
    elems.append(cap_comp("C61", "6C0000A3", 300, 2350, "100nF"))
    elems.append(gnd_comp("PWR064", "6C0000C4", 300, 2450))

    # GND and GND_EP
    elems.append(gnd_comp("PWR065", "6C0000C5", 800, 2500))
    elems.append(gnd_comp("PWR066", "6C0000C6", 800, 2700))

    # PG -> NoConn
    elems.append(noconn(1300, 2100))

    # OUT(7) and OUT(8): wire together, extend to label, add OUT cap
    # OUT7=(1300,1800), OUT8=(1300,1900)
    elems.append(wire(1300, 1900, 1300, 1800))   # join OUT8 to OUT7
    elems.append(wire(1300, 1800, 1500, 1800))   # extend right to label
    elems.append(junction(1300, 1800))            # OUT7 pin + OUT8 stub + label wire
    elems.append(label(1500, 1800, 0, "VIN_3V3"))

    # OUT bypass cap C62: 10uF, P=(1500,1950), pin1=1850 (VIN_3V3), pin2=2050 (GND)
    elems.append(cap_comp("C62", "6C0000A4", 1500, 1950, "10uF",
                           "Capacitor_SMD:C_0805_2012Metric"))
    elems.append(wire(1500, 1850, 1500, 1800))
    elems.append(junction(1500, 1800))  # label conn + OUT wire endpoint + cap stub
    elems.append(gnd_comp("PWR067", "6C0000C7", 1500, 2050))

    # -----------------------------------------------------------------------
    # U6: TPS25730D at P=(1900,4000)
    # Body: x=1300-2500, y=3000-5000
    # Left pins at x=1100, right at x=2700, bottom at y=5200, top at y=2800
    # -----------------------------------------------------------------------
    elems.append(
        "$Comp\n"
        "L UZEV_Connectors:TPS25730D U6\n"
        "U 1 1 6C0000A1\n"
        "P 1900 4000\n"
        "F 0 \"U6\" H 1950 2850 50  0000 L CNN\n"
        "F 1 \"TPS25730D\" H 1950 5100 50  0000 L CNN\n"
        "F 2 \"\" H 1900 4000 50  0001 C CNN\n"
        "F 3 \"~\" H 1900 4000 50  0001 C CNN\n"
        "\t1    1900 4000\n"
        "\t1    0    0    -1  \n"
        "$EndComp"
    )

    # --- U6 left side wiring ---

    # VIN_3V3 pin (1100,3100) -> label
    elems.append(wire(1100, 3100, 950, 3100))
    elems.append(label(950, 3100, 0, "VIN_3V3"))

    # CC1 (1100,3200) -> label + 330pF cap to GND
    elems.append(wire(1100, 3200, 900, 3200))
    elems.append(label(900, 3200, 0, "CC1"))
    # C63: 330pF cap, P=(1000,3050), pin1=2950 (CC1 net), pin2=3150 (GND)
    elems.append(cap_comp("C63", "6C0000A5", 1000, 3050, "330pF"))
    elems.append(label(1000, 2950, 0, "CC1"))
    elems.append(gnd_comp("PWR068", "6C0000C8", 1000, 3150))

    # CC2 (1100,3300) -> label + 330pF cap to GND
    elems.append(wire(1100, 3300, 900, 3300))
    elems.append(label(900, 3300, 0, "CC2"))
    # C64: 330pF cap, P=(1000,3350), pin1=3250 (CC2 net), pin2=3450 (GND)
    elems.append(cap_comp("C64", "6C0000A6", 1000, 3350, "330pF"))
    elems.append(label(1000, 3250, 0, "CC2"))
    elems.append(gnd_comp("PWR069", "6C0000C9", 1000, 3450))

    # ADCIN1 (1100,3400): divider 91k up / 11k down from LDO_3V3
    # R40 (91k): P=(700,3250), pin1=(700,3100)[LDO_3V3], pin2=(700,3400)[mid]
    # R41 (11k): P=(700,3550), pin1=(700,3400)[mid],    pin2=(700,3700)[GND]
    elems.append(res_comp("R40", "6C0000AA", 700, 3250, "91k"))
    elems.append(label(700, 3100, 0, "LDO_3V3"))
    elems.append(res_comp("R41", "6C0000AB", 700, 3550, "11k"))
    elems.append(gnd_comp("PWR073", "6C0000CA", 700, 3700))
    elems.append(wire(700, 3400, 1100, 3400))   # mid-node to ADCIN1
    elems.append(junction(700, 3400))            # R40 pin2 + R41 pin1 + wire

    # ADCIN2 (1100,3500): direct to LDO_1V5
    elems.append(wire(1100, 3500, 950, 3500))
    elems.append(label(950, 3500, 0, "LDO_1V5"))

    # ADCIN3 (1100,3600): divider 82k up / 20k down from LDO_3V3
    # R42 (82k): P=(500,3450), pin1=(500,3300)[LDO_3V3], pin2=(500,3600)[mid]
    # R43 (20k): P=(500,3750), pin1=(500,3600)[mid],     pin2=(500,3900)[GND]
    elems.append(res_comp("R42", "6C0000AC", 500, 3450, "82k"))
    elems.append(label(500, 3300, 0, "LDO_3V3"))
    elems.append(res_comp("R43", "6C0000AD", 500, 3750, "20k"))
    elems.append(gnd_comp("PWR074", "6C0000CB", 500, 3900))
    elems.append(wire(500, 3600, 1100, 3600))   # mid-node to ADCIN3
    elems.append(junction(500, 3600))

    # ADCIN4 (1100,3700): divider 100k up / 4.7k down from LDO_3V3
    # R44 (100k): P=(300,3550), pin1=(300,3400)[LDO_3V3], pin2=(300,3700)[mid]
    # R45 (4.7k): P=(300,3850), pin1=(300,3700)[mid],     pin2=(300,4000)[GND]
    elems.append(res_comp("R44", "6C0000AE", 300, 3550, "100k"))
    elems.append(label(300, 3400, 0, "LDO_3V3"))
    elems.append(res_comp("R45", "6C0000AF", 300, 3850, "4.7k"))
    elems.append(gnd_comp("PWR075", "6C0000CC", 300, 4000))
    elems.append(wire(300, 3700, 1100, 3700))   # mid-node to ADCIN4
    elems.append(junction(300, 3700))

    # LDO_3V3 pin (1100,3800) -> label
    elems.append(wire(1100, 3800, 950, 3800))
    elems.append(label(950, 3800, 0, "LDO_3V3"))

    # LDO_1V5 pin (1100,3900) -> label
    elems.append(wire(1100, 3900, 950, 3900))
    elems.append(label(950, 3900, 0, "LDO_1V5"))

    # FAULT_IN (1100,4000) -> 10k pullup to LDO_3V3
    # R49: P=(850,3850), pin1=(850,3700)[LDO_3V3], pin2=(850,4000)[FAULT_IN]
    elems.append(res_comp("R49", "6C0000B3", 850, 3850, "10k"))
    elems.append(label(850, 3700, 0, "LDO_3V3"))
    elems.append(wire(850, 4000, 1100, 4000))

    # I2Ct_SCL (1100,4100), I2Ct_SDA (1100,4200), CAP_MIS (1100,4300), DBG_ACC (1100,4400) -> NoConn
    elems.append(noconn(1100, 4100))
    elems.append(noconn(1100, 4200))
    elems.append(noconn(1100, 4300))
    elems.append(noconn(1100, 4400))

    # --- U6 right side wiring ---

    # VBUS bus: vertical at x=2850, y=3100..3650, stubs from x=2700 pins
    # VBUS_IN_A(2700,3100), VBUS_IN_B(2700,3200), VBUS_IN_C(2700,3300)
    # PPHV_A(2700,3450), PPHV_B(2700,3550), PPHV_C(2700,3650)
    elems.append(wire(2850, 3100, 2850, 3650))  # vertical VBUS bus
    elems.append(wire(2700, 3100, 2850, 3100))  # VBUS_IN_A stub (bus start)
    elems.append(wire(2700, 3200, 2850, 3200))  # VBUS_IN_B
    elems.append(junction(2850, 3200))
    elems.append(wire(2700, 3300, 2850, 3300))  # VBUS_IN_C
    elems.append(junction(2850, 3300))
    elems.append(wire(2700, 3450, 2850, 3450))  # PPHV_A
    elems.append(junction(2850, 3450))
    elems.append(wire(2700, 3550, 2850, 3550))  # PPHV_B
    elems.append(junction(2850, 3550))
    elems.append(wire(2700, 3650, 2850, 3650))  # PPHV_C (bus end)
    # VBUS label at top of bus
    # Junction at (2850,3100): vertical bus start + VBUS_IN_A stub + extension wire
    elems.append(junction(2850, 3100))
    elems.append(wire(2850, 3100, 2950, 3100))
    elems.append(label(2950, 3100, 0, "VBUS"))

    # DRAIN_A (2700,3800) and DRAIN_B (2700,3900) -> VIN bus at (2800,2900)
    # Route: stubs to x=2800, merge at (2800,3800), then up to (2800,3100)
    # which joins the existing C4 pin1 / VIN stub at (2800,3100)
    elems.append(wire(2700, 3800, 2800, 3800))   # DRAIN_A horizontal
    elems.append(wire(2700, 3900, 2800, 3900))   # DRAIN_B horizontal
    elems.append(wire(2800, 3900, 2800, 3800))   # merge DRAIN_B to DRAIN_A level
    elems.append(junction(2800, 3800))            # DRAIN_A + DRAIN_B merge + up wire
    elems.append(wire(2800, 3800, 2800, 3100))   # up to existing C4/VIN junction
    elems.append(junction(2800, 3100))            # C4 pin1 + existing VIN wire + DRAIN wire

    # SINK_EN, PLUG_EVENT, PLUG_FLIP -> NoConn
    elems.append(noconn(2700, 4000))
    elems.append(noconn(2700, 4100))
    elems.append(noconn(2700, 4200))

    # --- U6 top pins ---
    # VBUS_33 (1900,2800): wire up, VBUS label
    elems.append(wire(1900, 2800, 1900, 2650))
    elems.append(label(1900, 2650, 0, "VBUS"))

    # RSV_26 (2000,2800): 10k to GND (resistor above pin, GND at top)
    # R46: P=(2000,2600), pin1=(2000,2450)[GND], pin2=(2000,2750)
    elems.append(res_comp("R46", "6C0000B0", 2000, 2600, "10k"))
    elems.append(gnd_comp("PWR070", "6C0000CD", 2000, 2450))
    elems.append(wire(2000, 2800, 2000, 2750))

    # RSV_27 (2100,2800): 10k to GND
    # R47: P=(2100,2600), pin1=(2100,2450)[GND], pin2=(2100,2750)
    elems.append(res_comp("R47", "6C0000B1", 2100, 2600, "10k"))
    elems.append(gnd_comp("PWR071", "6C0000CE", 2100, 2450))
    elems.append(wire(2100, 2800, 2100, 2750))

    # RSV_36 (2200,2800): 10k to GND
    # R48: P=(2200,2600), pin1=(2200,2450)[GND], pin2=(2200,2750)
    elems.append(res_comp("R48", "6C0000B2", 2200, 2600, "10k"))
    elems.append(gnd_comp("PWR072", "6C0000CF", 2200, 2450))
    elems.append(wire(2200, 2800, 2200, 2750))

    # --- U6 bottom pins ---
    # DRAIN_EP (1700,5200): Text Label "VIN" (same net as GLabel VIN on this sheet)
    elems.append(label(1700, 5200, 0, "VIN"))

    # VBUS_32 (1800,5200): Text Label "VBUS"
    elems.append(label(1800, 5200, 0, "VBUS"))

    # GND bottom pins: GND_34..GND_31 (9 pins)
    gnd_bottom = [
        ("PWR079", "6C0000D0", 1400, 5200),  # GND_34
        ("PWR080", "6C0000D1", 1500, 5200),  # GND_35
        ("PWR081", "6C0000D2", 1600, 5200),  # GND_EP
        ("PWR082", "6C0000D3", 1900, 5200),  # GND_11
        ("PWR083", "6C0000D4", 2000, 5200),  # GND_12
        ("PWR084", "6C0000D5", 2100, 5200),  # GND_14
        ("PWR085", "6C0000D6", 2200, 5200),  # GND_16
        ("PWR086", "6C0000D7", 2300, 5200),  # GND_17
        ("PWR087", "6C0000D8", 2400, 5200),  # GND_31
    ]
    for pwr_ref, stamp, px, py in gnd_bottom:
        elems.append(gnd_comp(pwr_ref, stamp, px, py))

    # --- VIN_3V3 bypass cap ---
    # C67: 100nF, P=(1200,2900), pin1=2800 (VIN_3V3), pin2=3000 (GND)
    elems.append(cap_comp("C67", "6C0000A9", 1200, 2900, "100nF"))
    elems.append(label(1200, 2800, 0, "VIN_3V3"))
    elems.append(gnd_comp("PWR078", "6C0000D9", 1200, 3000))

    return elems


# ---------------------------------------------------------------------------
# Post-write verification checks
# ---------------------------------------------------------------------------

def verify(content):
    errors = []

    # Must contain J5, U6, U7 component blocks
    for ref in ["J5", "U6", "U7"]:
        if f"L UZEV_Connectors:" not in content:
            errors.append(f"Missing UZEV_Connectors components")
            break
    for ref in [" J5\n", " U6\n", " U7\n"]:
        if ref not in content:
            errors.append(f"Missing component ref:{ref.strip()}")

    # Must NOT contain old HUSB238
    if "HUSB238" in content:
        errors.append("HUSB238 still present — remove script may not have run")

    # Must end with $EndSCHEMATC
    if not content.rstrip().endswith("$EndSCHEMATC"):
        errors.append("File does not end with $EndSCHEMATC")

    # VIN label (DRAIN_EP connection)
    if content.count("VIN\n") < 2:
        errors.append("Expected >= 2 'VIN' net labels (GLabel + DRAIN_EP Label)")

    # Key net labels present
    for net in ["VBUS\n", "VIN_3V3\n", "LDO_3V3\n", "LDO_1V5\n", "CC1\n", "CC2\n"]:
        if net not in content:
            errors.append(f"Missing net label: {net.strip()}")

    # DRAIN wires to VIN bus
    if "2800 3800" not in content:
        errors.append("Missing DRAIN merge point at (2800,3800)")
    if "2800 3100" not in content:
        errors.append("Missing VIN junction at (2800,3100)")

    return errors


# ---------------------------------------------------------------------------
# DECISIONS_LOG.md update
# ---------------------------------------------------------------------------

def update_decisions_log():
    with open(DEC_LOG, "r", encoding="utf-8") as f:
        log = f.read()

    # DEC-036: change PARTIALLY APPLIED -> APPLIED
    old = "**Status:** PARTIALLY APPLIED"
    new = "**Status:** APPLIED"
    if old not in log:
        return False, "DEC-036 PARTIALLY APPLIED marker not found in log"
    log = log.replace(old, new, 1)

    # DEF-13: change OPEN -> CLOSED
    old_def = "**Status:** OPEN — blocked on `dec036_sch_apply.py` execution."
    new_def = "**Status:** CLOSED — dec036_sch_apply.py executed successfully 2026-06-08."
    if old_def not in log:
        return False, "DEF-13 OPEN marker not found in log"
    log = log.replace(old_def, new_def, 1)

    tmp = DEC_LOG + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(log)
    os.replace(tmp, DEC_LOG)
    return True, "OK"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Pre-flight checks
    actual_md5 = md5sum(SCH_FILE)
    if actual_md5 != EXPECTED_MD5:
        print(f"ABORT: MD5 mismatch. Expected {EXPECTED_MD5}, got {actual_md5}")
        print("File has been modified since this script was written. Do not proceed.")
        sys.exit(1)
    print(f"MD5 verified: {actual_md5}")

    # Backup
    with open(SCH_FILE, "rb") as f:
        sch_bytes = f.read()
    with open(BAK_FILE, "wb") as f:
        f.write(sch_bytes)
    print(f"Backup written: {BAK_FILE}")

    # Read current content
    content = sch_bytes.decode("utf-8")

    # Build new elements
    elements = build_elements()
    insertion = "\n".join(elements) + "\n"

    # Insert before $EndSCHEMATC
    marker = "$EndSCHEMATC"
    if marker not in content:
        print("ABORT: $EndSCHEMATC not found in schematic")
        sys.exit(1)
    new_content = content.replace(marker, insertion + marker, 1)

    # Verify
    errors = verify(new_content)
    if errors:
        print("ABORT: Post-write verification failed:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("Verification passed.")

    # Atomic write
    tmp = SCH_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(new_content)
    os.replace(tmp, SCH_FILE)

    new_md5 = md5sum(SCH_FILE)
    print(f"Schematic written. New MD5: {new_md5}")

    # Update DECISIONS_LOG
    ok, msg = update_decisions_log()
    if not ok:
        print(f"WARNING: DECISIONS_LOG update failed: {msg}")
        print("Schematic write succeeded. Update log manually.")
    else:
        print("DECISIONS_LOG updated: DEC-036 -> APPLIED, DEF-13 -> CLOSED.")

    print("dec036_sch_apply.py complete.")


if __name__ == "__main__":
    main()
