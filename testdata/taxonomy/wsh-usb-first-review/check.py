#!/usr/bin/env python3
"""Static scans only. Never execute the JavaScript fixtures."""
import argparse, json, subprocess, struct
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('--scratch-dir', required=True, type=Path)
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
out = a.scratch_dir
out.mkdir(parents=True, exist_ok=True)
usb = (fixtures / 'usb-positive.js').read_text()
rat = (fixtures / 'wshrat-protocol.js').read_text()
checks = {}
def add(name, source, expected=None):
    path = out / (name + '.js')
    path.write_text(source)
    checks[str(path)] = expected or {}
U = 'objectives/lateral-movement/usb-worm/drive-infector::wsh-hidden-shortcut-drive-worm'
R = 'well-known/malware/rat/houdini::wshrat-http-command-client'
C = 'micro-behaviors/communications/http/cookie-store::document-cookie-expire-directive'
add('usb', usb, {U: True})
add('usb-no-self-copy', usb.replace('fso.CopyFile(WScript.ScriptFullName,', 'fso.CopyFile(otherSource,'), {U: False})
add('usb-fixed-drive', usb.replace('DriveType == 1', 'DriveType == 2'), {U: False})
add('usb-visible-files', usb.replace('file.Attributes = 2 + 4;', ''), {U: False})
add('usb-single-launch', usb.replace('&start Document.pdf', ''), {U: False})
add('rat', rat, {R: True})
add('rat-no-registration', rat.replace('"WSHRAT"', '"ordinary-client"'), {R: False})
add('download', (fixtures / 'http-download.js').read_text(), {C: False, U: False, R: False})
add('cookie', 'document.cookie = "session=; Max-Age=0; path=/";', {C: True})
# Inert synthetic PE headers let the VM-port matcher prove its operation,
# with a neighboring port as the negative control. These files are never run.
def port_pe(port):
    data = bytearray(1024)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x8664, 1, 0, 0, 0, 0xf0, 0x22)
    o = 0x98
    struct.pack_into('<H', data, o, 0x20b)
    struct.pack_into('<III', data, o + 4, 0x200, 0, 0)
    struct.pack_into('<IIQ', data, o + 16, 0x1000, 0x1000, 0x140000000)
    struct.pack_into('<II', data, o + 32, 0x1000, 0x200)
    struct.pack_into('<HH', data, o + 40, 6, 0)
    struct.pack_into('<HH', data, o + 48, 6, 0)
    struct.pack_into('<II', data, o + 56, 0x2000, 0x200)
    struct.pack_into('<HH', data, o + 68, 3, 0x8160)
    struct.pack_into('<I', data, o + 108, 16)
    sec = o + 0xf0
    data[sec:sec + 8] = b'.text\0\0\0'
    struct.pack_into('<IIIIIIHHI', data, sec + 8, 0x200, 0x1000, 0x200, 0x200, 0, 0, 0, 0, 0x60000020)
    code = bytes.fromhex('b868584d56b90a000000bb00000000ba') + struct.pack('<I', port) + bytes.fromhex('edc3')
    data[512:512 + len(code)] = code
    return data
V = 'micro-behaviors/os/virtualization/detect::vmware-version-port-query'
for name, port, expected in [('vm-port', 0x5658, True), ('different-port', 0x5659, False)]:
    path = out / (name + '.exe')
    path.write_bytes(port_pe(port))
    checks[str(path)] = {V: expected}
run = subprocess.run([a.cleave, '--traits-dir', str(root), '--format', 'json', *checks], capture_output=True, text=True)
(out / 'stderr.txt').write_text(run.stderr)
if run.returncode:
    raise SystemExit(run.stderr or run.stdout)
(out / 'reports.json').write_text(run.stdout)
reports = []
remaining = run.stdout.strip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
files = [f for report in reports for f in report.get('files', [report])]
found = {f['path']: f.get('traits', []) for f in files}
for path, expected in checks.items():
    traits = found[path]
    ids = {t['id'] for t in traits}
    for id, want in expected.items():
        assert (id in ids) == want, (Path(path).name, id, want)
    if Path(path).stem in {'download', 'cookie'}:
        assert all(t['crit'] < 4 for t in traits), (path, [(t['id'],t['crit']) for t in traits if t['crit'] >= 4])
print(f'Passed {len(checks)} positive and near-miss controls')
