#!/usr/bin/env python3
"""Verify timing observations keep their matches and hostile consumers."""
import json
from pathlib import Path
import subprocess

fixtures = Path(__file__).resolve().parent
root = fixtures.parents[2]
query = 'micro-behaviors/time/query::vbs-dateadd-seconds'
measure = 'micro-behaviors/time/timing/check::vbs-timer-sleep-delta-check'
loop = 'micro-behaviors/time/sleep/interval::vbs-wall-clock-sleep-loop'
objective = 'objectives/anti-analysis/timing/evasion::'
cases = {
    'date-offset.vbs': ({query}, None),
    'sleep-measurement.vbs': ({measure}, None),
    'sleep-loop.vbs': ({query, loop}, None),
    'delayed-dispatch.vbs': ({query, loop}, objective + 'vbs-delayed-assembled-shell-loader'),
    'sleep-check-dispatch.vbs': ({measure}, objective + 'vbs-sleep-acceleration-sandbox-evasion'),
}
for name, (required, hostile) in cases.items():
    result = subprocess.run(
        ['cleave', '--traits-dir', str(root), '--format', 'json', str(fixtures / name)],
        text=True, capture_output=True, check=True,
    )
    traits = json.loads(result.stdout)['files'][0]['traits']
    ids = {trait['id'] for trait in traits}
    assert required <= ids, (name, required - ids)
    for old in ['vbs-dateadd-seconds', 'vbs-timer-sleep-delta-check', 'vbs-wall-clock-sleep-loop']:
        assert objective + old not in ids, (name, old)
    assert all(t['crit'] == 3 for t in traits if t['id'] in required), name
    if hostile:
        assert any(t['id'] == hostile and t['crit'] == 5 for t in traits), name
    else:
        assert all(t['crit'] < 4 for t in traits), name
    print('PASS', name)
