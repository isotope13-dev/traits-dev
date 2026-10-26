#!/usr/bin/env python3
"""Check storage-to-peer binding without running the browser bridge."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent/'cleave/target/release/cleave'))
TRAIT = 'micro-behaviors/communications/ipc/message::wildcard-peer-browser-storage-export'
SOURCE = 'function reply(event){event.source.postMessage(JSON.stringify({Data:localStorage}),"*");}'
CASES = [
    ('local', SOURCE, True),
    ('session', SOURCE.replace('localStorage', 'sessionStorage'), True),
    ('qualified', SOURCE.replace('localStorage', 'window.localStorage'), True),
    ('renamed', SOURCE.replace('event', 'message').replace('Data:', 'payload:'), True),
    ('pinned-origin', SOURCE.replace('"*"', '"https://app.example"'), False),
    ('unrelated-data', SOURCE.replace('localStorage', 'userSettings'), False),
    ('wrong-call', SOURCE.replace('postMessage', 'recordMessage'), False),
    ('wrong-source', SOURCE.replace('.source.', '.cache.'), False),
    ('scalar-value', SOURCE.replace('localStorage', 'localStorage.getItem("theme")'), False),
    ('comment', '// '+SOURCE, False),
]

with tempfile.TemporaryDirectory(prefix='browser-store-controls-') as temporary:
    paths = []
    for name, source, _ in CASES:
        p = Path(temporary)/(name+'.js')
        p.write_text(source)
        paths.append(str(p))
    run = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'jsonl', *paths],
                         capture_output=True, text=True, check=True)
    remaining = run.stdout.lstrip()
    decoder = json.JSONDecoder()
    matched = set()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for f in report.get('files', []):
            if any(t['id'] == TRAIT for t in f.get('traits', [])):
                matched.add(Path(f['path']).stem)
    for name, _, expected in CASES:
        assert (name in matched) == expected, (name, expected)
print(json.dumps({'passed': len(CASES), 'cases': [c[0] for c in CASES]}, indent=2))
