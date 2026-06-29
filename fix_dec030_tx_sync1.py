#!/usr/bin/env python3
"""
DEC-030 fix: add missing GLabels for tx_sync_1 differential pair.

Changes:
  adrv9009_signals.sch — insert 4 GLabels around existing tie wires at Y=6200/6450
  connectors.sch       — remove 4 NoConn flags, insert FMC H31/H32 stubs and JX1 B36/B37 stubs
"""
import os, hashlib, re

def md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()

def atomic_write(path, content):
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        f.write(content)
    os.replace(tmp, path)

# ── adrv9009_signals.sch ─────────────────────────────────────────────────────

SIG = '/home/arc/projects/uzev_carrier_v5/adrv9009_signals.sch'
sig_before = md5(SIG)
print(f'adrv9009_signals.sch before: {sig_before}')

sig_text = open(SIG).read()

OLD_SIG = (
    'Wire Wire Line\n'
    '\t12400 6200 13000 6200\n'
    'Text Notes 14000 6220 0    25   ~ 0\n'
    'tx_sync_1_p (H31_LA28_P->B36)\n'
    'Wire Wire Line\n'
    '\t12400 6450 13000 6450\n'
    'Text Notes 14000 6470 0    25   ~ 0\n'
    'tx_sync_1_n (H32_LA28_N->B37)\n'
)

NEW_SIG = (
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

assert OLD_SIG in sig_text, 'ABORT: adrv9009_signals.sch pattern not found'
assert sig_text.count(OLD_SIG) == 1, 'ABORT: pattern found more than once'

sig_text_new = sig_text.replace(OLD_SIG, NEW_SIG, 1)
atomic_write(SIG, sig_text_new)
sig_after = md5(SIG)
print(f'adrv9009_signals.sch after:  {sig_after}')

# ── connectors.sch ───────────────────────────────────────────────────────────

CON = '/home/arc/projects/uzev_carrier_v5/connectors.sch'
con_before = md5(CON)
print(f'connectors.sch before: {con_before}')

con_text = open(CON).read()

# Step 1: remove NoConn flags for FMC H31/H32 pins
for noconn in ('NoConn ~ 23900 21000\n', 'NoConn ~ 23900 21100\n'):
    assert noconn in con_text, f'ABORT: {noconn.strip()} not found'
    assert con_text.count(noconn) == 1, f'ABORT: {noconn.strip()} found multiple times'
    con_text = con_text.replace(noconn, '', 1)

# Step 2: remove NoConn flags for JX1 B36/B37 pins
for noconn in ('NoConn ~ 6400 7050\n', 'NoConn ~ 5600 7150\n'):
    assert noconn in con_text, f'ABORT: {noconn.strip()} not found'
    assert con_text.count(noconn) == 1, f'ABORT: {noconn.strip()} found multiple times'
    con_text = con_text.replace(noconn, '', 1)

# Step 3: insert FMC H31/H32 stubs after FMC_H26_LA21_N block
FMC_ANCHOR = (
    'Wire Wire Line\n'
    '\t23900 20500 23700 20500\n'
    'Text GLabel 23700 20500 2    50   BiDi ~ 0\n'
    'FMC_H26_LA21_N\n'
)
FMC_INSERT = (
    'Wire Wire Line\n'
    '\t23900 21000 23700 21000\n'
    'Text GLabel 23700 21000 2    50   BiDi ~ 0\n'
    'FMC_H31_LA28_P\n'
    'Wire Wire Line\n'
    '\t23900 21100 23700 21100\n'
    'Text GLabel 23700 21100 2    50   BiDi ~ 0\n'
    'FMC_H32_LA28_N\n'
)
assert FMC_ANCHOR in con_text, 'ABORT: FMC anchor block not found in connectors.sch'
assert con_text.count(FMC_ANCHOR) == 1, 'ABORT: FMC anchor found multiple times'
con_text = con_text.replace(FMC_ANCHOR, FMC_ANCHOR + FMC_INSERT, 1)

# Step 4: insert JX1 B36/B37 stubs after HP_DP_34_GC_P block
JX1_ANCHOR = (
    'Wire Wire Line\n'
    '\t6400 6650 6600 6650\n'
    'Text GLabel 6600 6650 0    50   BiDi ~ 0\n'
    'HP_DP_34_GC_P\n'
)
JX1_INSERT = (
    'Wire Wire Line\n'
    '\t6400 7050 6600 7050\n'
    'Text GLabel 6600 7050 0    50   BiDi ~ 0\n'
    'HP_DP_38_P\n'
    'Wire Wire Line\n'
    '\t5600 7150 5400 7150\n'
    'Text GLabel 5400 7150 2    50   BiDi ~ 0\n'
    'HP_DP_38_N\n'
)
assert JX1_ANCHOR in con_text, 'ABORT: JX1 anchor block not found in connectors.sch'
assert con_text.count(JX1_ANCHOR) == 1, 'ABORT: JX1 anchor found multiple times'
con_text = con_text.replace(JX1_ANCHOR, JX1_ANCHOR + JX1_INSERT, 1)

atomic_write(CON, con_text)
con_after = md5(CON)
print(f'connectors.sch after:  {con_after}')

print('DEC-030 fix complete.')
print('Next: open both sheets in KiCad, verify visually, re-run ERC (save as 11uzev_adrv9009_carrier.erc).')
