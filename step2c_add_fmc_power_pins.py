#!/usr/bin/env python3
"""step2c: rename 29 FMC_HPC_ADRV9009 pins per ANSI/VITA 57.1-2008 Table 2."""
import re, shutil, sys, subprocess
from datetime import datetime

LIB = "/home/arc/projects/uzev_carrier_v5/UZEV_Connectors.lib"
SYMBOL = "FMC_HPC_ADRV9009"

RENAMES = {
    "K1":  "VREF_B_M2C", "H1":  "VREF_A_M2C", "F1":  "PG_M2C",
    "D1":  "PG_C2M",     "B1":  "RES1",       "H2":  "PRSNT_M2C_L",
    "D29": "TCK",        "D30": "TDI",        "C30": "SCL",
    "D31": "TDO",        "C31": "SDA",        "D32": "3P3VAUX",
    "D33": "TMS",        "D34": "TRST_L",     "C34": "GA0",
    "D35": "GA1",        "C35": "12P0V",      "D36": "3P3V",
    "C37": "12P0V",      "D38": "3P3V",       "J39": "VIO_B_M2C",
    "G39": "VADJ",       "E39": "VADJ",       "C39": "3P3V",
    "K40": "VIO_B_M2C",  "H40": "VADJ",       "F40": "VADJ",
    "D40": "3P3V",       "B40": "RES0",
}
assert len(RENAMES) == 29

def main():
    with open(LIB) as f:
        lines = f.readlines()
    def_start = def_end = None
    for i, line in enumerate(lines):
        if line.startswith(f"DEF {SYMBOL} "):
            def_start = i
        elif def_start is not None and line.startswith("ENDDEF"):
            def_end = i
            break
    if def_start is None or def_end is None:
        sys.exit(f"ERROR: Could not find DEF/ENDDEF for {SYMBOL}")
    print(f"Found {SYMBOL} at lines {def_start+1}-{def_end+1}")
    total_before = sum(1 for l in lines[def_start:def_end+1] if l.startswith("X "))
    print(f"Total pins before: {total_before}")

    placeholder_re = re.compile(r"^Pin_\d+$")
    found = {}
    for i in range(def_start, def_end + 1):
        if not lines[i].startswith("X "):
            continue
        parts = lines[i].split()
        if len(parts) < 10:
            continue
        pin_name, pin_num = parts[1], parts[2]
        if pin_num in RENAMES:
            if pin_num in found:
                sys.exit(f"ERROR: Duplicate pin number {pin_num} line {i+1}")
            if not placeholder_re.match(pin_name):
                sys.exit(f"ERROR: Pin {pin_num} line {i+1} already named '{pin_name}'")
            found[pin_num] = i
    missing = set(RENAMES.keys()) - set(found.keys())
    if missing:
        sys.exit(f"ERROR: Target pins not found: {sorted(missing)}")
    print("Pre-flight OK: all 29 target pins in placeholder state")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = f"{LIB}.bak.before_dec003.{ts}"
    shutil.copy2(LIB, backup)
    print(f"Backup: {backup}")

    changes = []
    for pin_num, new_name in RENAMES.items():
        i = found[pin_num]
        parts = lines[i].split()
        old_name = parts[1]
        parts[1] = new_name
        lines[i] = " ".join(parts) + "\n"
        changes.append((pin_num, old_name, new_name))
    with open(LIB, "w") as f:
        f.writelines(lines)

    with open(LIB) as f:
        new_lines = f.readlines()
    ns = ne = None
    for i, line in enumerate(new_lines):
        if line.startswith(f"DEF {SYMBOL} "):
            ns = i
        elif ns is not None and line.startswith("ENDDEF"):
            ne = i
            break
    total_after = sum(1 for l in new_lines[ns:ne+1] if l.startswith("X "))
    if total_after != total_before:
        sys.exit(f"ERROR: Pin count {total_before} -> {total_after}")
    print(f"Total pins after: {total_after} (unchanged)")

    verified = 0
    for i in range(ns, ne + 1):
        if not new_lines[i].startswith("X "):
            continue
        parts = new_lines[i].split()
        if len(parts) < 10:
            continue
        pin_name, pin_num = parts[1], parts[2]
        if pin_num in RENAMES:
            if pin_name != RENAMES[pin_num]:
                sys.exit(f"ERROR: {pin_num} should be {RENAMES[pin_num]} not {pin_name}")
            verified += 1
    if verified != 29:
        sys.exit(f"ERROR: Verified only {verified}/29")
    print("Post-flight OK: all 29 renames verified")

    print("\nChanges applied:")
    for pin_num, old, new in sorted(changes):
        print(f"  {pin_num:4s} {old:12s} -> {new}")

    print("\nDiff:")
    r = subprocess.run(["diff", "-u", backup, LIB], capture_output=True, text=True)
    print(r.stdout)
    print("SUCCESS: V2 rename complete.")

if __name__ == "__main__":
    main()
