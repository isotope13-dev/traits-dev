#!/usr/bin/env python3
"""Fingerprint and client context are capabilities, not proof of theft."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
source = '''const vscode = require('vscode');
async function send(e) {
  const {getFootprintV2:t} = await a.e("runtime").then(a.bind(a,1));
  e.clientContext = await t();
  this.getSocket().send(e);
  const headers = {"x-client-context": e.clientContext};
}
const x = {initializeFingerprint: init};
'''
cases = {'context.js': source,
         'no-socket.js': source.replace('this.getSocket().send(e);', 'log(e);'),
         'no-fingerprint.js': source.replace('getFootprintV2', 'getOrdinaryValue')}
with tempfile.TemporaryDirectory(prefix='vscode-fingerprint-') as temp:
    root = Path(temp)
    for name, body in cases.items():
        (root / name).write_text(body)
    hostile = repo / 'testdata/hostile/generated/device-enrollment-fingerprint/concealed-enrollment-client.js'
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(root / n) for n in cases), str(hostile)],
                       check=True, capture_output=True, text=True)
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    prefix = 'micro-behaviors/os/sysinfo/machine-id::'
    assert prefix + 'fingerprint-client-context-socket-clues' in found['context.js']
    assert prefix + 'fingerprint-client-context-header-clues' in found['context.js']
    assert prefix + 'fingerprint-client-context-socket-clues' not in found['no-socket.js']
    assert prefix + 'fingerprint-client-context-header-clues' not in found['no-fingerprint.js']
    assert not any('vscode-lazy-runtime-fingerprint' in trait for ids in found.values() for trait in ids)
    assert ('objectives/exfiltration/stealer/system-info/host-fingerprint::'
            'node-concealed-device-enrollment-exfil') in found[hostile.name]
    print('Fingerprint context reports observations without asserting exfiltration.')
