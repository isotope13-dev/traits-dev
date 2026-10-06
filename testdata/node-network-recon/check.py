#!/usr/bin/env python3
"""Run controls outside testdata so test-harness suppressors cannot mask bugs."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
expected = {
    'objectives/exfiltration/stealer/file::oob-endpoint-file-exfil',
    'objectives/exfiltration/stealer/system-info/network::node-loopback-network-recon-oob-post',
}
for fixture in Path(__file__).parent.glob('*.js'):
    target = scratch / fixture.name
    shutil.copyfile(fixture, target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    traits = report['files'][0]['traits']
    hostile = {t['id'] for t in traits if t['crit'] == 5}
    assert hostile == (expected if fixture.name == 'renamed-network-probe.js' else set()), (fixture.name, hostile)
    if fixture.name == 'non-timeout-callback.js':
        assert not any(t['id'].endswith('settimeout-callback-short-delay') for t in traits)
    assert not any(t['id'].startswith('well-known/lib/ui/bootstrap::') for t in traits)
    print(f'{fixture.name}: passed')
