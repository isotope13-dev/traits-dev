"""Verify relocated native widget APIs and executable-name consumers statically."""
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
pe_image = runpy.run_path(str(ROOT / 'testdata/native-rat-loader-triage/verify.py'))['pe_image']
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
names = ['GetDlgItemTextW', 'SetDlgItemTextW', 'CheckDlgButton', 'GetDlgItem']
data = bytearray(0x200)
struct.pack_into('<IIIII', data, 0, 0x2040, 0, 0, 0x20a0, 0x2070)
data[0xa0:0xab] = b'USER32.dll\0'
cursor = 0xb0
for index, name in enumerate(names):
    struct.pack_into('<Q', data, 0x40 + index * 8, 0x2000 + cursor)
    struct.pack_into('<Q', data, 0x70 + index * 8, 0x2000 + cursor)
    encoded = b'\0\0' + name.encode() + b'\0'
    data[cursor:cursor+len(encoded)] = encoded
    cursor = (cursor + len(encoded) + 1) & ~1
image = bytearray(pe_image(data=data))
struct.pack_into('<II', image, 0x98 + 120, 0x2000, 40)
cases = {
    'widget-imports.exe': bytes(image),
    'widget-strings.exe': pe_image(data='\0'.join(names).encode() + b'\0'),
    'event-name.ps1': 'Write-Output "eventvwr.exe"\n'.encode(),
    'event-near-miss.ps1': 'Write-Output "eventvwr.dll"\n'.encode(),
}
for name, contents in cases.items():
    (out / name).write_bytes(contents)
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json', *[str(out / n) for n in cases]], check=True, capture_output=True, text=True)
(out / 'placement.json').write_text(result.stdout)
decoder = json.JSONDecoder()
remaining = result.stdout
files = []
while remaining.strip():
    doc, end = decoder.raw_decode(remaining.lstrip())
    files.extend(doc.get('files', [doc]))
    remaining = remaining.lstrip()[end:]
rows = {Path(f['path']).name: {t['id']: t['crit'] for t in f.get('traits', [])} for f in files}
# Baseline widget atoms are deliberately stripped from normal reports when
# no composite references them. Debug traces evaluate the actual rules.
ids = ['micro-behaviors/ui/controls/widget::' + name for name in
       ['get-dialog-item-text', 'set-dialog-item-text', 'check-dialog-button', 'get-dialog-item']]
for name, summary in [('widget-imports.exe', 'Summary: 4 matched, 0 not matched'),
                      ('widget-strings.exe', 'Summary: 0 matched, 4 not matched')]:
    trace = subprocess.check_output([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                                     'test-rules', str(out / name), '--rules', ','.join(ids)], text=True)
    (out / (name + '.trace.txt')).write_text(trace)
    assert summary in trace, trace
rule = 'micro-behaviors/fs/path/basename::eventvwr-exe-reference'
assert rows['event-name.ps1'].get(rule) == 3
assert rule not in rows['event-near-miss.ps1']
print('PASS: native widget imports, string-only near miss, Event Viewer name and near miss')
