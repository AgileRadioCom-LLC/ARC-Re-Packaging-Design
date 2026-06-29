#!/usr/bin/env python3
"""
DEC-037 patch: connectors.sch
  - Remove spurious FMC_H31_LA28_P / FMC_H32_LA28_N wire+label blocks
    from both J4 (H31/H32) and J1 (B36/B37)
  - Add NoConn flags at the four freed pin endpoints
Rationale: HP_DP_38 (JX1.B36/B37) is spare per PROPOSED MAPPING; LA28 is
#N/A on ADRV9009 FMC card per FMC Signals spreadsheet. The May-25 schematic
edit incorrectly joined two independent spare resources. Removing the nets
and adding NC flags is the correct fix.
"""
import os, sys, shutil, hashlib
from datetime import datetime

SCH = "connectors.sch"
BAK = f"connectors.sch.bak.before_dec037"

# ── Exact 4-line blocks to remove ────────────────────────────────────────────
# Each block: "Wire Wire Line\n\t<coords>\nText GLabel ...\n<label>\n"
# Use \n as separator; blocks in the file are separated from neighbours by \n.

REMOVE_BLOCKS = [
    # J4 side — H31
    (
        "Wire Wire Line\n"
        "\t23900 21000 23700 21000\n"
        "Text GLabel 23700 21000 2    50   BiDi ~ 0\n"
        "FMC_H31_LA28_P\n"
    ),
    # J4 side — H32
    (
        "Wire Wire Line\n"
        "\t23900 21100 23700 21100\n"
        "Text GLabel 23700 21100 2    50   BiDi ~ 0\n"
        "FMC_H32_LA28_N\n"
    ),
    # J1 side — B37 (was labelled H31_LA28_P)
    (
        "Wire Wire Line\n"
        "\t6400 7050 6600 7050\n"
        "Text GLabel 6600 7050 0    50   BiDi ~ 0\n"
        "FMC_H31_LA28_P\n"
    ),
    # J1 side — B36 (was labelled H32_LA28_N)
    (
        "Wire Wire Line\n"
        "\t5600 7150 5400 7150\n"
        "Text GLabel 5400 7150 2    50   BiDi ~ 0\n"
        "FMC_H32_LA28_N\n"
    ),
]

# ── NoConn flags to insert (placed before $EndSCHEMATC) ──────────────────────
NEW_NOCONNS = (
    "NoConn ~ 23900 21000\n"   # J4-H31
    "NoConn ~ 23900 21100\n"   # J4-H32
    "NoConn ~ 6400 7050\n"     # J1-B37
    "NoConn ~ 5600 7150\n"     # J1-B36
)

# ── Read ──────────────────────────────────────────────────────────────────────
with open(SCH, "r", encoding="utf-8") as f:
    original = f.read()

md5_before = hashlib.md5(original.encode()).hexdigest()
size_before = len(original)
print(f"Input : {SCH}  size={size_before}  md5={md5_before}")

# ── Verify all blocks are present exactly once ────────────────────────────────
errors = []
for i, blk in enumerate(REMOVE_BLOCKS):
    count = original.count(blk)
    if count != 1:
        errors.append(f"Block {i+1} found {count}× (expected 1):\n  {repr(blk[:60])}")
if errors:
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)

if "$EndSCHEMATC" not in original:
    print("ERROR: $EndSCHEMATC sentinel not found", file=sys.stderr)
    sys.exit(1)

# ── Backup ────────────────────────────────────────────────────────────────────
if os.path.exists(BAK):
    print(f"Backup already exists: {BAK} — skipping overwrite")
else:
    shutil.copy2(SCH, BAK)
    print(f"Backup : {BAK}")

# ── Apply removals ────────────────────────────────────────────────────────────
patched = original
for blk in REMOVE_BLOCKS:
    patched = patched.replace(blk, "", 1)

removed_lines = (original.count("\n") - patched.count("\n"))
print(f"Removed: {len(REMOVE_BLOCKS)} blocks ({removed_lines} lines)")

# ── Verify the four net labels are fully gone ─────────────────────────────────
for label in ("FMC_H31_LA28_P", "FMC_H32_LA28_N"):
    remaining = patched.count(label)
    if remaining:
        print(f"ERROR: '{label}' still appears {remaining}× after removal",
              file=sys.stderr)
        sys.exit(1)
print("Verified: FMC_H31_LA28_P and FMC_H32_LA28_N fully removed")

# ── Insert NoConn flags before $EndSCHEMATC ───────────────────────────────────
patched = patched.replace("$EndSCHEMATC", NEW_NOCONNS + "$EndSCHEMATC", 1)
print(f"Added  : 4 NoConn flags")

# ── Verify no duplicate NoConns at those coords ───────────────────────────────
for coord in ("23900 21000", "23900 21100", "6400 7050", "5600 7150"):
    n = patched.count(f"NoConn ~ {coord}")
    if n != 1:
        print(f"ERROR: NoConn ~ {coord} appears {n}× (expected 1)", file=sys.stderr)
        sys.exit(1)
print("Verified: 4 new NoConn coords each appear exactly once")

# ── Atomic write ──────────────────────────────────────────────────────────────
tmp = SCH + ".dec037.tmp"
with open(tmp, "w", encoding="utf-8") as f:
    f.write(patched)
os.replace(tmp, SCH)

md5_after  = hashlib.md5(patched.encode()).hexdigest()
size_after = len(patched)
delta      = size_after - size_before
print(f"Output : {SCH}  size={size_after} ({delta:+d})  md5={md5_after}")
print("DONE — connectors.sch patched for DEC-037")
