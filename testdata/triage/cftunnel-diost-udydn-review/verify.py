#!/usr/bin/env python3
"""Focused controls for the three registry second reviews; never runs payloads."""
import argparse
import json
import struct
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--samples', type=Path, required=True)
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
args.scratch.mkdir(parents=True, exist_ok=True)
pe = args.samples / '50af5e9b064f/diost.payload.bin'
java = args.samples / 'd2f6b31dde5f/papercut-udydn-bridge.java'
original = pe.read_bytes()
peoff = struct.unpack_from('<I', original, 0x3c)[0]
optional = peoff + 24
section = optional + struct.unpack_from('<H', original, peoff + 20)[0]
text_rva, text_off = struct.unpack_from('<I', original, section + 12)[0], struct.unpack_from('<I', original, section + 20)[0]
guard = original[text_off + 0x3badc - text_rva:text_off + 0x3bb82 - text_rva]


def synthetic_pe(code):
    """Data-only test image; retain PE syntax but no original application code."""
    header = bytearray(original[:0x600])
    struct.pack_into('<H', header, peoff + 6, 1)
    struct.pack_into('<I', header, optional + 16, 0x1000)
    struct.pack_into('<I', header, optional + 56, 0x2000)
    struct.pack_into('<I', header, optional + 64, 0)
    header[optional + 112:optional + 112 + 16 * 8] = bytes(16 * 8)
    struct.pack_into('<IIII', header, section + 8, len(code), 0x1000, 0x200, 0x600)
    header[section + 40:section + 160] = bytes(120)
    return bytes(header) + code.ljust(0x200, b'\x90')


specs = {}

def add(name, data, required=(), absent=(), no_hostile=False):
    p = args.scratch / name
    p.write_bytes(data if isinstance(data, bytes) else data.encode())
    specs[name] = {'required': list(required), 'absent': list(absent), 'no_hostile': no_hostile}


gate = 'objectives/anti-analysis/environment-detect/check::peb-pointer-decoy-constant-x64'
mul = 'metadata/binary/instruction/operand::x86-imul-31'
http = 'objectives/anti-static/obfuscation/imports/api-hashing::near-fnv-winhttp-hash-table'
cls = 'micro-behaviors/fs/delete/file/library::java-class-file-delete-source'
tasking = 'objectives/command-and-control/remote-command/dispatch::java-filesystem-base64-shell-tasking'
logs = 'objectives/evasion/indicator-removal/application-logs::java-command-tasking-log-deletion'
add('peb-key.exe', synthetic_pe(guard), [gate], no_hostile=True)
add('renamed-key.exe', synthetic_pe(guard), [gate], no_hostile=True)
add('no-peb.exe', synthetic_pe(guard.replace(bytes.fromhex('65 48 8b 04 25 60'), bytes.fromhex('65 48 8b 04 25 30'), 1)), absent=[gate], no_hostile=True)
add('no-heap-check.exe', synthetic_pe(guard.replace(bytes.fromhex('48 8b 40 30'), bytes.fromhex('48 8b 40 20'), 1)), absent=[gate], no_hostile=True)
add('no-decoy.exe', synthetic_pe(guard.replace(bytes.fromhex('ef be ad de'), bytes(4))), absent=[gate], no_hostile=True)
add('arithmetic.exe', synthetic_pe(bytes.fromhex('48 6b c0 1f c3')), [mul], absent=[gate, http], no_hostile=True)
add('hashes-only.exe', synthetic_pe(bytes.fromhex('b3 90 e0 4f 31 d5 26 07 da 6f bc 54 ba dd 4d 04 da 24 c5 81 fd 5f b6 73')), absent=[http, gate], no_hostile=True)
add('BuildCleanup.java', 'import java.io.File; class BuildCleanup { void clean() { new File("build/Old.class").delete(); }}', [cls], absent=[tasking, logs], no_hostile=True)
add('Comment.java', 'class Comment { /* new File("lib/Self.class").delete(); */ }', absent=[cls, tasking, logs], no_hostile=True)
source = java.read_text()
worker = source[source.index('public class Udydn'):source.index('    private static void wipeLogs')]
worker = worker.replace('            wipeLogs();', '').replace('            selfDestruct();', '') + '}\n'
add('BatchWorker.java', 'import java.io.*; import java.nio.file.*; import java.util.Base64;\n' + worker, absent=[tasking, logs], no_hostile=True)
add('install.sh', '#!/bin/sh\n# Usage: curl -fsSL https://raw.githubusercontent.com/vendor/tool/main/install.sh | bash\n', absent=['objectives/execution/trigger/agent::session-hook-curl-pipe-shell'], no_hostile=True)
add('catalog.lua', '\n'.join('local text%d = "entry %d"' % (i, i) for i in range(2100)), required=['metadata/file/profile/string-population::lua-string-count-2000-plus'], no_hostile=True)

add('references.sh', "#!/bin/sh\nprintf '%s' 'docker-compose.yml' 'celerybeat-schedule' 'https://github.com/fatedier/frp/releases/'\n", required=['micro-behaviors/fs/path/config/app::docker-compose-yml-name', 'micro-behaviors/fs/path/metadata-store::celerybeat-schedule-name', 'micro-behaviors/communications/url/external/github::frp-repo-reference'], absent=['objectives/discovery/network/scan/http::notebook-stack-config-targets', 'well-known/dual-use/tunnel/frp::frp-repo'], no_hostile=True)
add('sshpath.go', 'package demo\nconst keyPath = "/tmp/id_rsa"\n', required=['micro-behaviors/fs/path/private-key::go-user-ssh-private-key-paths'], absent=['objectives/credential-access/files/config::go-user-ssh-private-key-paths'], no_hostile=True)
add('pointer-load.exe', synthetic_pe(bytes.fromhex('8b 40 3c c3')), no_hostile=True)
add('pointer-sib.exe', synthetic_pe(bytes.fromhex('8b 44 3c 20 c3')), no_hostile=True)

proc = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', str(args.scratch)], text=True, capture_output=True)
if proc.returncode:
    raise RuntimeError(proc.stderr + proc.stdout)
reports = []
remaining = proc.stdout.lstrip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
files = [f for report in reports for f in report.get('files', [report])]
results = []
seen = set()
for f in files:
    name = Path(f['path']).name
    if name not in specs:
        continue
    seen.add(name)
    traits = {t['id']: t['crit'] for t in f.get('traits', [])}
    spec = specs[name]
    missing = set(spec['required']) - traits.keys()
    unexpected = set(spec['absent']) & traits.keys()
    hostile = [k for k, v in traits.items() if v == 5]
    assert not missing and not unexpected and not (spec['no_hostile'] and hostile), (name, missing, unexpected, hostile)
    results.append({'case': name, 'passed': True, 'hostile': hostile, **spec})
assert seen == specs.keys(), (seen, specs.keys())
# A SIB index byte of 0x3c must not be called an e_lfanew displacement.
pointer_pattern = '8B (40|41|42|43|45|46|47|48|49|4A|4B|4D|4E|4F) 3C'
for name, matched in [('pointer-load.exe', True), ('pointer-sib.exe', False)]:
    debug = subprocess.run([args.cleave, 'test-match', str(args.scratch / name), '--type', 'hex', '--pattern', pointer_pattern, '--section', '.text'], text=True, capture_output=True, check=True)
    actual = 'MATCHED' in debug.stdout and 'NOT MATCHED' not in debug.stdout
    assert actual == matched, (name, debug.stdout, debug.stderr)

Path(__file__).with_name('results.json').write_text(json.dumps(results, indent=2) + '\n')
print('%d focused controls passed' % len(results))
