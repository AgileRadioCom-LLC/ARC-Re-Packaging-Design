#!/usr/bin/env python3
"""
DEC-031 fix: directly merge tx_sync_1 nets by giving both connector stubs the same GLabel name.

Why DEC-030 failed:
  adrv9009_signals.sch already had decorative floating wires at (12400,6200)-(13000,6200)
  and (12400,6450)-(13000,6450) before the fix. Adding GLabels around pre-existing floating
  wires does not produce net merging in KiCad 5.1.5's net resolver.

This fix:
  connectors.sch — rename HP_DP_38_P → FMC_H31_LA28_P  (J1-B36 stub)
                   rename HP_DP_38_N → FMC_H32_LA28_N  (J1-B37 stub)
                   Both J4-H31 and J1-B36 now share the same global label → one merged net.
  adrv9009_signals.sch — revert to pre-DEC030 state: remove the 4 GLabels, keep the
                          original floating wires and text notes (documentation only).

Expected netlist result:
  Net "FMC_H31_LA28_P"  nodes: J4-H31, J1-B36
  Net "FMC_H32_LA28_N"  nodes: J4-H32, J1-B37
  HP_DP_38_P and HP_DP_38_N nets: eliminated entirely
"""
import os, hashlib

def md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()

def atomic_write(path, content):
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        f.write(content)
    os.replace(tmp, path)

# ── connectors.sch ───────────────────────────────────────────────────────────

CON = '/home/arc/projects/uzev_carrier_v5/connectors.sch'
con_before = md5(CON)
print(f'connectors.sch  before: {con_before}')

con_text = open(CON).read()

# Rename J1-B36 stub: HP_DP_38_P → FMC_H31_LA28_P
OLD_B36 = (
    'Wire Wire Line\n'
    '\t6400 7050 6600 7050\n'
    'Text GLabel 6600 7050 0    50   BiDi ~ 0\n'
    'HP_DP_38_P\n'
)
NEW_B36 = (
    'Wire Wire Line\n'
    '\t6400 7050 6600 7050\n'
    'Text GLabel 6600 7050 0    50   BiDi ~ 0\n'
    'FMC_H31_LA28_P\n'
)
assert OLD_B36 in con_text, 'ABORT: HP_DP_38_P stub not found at expected position'
assert con_text.count(OLD_B36) == 1, 'ABORT: HP_DP_38_P stub found multiple times'
con_text = con_text.replace(OLD_B36, NEW_B36, 1)

# Rename J1-B37 stub: HP_DP_38_N → FMC_H32_LA28_N
OLD_B37 = (
    'Wire Wire Line\n'
    '\t5600 7150 5400 7150\n'
    'Text GLabel 5400 7150 2    50   BiDi ~ 0\n'
    'HP_DP_38_N\n'
)
NEW_B37 = (
    'Wire Wire Line\n'
    '\t5600 7150 5400 7150\n'
    'Text GLabel 5400 7150 2    50   BiDi ~ 0\n'
    'FMC_H32_LA28_N\n'
)
assert OLD_B37 in con_text, 'ABORT: HP_DP_38_N stub not found at expected position'
assert con_text.count(OLD_B37) == 1, 'ABORT: HP_DP_38_N stub found multiple times'
con_text = con_text.replace(OLD_B37, NEW_B37, 1)

atomic_write(CON, con_text)
con_after = md5(CON)
print(f'connectors.sch  after:  {con_after}')

# ── adrv9009_signals.sch ─────────────────────────────────────────────────────

SIG = '/home/arc/projects/uzev_carrier_v5/adrv9009_signals.sch'
sig_before = md5(SIG)
print(f'adrv9009_signals.sch before: {sig_before}')

sig_text = open(SIG).read()

# Revert to pre-DEC030 state: remove the 4 GLabels, restore original floating wires
OLD_SIG = (
    'Text GLabel 12000 6200 0    40   BiDi ~ 0\n'
    'FMC_H31_LA28_P\n'
    'Wire Wire Line\n'
    '\t12400 6200 13000 6200\n'
    'Text GLabel 13400 6200 2    40   BiDi ~ 0\n'
    'HP_DP_38_P\n'
    'Text Notes 14000 6220 0    25   ~ 0\n'
    'tx_sync_1_p (H31_LA28_P->B36)\n'
    'Text GLabel 12000 6450 0    40   BiDi ~ 0\n'
    'FMC_H32_LA28_N\n'
    'Wire Wire Line\n'
    '\t12400 6450 13000 6450\n'
    'Text GLabel 13400 6450 2    40   BiDi ~ 0\n'
    'HP_DP_38_N\n'
    'Text Notes 14000 6470 0    25   ~ 0\n'
    'tx_sync_1_n (H32_LA28_N->B37)\n'
)
NEW_SIG = (
    'Wire Wire Line\n'
    '\t12400 6200 13000 6200\n'
    'Text Notes 14000 6220 0    25   ~ 0\n'
    'tx_sync_1_p (H31_LA28_P->B36)\n'
    'Wire Wire Line\n'
    '\t12400 6450 13000 6450\n'
    'Text Notes 14000 6470 0    25   ~ 0\n'
    'tx_sync_1_n (H32_LA28_N->B37)\n'
)
assert OLD_SIG in sig_text, 'ABORT: DEC-030 GLabel block not found in adrv9009_signals.sch'
assert sig_text.count(OLD_SIG) == 1, 'ABORT: pattern found multiple times'

sig_text_new = sig_text.replace(OLD_SIG, NEW_SIG, 1)
atomic_write(SIG, sig_text_new)
sig_after = md5(SIG)
print(f'adrv9009_signals.sch after:  {sig_after}')

print()
print('DEC-031 fix complete.')
print('Next steps:')
print('  1. Open KiCad → reload project (or close/reopen KiCad)')
print('  2. Run ERC — expect 0 errors (H31/H32/B36/B37 now connected via FMC names)')
print('  3. Generate netlist → verify:')
print('     Net "FMC_H31_LA28_P" contains both J4-H31 and J1-B36')
print('     Net "FMC_H32_LA28_N" contains both J4-H32 and J1-B37')
print('  4. Save ERC as 13uzev_adrv9009_carrier.erc')
