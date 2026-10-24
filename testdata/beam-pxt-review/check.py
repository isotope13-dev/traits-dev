#!/usr/bin/env python3
"""Check WinRT calls versus references and embedded IEX versus prose labels."""
import json
import os
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
root = here.parents[1]
winrt = {
    'micro-behaviors/fs/read/file/full::winrt-fileio-read',
    'micro-behaviors/fs/write/content::winrt-fileio-write-text',
    'micro-behaviors/fs/enumerate/drives::winrt-removable-devices-folders',
    'micro-behaviors/process/create/shellexec::winrt-launch-file',
    'micro-behaviors/hardware/serial::winrt-serial-device-open',
}
iex = 'micro-behaviors/process/interpreter/eval/direct::powershell-expression-command-text'
cases = {
    'winrt-calls.ts': (winrt, set()),
    'winrt-references.ts': (set(), winrt),
    'iex-commands.js': ({iex}, set()),
    'browser-label.js': (set(), {iex}),
}
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
     '--format', 'jsonl', *[str(here / name) for name in cases]],
    text=True, capture_output=True, check=True,
)
decoder = json.JSONDecoder()
stream = result.stdout
seen = set()
while stream.strip():
    report, end = decoder.raw_decode(stream.lstrip())
    stream = stream.lstrip()[end:]
    for file in report.get('files', []):
        name = Path(file['path']).name
        if name not in cases:
            continue
        ids = {trait['id'] for trait in file.get('traits', [])}
        required, forbidden = cases[name]
        assert required <= ids, (name, 'missing', required - ids)
        assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
        seen.add(name)
assert seen == cases.keys(), ('unscanned cases', cases.keys() - seen)
print('PASS: WinRT calls, quoted/commented references, IEX commands and prose labels')
