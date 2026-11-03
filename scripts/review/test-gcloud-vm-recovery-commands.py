#!/usr/bin/env python3
"""Check VM-operation and startup-script command recognition."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
PREFIX = 'micro-behaviors/os/virtualization/management::'
STOP = PREFIX + 'gcloud-compute-instance-stop'
DETACH = PREFIX + 'gcloud-compute-instance-detach-disk'
ATTACH = PREFIX + 'gcloud-compute-instance-attach-disk'
DELETE = PREFIX + 'gcloud-compute-instance-delete'
STARTUP = PREFIX + 'gcloud-windows-startup-script-file'
CASES = {
    'stop': ('gcloud compute instances stop "$vm"\n', {STOP}),
    'detach': ('gcloud compute instances detach-disk "$vm" --disk="$disk"\n', {DETACH}),
    'attach': ('gcloud compute instances attach-disk "$vm" --disk="$disk" --boot\n', {ATTACH}),
    'delete': ('gcloud compute instances delete "$vm"\n', {DELETE}),
    'startup': ('gcloud compute instances create "$vm" --metadata-from-file=windows-startup-script-ps1="$script"\n', {STARTUP}),
    'absolute': ('/usr/bin/gcloud compute instances stop "$vm"\n', {STOP}),
    'different-resource': ('gcloud compute disks delete "$disk"\n', set()),
    'echo': ('echo gcloud compute instances delete "$vm"\n', set()),
    'comment': ('# gcloud compute instances delete "$vm"\n', set()),
    'plain-metadata': ('gcloud compute instances create "$vm" --metadata=windows-startup-script-ps1="$script"\n', set()),
    'linux-startup': ('gcloud compute instances create "$vm" --metadata-from-file=startup-script="$script"\n', set()),
}
with tempfile.TemporaryDirectory(prefix='gcloud-vm-') as tmp:
    paths = []
    for name, (source, _) in CASES.items():
        p = Path(tmp) / (name + '.sh')
        p.write_text('#!/bin/sh\n' + source)
        paths.append(str(p))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(CASES)
    relevant = {STOP, DETACH, ATTACH, DELETE, STARTUP}
    for f in reports:
        name = Path(f['path']).stem
        got = {t['id'] for t in f.get('traits', [])} & relevant
        assert got == CASES[name][1], (name, got, CASES[name][1])
print('gcloud VM operations are distinguished from comments, other resources, and metadata')
