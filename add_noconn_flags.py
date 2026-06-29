#!/usr/bin/env python3
"""DEC-029: Add NoConn flags to all 826 unconnected pins from 9uzev ERC."""
import os, re, shutil, hashlib

ERC  = '/home/arc/Desktop/ERC files/9uzev_adrv9009_carrier.erc'
BASE = '/home/arc/projects/uzev_carrier_v5'

SHEET_MAP = {
    '/':                  'uzev_adrv9009_carrier.sch',
    '/Connectors/':       'connectors.sch',
    '/Power/':            'power.sch',
    '/ADRV9009_Signals/': 'adrv9009_signals.sch',
    '/Support_IO/':       'support_io.sch',
}

# Parse ERC: group pin locations by sheet
pins = {s: [] for s in SHEET_MAP}
current_sheet = '/'
with open(ERC) as f:
    for line in f:
        m = re.match(r'^\*\*\*\*\* Sheet (.+)', line.strip())
        if m:
            current_sheet = m.group(1)
            continue
        m = re.match(r'\s+@\(([0-9.]+) mm, ([0-9.]+) mm\).*unconnected', line)
        if m and current_sheet in pins:
            x = round(float(m.group(1)) / 0.0254)
            y = round(float(m.group(2)) / 0.0254)
            pins[current_sheet].append((x, y))

total = sum(len(v) for v in pins.values())
print(f"Parsed {total} unconnected pins across {sum(1 for v in pins.values() if v)} sheets")

for sheet, coords in pins.items():
    if not coords:
        continue
    sch = os.path.join(BASE, SHEET_MAP[sheet])
    with open(sch) as f:
        content = f.read()
    noconn_block = ''.join(f'NoConn ~ {x} {y}\n' for x, y in coords)
    content = content.replace('$EndSCHEMATC', noconn_block + '$EndSCHEMATC')
    shutil.copy2(sch, sch + '.bak.before_dec029')
    with open(sch + '.tmp', 'w') as f:
        f.write(content)
    os.replace(sch + '.tmp', sch)
    md5 = hashlib.md5(open(sch,'rb').read()).hexdigest()
    print(f"  {SHEET_MAP[sheet]}: +{len(coords)} NoConn flags  md5={md5}")

print("Done.")
