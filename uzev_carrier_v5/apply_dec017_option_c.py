#!/usr/bin/env python3
"""
apply_dec017_option_c.py
DEC-017 Option C: JTAG J7 wiring for support_io.sch
Per manual_jtag_wiring_spec.md + DEC-015/DEC-017.

Phases:
  1a. Move $Comp blocks: R6, R7, R8, R9, #PWR020
  1b. Move JTAG GLabels (x=8100) to new y-positions
  2.  Delete 8 old wires (4 left body, 4 right stubs)
  3.  Add 10 new wires (4 left unified, 4 right to J7, 1 VCC, 1 GND)
  4.  Insert new VCCO_HP_65 GLabel at (11500,7700) orient=2

Aborts on any verification failure. Atomic write via .tmp + os.replace.
DO NOT execute without user approval.
"""

import os, hashlib, re, sys

SCH = '/home/arc/projects/uzev_carrier_v5/support_io.sch'

# Expected baseline (post-DEC-018, pre-Option-C)
EXPECTED_MD5  = 'ac1a54d99fdde60ed5836ed443eb38e2'
EXPECTED_SIZE = 11664

# ── configuration ─────────────────────────────────────────────────────────────

# Phase 1a: resistor P_y moves {refdes: (old_y, new_y)}
RESISTOR_MOVES = {
    'R6': (7600, 7900),
    'R7': (7900, 8100),
    'R8': (8200, 8000),
    'R9': (8500, 7800),
}

# Phase 1b: JTAG GLabel y-moves; all at x=8100, orient=0, type=BiDi
GLABEL_MOVES = {
    'JTAG_TCK': (7600, 7900),
    'JTAG_TDI': (7900, 8100),
    'JTAG_TDO': (8200, 8000),
    'JTAG_TMS': (8500, 7800),
}

# Phase 1a: #PWR020 move
PWR020_OLD_Y = 9100
PWR020_NEW_Y = 8200

# Phase 2: old wire coord lines to delete (tab-prefixed, no newline)
OLD_WIRES = {
    '\t8500 7600 8900 7600',   # R6 left body (old y)
    '\t8500 7900 8900 7900',   # R7 left body (old y)
    '\t8500 8200 8900 8200',   # R8 left body (old y)
    '\t8500 8500 8900 8500',   # R9 left body (old y)
    '\t9300 7600 10700 7600',  # R6 right stub (old y)
    '\t9300 7900 10700 7900',  # R7 right stub (old y)
    '\t9300 8200 10700 8200',  # R8 right stub (old y)
    '\t9300 8500 10700 8500',  # R9 right stub (old y)
}

# Phase 3+: new wire coordinates (no tab)
# Left wires are unified 8100→8900 (combines spec 6a gap-fill + 6b body wire)
NEW_WIRE_COORDS = [
    '8100 7800 8900 7800',    # TMS/R9 left
    '8100 7900 8900 7900',    # TCK/R6 left
    '8100 8000 8900 8000',    # TDO/R8 left
    '8100 8100 8900 8100',    # TDI/R7 left
    '9300 7800 11300 7800',   # TMS/R9 → J7 pin 2
    '9300 7900 11300 7900',   # TCK/R6 → J7 pin 3
    '9300 8000 11300 8000',   # TDO/R8 → J7 pin 4
    '9300 8100 11300 8100',   # TDI/R7 → J7 pin 5
    '11300 7700 11500 7700',  # J7 pin 1 → new VCCO_HP_65 GLabel
    '11100 8200 11300 8200',  # #PWR020 → J7 pin 6
]

# Phase 4: new GLabel (same format as existing VCCO_HP_65 at 11500,8900)
NEW_GLABEL = [
    'Text GLabel 11500 7700 2    40   Input ~ 0\n',
    'VCCO_HP_65\n',
]

# ── helpers ───────────────────────────────────────────────────────────────────

def file_md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()

def shift_comp_y(block, delta):
    """Shift all y-coordinates in a $Comp block by delta."""
    out = []
    for raw in block:
        s = raw.rstrip('\n')

        # P x y
        m = re.match(r'^(P \d+ )(\d+)(.*)$', s)
        if m:
            out.append(m.group(1) + str(int(m.group(2)) + delta) + m.group(3) + '\n')
            continue

        # F n "text" style x y rest
        m = re.match(r'^(F \d+ "(?:[^"]*)" \S+ \d+ )(\d+)(.*)$', s)
        if m:
            out.append(m.group(1) + str(int(m.group(2)) + delta) + m.group(3) + '\n')
            continue

        # \tunit x y  (exactly 3 tokens after tab; matrix row has 4 tokens — not matched)
        m = re.match(r'^(\t\d+\s+\d+\s+)(\d+)\s*$', s)
        if m:
            out.append(m.group(1) + str(int(m.group(2)) + delta) + '\n')
            continue

        out.append(raw)
    return out

# ── preflight ────────────────────────────────────────────────────────────────

actual_size = os.path.getsize(SCH)
actual_md5  = file_md5(SCH)
if actual_size != EXPECTED_SIZE or actual_md5 != EXPECTED_MD5:
    print(f'PREFLIGHT FAIL: expected size={EXPECTED_SIZE} md5={EXPECTED_MD5}')
    print(f'                actual   size={actual_size} md5={actual_md5}')
    sys.exit(1)
print(f'PREFLIGHT OK:   size={actual_size} md5={actual_md5}')

with open(SCH) as f:
    lines = f.readlines()

# ── phase 1a: move $Comp blocks ───────────────────────────────────────────────

pass1 = []
i = 0
comp_applied = {k: False for k in list(RESISTOR_MOVES) + ['#PWR020']}

while i < len(lines):
    if lines[i].strip() == '$Comp':
        block = []
        while lines[i].strip() != '$EndComp':
            block.append(lines[i])
            i += 1
        block.append(lines[i])  # $EndComp
        i += 1

        ref = None
        for bl in block:
            m = re.match(r'^L Device:R (R\d+)\s*$', bl.strip())
            if m and m.group(1) in RESISTOR_MOVES:
                ref = m.group(1); break
            if bl.strip() == 'L power:GND #PWR020':
                ref = '#PWR020'; break

        if ref in RESISTOR_MOVES:
            old_y, new_y = RESISTOR_MOVES[ref]
            block = shift_comp_y(block, new_y - old_y)
            comp_applied[ref] = True
        elif ref == '#PWR020':
            block = shift_comp_y(block, PWR020_NEW_Y - PWR020_OLD_Y)
            comp_applied['#PWR020'] = True

        pass1.extend(block)
    else:
        pass1.append(lines[i])
        i += 1

# ── phase 1b: move JTAG GLabels ──────────────────────────────────────────────

pass2 = []
i = 0
glabel_applied = {k: False for k in GLABEL_MOVES}

while i < len(pass1):
    line = pass1[i]
    if line.startswith('Text GLabel 8100 ') and i + 1 < len(pass1):
        sig = pass1[i + 1].strip()
        if sig in GLABEL_MOVES:
            old_y, new_y = GLABEL_MOVES[sig]
            m = re.match(r'^(Text GLabel 8100 )(\d+)( .+\n)$', line)
            if m and int(m.group(2)) == old_y:
                pass2.append(m.group(1) + str(new_y) + m.group(3))
                glabel_applied[sig] = True
                i += 1
                pass2.append(pass1[i])  # signal name line unchanged
                i += 1
                continue
    pass2.append(line)
    i += 1

# ── phase 2: delete old wires ────────────────────────────────────────────────

pass3 = []
i = 0
wires_deleted = 0

while i < len(pass2):
    if pass2[i].strip() == 'Wire Wire Line' and i + 1 < len(pass2):
        coord = pass2[i + 1].rstrip('\n')
        if coord in OLD_WIRES:
            wires_deleted += 1
            i += 2
            continue
    pass3.append(pass2[i])
    i += 1

# ── phase 3/4: inject new GLabel + wires before $EndSCHEMATC ─────────────────

final = []
for line in pass3:
    if line.strip() == '$EndSCHEMATC':
        final.extend(NEW_GLABEL)
        for coord in NEW_WIRE_COORDS:
            final.append('Wire Wire Line\n')
            final.append('\t' + coord + '\n')
        final.append(line)
    else:
        final.append(line)

# ── verification ──────────────────────────────────────────────────────────────

content = ''.join(final)
ok = True

print('\n--- VERIFICATION ---')

for ref, done in comp_applied.items():
    tag = 'OK' if done else 'FAIL'
    print(f'{tag}: $Comp {ref} moved')
    if not done: ok = False

for sig, done in glabel_applied.items():
    tag = 'OK' if done else 'FAIL'
    print(f'{tag}: GLabel {sig} moved')
    if not done: ok = False

tag = 'OK' if wires_deleted == 8 else 'FAIL'
print(f'{tag}: old wires deleted ({wires_deleted}/8)')
if wires_deleted != 8: ok = False

for coord in NEW_WIRE_COORDS:
    present = ('\t' + coord + '\n') in content
    tag = 'OK' if present else 'FAIL'
    print(f'{tag}: new wire {coord}')
    if not present: ok = False

gl_ok = 'Text GLabel 11500 7700 2    40   Input ~ 0\n' in content
tag = 'OK' if gl_ok else 'FAIL'
print(f'{tag}: new VCCO_HP_65 GLabel at (11500,7700)')
if not gl_ok: ok = False

end_n = content.count('$EndSCHEMATC')
tag = 'OK' if end_n == 1 else 'FAIL'
print(f'{tag}: $EndSCHEMATC count={end_n}')
if end_n != 1: ok = False

if not ok:
    print('\nABORTED — verification failed, no file written.')
    sys.exit(1)

# ── atomic write ──────────────────────────────────────────────────────────────

tmp = SCH + '.tmp'
with open(tmp, 'w') as f:
    f.write(content)
os.replace(tmp, SCH)

sz  = os.path.getsize(SCH)
md5 = file_md5(SCH)
print(f'\nAFTER: size={sz} md5={md5}')
print('DONE')
