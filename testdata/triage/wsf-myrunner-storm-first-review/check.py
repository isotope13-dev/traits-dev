#!/usr/bin/env python3
"""Regression checks for observation/intent and signer-presence boundaries."""
import argparse
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
small = 'metadata/binary/layout/overlay::signed-pe-small-noncertificate-overlay'
large = 'metadata/binary/layout/overlay::signed-pe-large-noncertificate-overlay'
locale = 'metadata/lang/locale::language-label-code-de'
clr = 'micro-behaviors/process/interpreter/runtime/clr::powershell-xor-assembly-reflection-profile'
removed = {
    'objectives/execution/payload/module-load::powershell-xor-reflected-assembly-invocation',
    'objectives/anti-static/obfuscation/payload/resource::unsigned-dotnet-opaque-resource-decode-resolver-profile',
    'micro-behaviors/data/source/prototype::js-proto-guard-prototype',
    'micro-behaviors/data/source/prototype::js-proto-pollution-guard',
}

with tempfile.TemporaryDirectory(prefix='first-review-controls-', dir=args.output) as temporary:
    tmp = Path(temporary)
    # This repository fixture carries a parsed subject; verification/trust is
    # deliberately outside the signed-record profile's claim.
    body = (ROOT / 'testdata/hostile/forged-microsoft-pca-signature.exe').read_bytes()
    pe = struct.unpack_from('<I', body, 0x3c)[0]
    optional = pe + 24
    magic = struct.unpack_from('<H', body, optional)[0]
    security = optional + (112 if magic == 0x20b else 96) + 4 * 8
    cert_offset, cert_size = struct.unpack_from('<II', body, security)
    unsigned = bytearray(body[:cert_offset])
    struct.pack_into('<II', unsigned, security, 0, 0)
    corrupt = bytearray(body)
    corrupt[cert_offset:cert_offset + cert_size] = bytes(cert_size)
    bodies = {
        'signed-small.exe': body + bytes(1024),
        'signed-large.exe': body + bytes(65536),
        'unsigned-small.exe': bytes(unsigned) + bytes(1024),
        'certificate-without-subject.exe': bytes(corrupt) + bytes(1024),
    }
    for name, value in bodies.items():
        (tmp / name).write_bytes(value)
    sources = [HERE / name for name in (
        'locale-positive.js', 'url-near-miss.js',
        'reflection-positive.ps1', 'reflection-near-miss.ps1',
        'literal-branch-positive.js', 'literal-branch-near-miss.js')]
    paths = sources + [tmp / name for name in bodies]
    run = subprocess.run(
        [args.cleave, '--traits-dir', str(ROOT), '--no-update-check', '--format', 'json', *map(str, paths)],
        text=True, capture_output=True, check=True,
        env={**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'CLEAVE_VALIDATE': '0'})
    (args.output / 'controls.stderr.txt').write_text(run.stderr)
    decoder, rest, reports = json.JSONDecoder(), run.stdout, []
    while rest.strip():
        report, end = decoder.raw_decode(rest.lstrip())
        rest = rest.lstrip()[end:]
        reports.append(report)
    files = {Path(f['path']).name: f for r in reports for f in r['files']}
    results = []
    for path in paths:
        file = files[path.name]
        ids = {t['id'] for t in file['traits']}
        assert not ids & removed, (path.name, ids & removed)
        assert (small in ids) == (path.name == 'signed-small.exe'), path.name
        assert (large in ids) == (path.name == 'signed-large.exe'), path.name
        assert (locale in ids) == (path.name == 'locale-positive.js'), path.name
        assert (clr in ids) == (path.name == 'reflection-positive.ps1'), path.name
        branch = 'micro-behaviors/data/control-flow/branch::js-literal-string-if-comparison'
        assert (branch in ids) == (path.name == 'literal-branch-positive.js'), path.name
        assert 'objectives/anti-static/obfuscation/control-flow/logic::js-rc4-literal-branch-padding' not in ids, path.name
        if path.name in {'reflection-positive.ps1', 'reflection-near-miss.ps1'}:
            assert not any(t['crit'] == 5 for t in file['traits']), path.name
        results.append({'fixture': path.name, 'passed': True})
    (args.output / 'controls-results.json').write_text(json.dumps(results, indent=2) + '\n')
    (args.output / 'controls-reports.json').write_text(json.dumps(reports) + '\n')
    print(f'PASS: {len(results)} observation/intent and signing controls')
