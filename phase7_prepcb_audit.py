#!/usr/bin/env python3
"""
Phase 7 pre-PCB-layout audit for UZEV ADRV9009 carrier.
Checks: file hashes, footprint completeness, footprint disk presence,
J6 NoConn status, BOM generation.
Run from project root. No KiCad install required.
"""

import os, re, hashlib, sys
from collections import defaultdict

PROJ = os.path.dirname(os.path.abspath(__file__))
KISYSMOD = '/usr/share/kicad/modules'
CUSTOM_LIB = os.path.join(PROJ, 'UZEV_Connectors.pretty')

SCH_FILES = [
    'connectors.sch',
    'power.sch',
    'adrv9009_signals.sch',
    'support_io.sch',
]

EXPECTED_HASHES = {
    'UZEV_Connectors.lib':  ('63fe2e2e3c9c84424d2f50d959ecd432', 65554),  # DEC-035 Step 1
    'connectors.sch':       ('0377a743d1d3fc07bb2aeb4394f67ba2', 43070),
    'power.sch':            ('8eeabb3d55a62b4177046839b82a2275', 51906),   # DEC-035 Step 3+repair
    'adrv9009_signals.sch': ('e0d870dacab2bcf0028b8c255f9fb0f6', 21227),
    'support_io.sch':       ('34c0a2aeb89bbd37e8e34374e4718a6d', 14504),
}

# Footprints known to NOT be in KISYSMOD — resolved to custom or alternate lib
CUSTOM_FOOTPRINTS = {
    'UZEV_Connectors',
}

FORBIDDEN_FOOTPRINTS = [
    'Package_TO_SOT_SMD:PowerPAD_SO-8_EP_3.9x4.9mm_P1.27mm',       # pre-DEC-033 B5
    'Package_DFN_QFN:VQFN-20-1EP_3.5x3.5mm_P0.5mm_EP2.1x2.1mm',   # pre-DEC-033 L1-L4
    'Package_DFN_QFN:VQFN-14-1EP_3.5x4.5mm_P0.65mm_EP2.1x3.1mm',  # pre-DEC-033 B1-B4
]

# ── helpers ──────────────────────────────────────────────────────────────────

def md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()

def parse_components(sch_path):
    """Return list of dicts {ref, value, footprint, sheet} from a .sch file."""
    components = []
    sheet = os.path.basename(sch_path)
    with open(sch_path) as f:
        content = f.read()
    for block in re.findall(r'\$Comp.*?\$EndComp', content, re.DOTALL):
        ref_m  = re.search(r'^F 0 "([^"]*)"', block, re.MULTILINE)
        val_m  = re.search(r'^F 1 "([^"]*)"', block, re.MULTILINE)
        fp_m   = re.search(r'^F 2 "([^"]*)"', block, re.MULTILINE)
        if not ref_m:
            continue
        ref = ref_m.group(1)
        if ref.startswith('#'):
            continue
        components.append({
            'ref':       ref,
            'value':     val_m.group(1) if val_m else '',
            'footprint': fp_m.group(1)  if fp_m  else '',
            'sheet':     sheet,
        })
    return components

def resolve_footprint_path(fp_string):
    """Return (found:bool, path:str|None). fp_string is 'Lib:Name'."""
    if ':' not in fp_string:
        return False, None
    lib, name = fp_string.split(':', 1)
    if lib in CUSTOM_FOOTPRINTS:
        path = os.path.join(CUSTOM_LIB, name + '.kicad_mod')
    else:
        path = os.path.join(KISYSMOD, lib + '.pretty', name + '.kicad_mod')
    return os.path.isfile(path), path

def check_j6_noconns(sch_path):
    """Verify J6 pins 1-3 have NoConn flags in support_io.sch."""
    with open(sch_path) as f:
        content = f.read()
    # J6 Conn_01x04_Male: pins at X=4700, Y=6500/6600/6700/6800
    # Pins 1-3 should have NoConn; pin 4 should have a wire
    noconn_coords = set(re.findall(r'NoConn ~ (\d+ \d+)', content))
    required = {'4700 6700', '4700 6600', '4700 6500'}
    found = required & noconn_coords
    missing = required - noconn_coords
    return found, missing

# ── checks ───────────────────────────────────────────────────────────────────

def run_audit():
    errors = []
    warnings = []
    passed = []

    print("=" * 60)
    print("UZEV Phase 7 Pre-PCB Audit")
    print("=" * 60)

    # 1. File hashes
    print("\n[1] File hash verification")
    for fname, (exp_md5, exp_size) in EXPECTED_HASHES.items():
        path = os.path.join(PROJ, fname)
        if not os.path.isfile(path):
            errors.append(f"MISSING: {fname}")
            print(f"  MISSING  {fname}")
            continue
        actual_md5  = md5(path)
        actual_size = os.path.getsize(path)
        if actual_md5 == exp_md5 and actual_size == exp_size:
            print(f"  OK       {fname}  md5={actual_md5}")
            passed.append(f"hash:{fname}")
        else:
            msg = f"HASH MISMATCH: {fname}  got {actual_md5}/{actual_size}  exp {exp_md5}/{exp_size}"
            errors.append(msg)
            print(f"  FAIL     {fname}  got {actual_md5}  exp {exp_md5}")

    # 2. Forbidden (pre-DEC-033) footprint strings
    print("\n[2] Forbidden footprint check (pre-DEC-033 strings)")
    for sch in SCH_FILES:
        path = os.path.join(PROJ, sch)
        if not os.path.isfile(path):
            continue
        content = open(path).read()
        for fp in FORBIDDEN_FOOTPRINTS:
            if fp in content:
                errors.append(f"FORBIDDEN footprint still present in {sch}: {fp}")
                print(f"  FAIL  {sch}: {fp}")
    if not errors or not any('FORBIDDEN' in e for e in errors):
        print("  OK  no pre-DEC-033 footprint strings found")
        passed.append("forbidden_fps")

    # 3. Component inventory and footprint completeness
    print("\n[3] Component inventory")
    all_comps = []
    for sch in SCH_FILES:
        comps = parse_components(os.path.join(PROJ, sch))
        all_comps.extend(comps)

    empty_fp = [c for c in all_comps if not c['footprint']]
    print(f"  Total components: {len(all_comps)}")
    print(f"  Empty footprints: {len(empty_fp)}")
    if empty_fp:
        for c in empty_fp:
            errors.append(f"Empty footprint: {c['ref']} in {c['sheet']}")
            print(f"    FAIL  {c['ref']} ({c['sheet']})")
    else:
        passed.append("footprint_completeness")

    # 4. Footprint disk presence
    print("\n[4] Footprint disk presence")
    missing_fp = []
    for c in all_comps:
        if not c['footprint']:
            continue
        found, path = resolve_footprint_path(c['footprint'])
        if not found:
            missing_fp.append((c['ref'], c['footprint'], path))
    if missing_fp:
        print(f"  {len(missing_fp)} footprint file(s) NOT found on disk:")
        for ref, fp, path in missing_fp:
            print(f"    FAIL  {ref}: {fp}")
            print(f"          expected: {path}")
            errors.append(f"Footprint file missing for {ref}: {fp}")
    else:
        print(f"  OK  all {len(all_comps)} footprint files resolved on disk")
        passed.append("footprint_disk")

    # 5. J6 NoConn check
    print("\n[5] J6 UART header NoConn check")
    support_io = os.path.join(PROJ, 'support_io.sch')
    if os.path.isfile(support_io):
        found_nc, missing_nc = check_j6_noconns(support_io)
        if missing_nc:
            for coord in sorted(missing_nc):
                errors.append(f"J6 NoConn missing at coordinate {coord}")
                print(f"  FAIL  NoConn missing at {coord}")
        else:
            print(f"  OK  J6 pins 1-3 NoConn flags present: {sorted(found_nc)}")
            passed.append("j6_noconn")
    else:
        errors.append("support_io.sch not found")

    # 6. BOM summary by value+footprint
    print("\n[6] BOM summary")
    bom = defaultdict(list)
    for c in sorted(all_comps, key=lambda x: x['ref']):
        key = (c['value'], c['footprint'])
        bom[key].append(c['ref'])
    print(f"  {'QTY':>4}  {'REF(S)':<30}  {'VALUE':<20}  FOOTPRINT")
    print(f"  {'-'*4}  {'-'*30}  {'-'*20}  {'-'*40}")
    for (val, fp), refs in sorted(bom.items(), key=lambda x: (-len(x[1]), x[0][0])):
        refs_str = ' '.join(refs)
        fp_short = fp.split(':')[-1] if ':' in fp else fp
        print(f"  {len(refs):>4}  {refs_str:<30}  {val:<20}  {fp_short}")

    # ── summary ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"RESULT: {len(passed)} checks passed, {len(warnings)} warnings, {len(errors)} errors")
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  WARN  {w}")
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  ERR   {e}")
        print("\nAudit FAILED — resolve errors before PCB layout.")
        sys.exit(1)
    else:
        print("\nAudit PASSED — ready for netlist export and PCBnew import.")

if __name__ == '__main__':
    run_audit()
