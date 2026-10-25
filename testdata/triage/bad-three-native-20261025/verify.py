#!/usr/bin/env python3
"""Check inert AutoIt observations; no program or payload is executed."""
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXFIL = 'objectives/exfiltration/stealer/multi-source::autoit-decoded-browser-wallet-telegram-theft'
CLIP = 'objectives/impact/crypto-manipulation/clipboard::autoit-hex-multichain-clipboard-replacement'
RUN = 'objectives/persistence/login/registry/run-key::autoit-clipper-run-key-fallback'
TASK = 'objectives/persistence/system/scheduled-task::autoit-clipper-recurring-self-task'
ALL = {EXFIL, CLIP, RUN, TASK}
CASES = {
    'autoit-observation.au3': ALL,
    'autoit-no-decoder.au3': set(),
    'autoit-no-clipboard-write.au3': {EXFIL},
    'autoit-no-wallet.au3': {CLIP, RUN, TASK},
    'autoit-no-transport.au3': {CLIP, RUN, TASK},
}
for filename, expected in CASES.items():
    result = subprocess.run(
        ['cleave', '--traits-dir', str(ROOT), '--format', 'json', str(HERE / filename)],
        check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    actual = {
        trait['id'] for member in report['files'] for trait in member.get('traits', [])
        if trait['crit'] == 5 and trait['id'] in ALL
    }
    assert actual == expected, (filename, sorted(expected), sorted(actual))
    print(filename, 'PASS', len(actual), 'hostile findings')
