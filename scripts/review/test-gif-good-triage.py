#!/usr/bin/env python3
"""Static regression checks using recovered GIF triage payloads; never executes samples.

Pass the audit's retained work directory with --triage-work. All modified
specimens are scanner controls, not benign training examples.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
MASK = 'objectives/evasion/masquerade/image::gif-conceals-xor-pe'
STAGE = 'objectives/execution/payload/image-map::encrypted-socket-buffer-execution'
FAMILY = 'well-known/malware/rat/miniduke::command-backdoor'
SINK = 'objectives/execution/exploit/command-injection::js-filename-quote-shell-breakout'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--triage-work', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    recovered = [r for r in json.loads((args.triage_work / 'decoded-payloads.json').read_text())
                 if r['period'] == 8]
    cases = {}

    def add(name, data, required=(), forbidden=(), no_flags=False):
        cases[name] = data, set(required), set(forbidden), no_flags

    for row in recovered:
        pe = Path(row['path']).read_bytes()
        key = hashlib.sha256(row['source_sha256'].encode()).digest()[:8]
        encrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(pe))
        gif = b'GIF89a \0;' + b'seed' + encrypted
        second = STAGE if len(pe) < 20000 else FAMILY
        add(row['source_sha256'][:12] + '-rekeyed.gif', gif, [MASK, second])

    small = Path(next(r['path'] for r in recovered if r['size'] < 20000)).read_bytes()
    # Break one relationship at a time, preserving networking and crypto imports.
    for name, before, after in [
        ('different-call-buffer', bytes.fromhex('ff9524fcffff'), bytes.fromhex('ff9520fcffff')),
        ('different-decrypt-api', bytes.fromhex('ff1514404000'), bytes.fromhex('ff1524404000')),
        ('different-recv-api', bytes.fromhex('6a00575356ff1594404000'), bytes.fromhex('6a00575356ff1584404000')),
        ('nonexecutable-allocation', bytes.fromhex('6a406800300000'), bytes.fromhex('6a046800300000')),
    ]:
        assert small.count(before) >= 1, name
        add(name + '.exe', small.replace(before, after), forbidden=[STAGE])

    inner_rows = json.loads((args.triage_work / 'nrv-payloads.json').read_text())
    inner = Path(next(r['path'] for r in inner_rows if r['path'].endswith('nrv-pe.exe'))).read_bytes()
    host = b'info.leveldelta.com'
    assert host in inner
    add('changed-command-server.exe', inner.replace(host, b'x' * len(host)), [FAMILY])
    add('missing-wire-alphabet.exe', inner.replace(b'0123456789~$', b'0123456789+/'), forbidden=[FAMILY])
    add('missing-response-dialect.exe', inner.replace(b'pid %5d terminated', b'X' * 18), forbidden=[FAMILY])
    add('missing-command-dialect.exe', inner.replace(b'pskill', b'XXXXXX'), forbidden=[FAMILY])

    add('ordinary.gif', bytes.fromhex('47494638396101000100800000000000ffffff2c00000000010001000002024401003b'), no_flags=True)
    add('unrelated-names.php', b'<?php class Broadcast { /* Illuminate\\Broadcasting\\PendingBroadcast */ }', no_flags=True)
    add('empty-display.py', b'class Display:\n def __str__(self): return ""\n def __repr__(self): return ""\n',
        required=['micro-behaviors/data/string/conversion::python-empty-str-conversion',
                  'micro-behaviors/data/string/conversion::python-empty-repr-conversion',
                  'micro-behaviors/data/string/conversion::python-empty-str-and-repr'], no_flags=True)
    add('nonempty-triple-quotes.py', b'class Display:\n def __str__(self): return """value"""\n def __repr__(self): return """value"""\n',
        forbidden=['micro-behaviors/data/string/conversion::python-empty-str-conversion',
                   'micro-behaviors/data/string/conversion::python-empty-repr-conversion'], no_flags=True)
    add('empty-prepend.php', b'auto_prepend_file=""\nauto_append_file=\'\'\n',
        forbidden=['micro-behaviors/communications/http/server/config::ini-auto-prepend-file',
                   'micro-behaviors/communications/http/server/config::ini-auto-append-file'], no_flags=True)
    add('prepend.phpt', b'--TEST--\nINI regression\n--INI--\nauto_prepend_file=inc.inc\n--FILE--\n<?php echo 1;\n',
        required=['micro-behaviors/communications/http/server/config::ini-auto-prepend-file'], no_flags=True)
    add('display-self.bat', b'@echo off\nfindstr "^::" <"%~f0"\n', no_flags=True)
    add('self-section.sh', b'#!/bin/sh\nsed -n "/^DOC/,/^DOC_END/p" "$0" |tail -n +2 | head -n -1\n',
        required=['micro-behaviors/fs/read/self::shell-self-section-extract'], no_flags=True)
    add('shortener-comment.js', b'// https://bit.ly/documentation\nwindow.location.href = object_url;\n', no_flags=True)
    add('invisible.c', b'bool invisible(struct pen *p) { return p->color == INVISIBLE; }\n', no_flags=True)
    add('quoted-changelog.js', b'Versions tagged with digits (e.g. `22.74.1\'; up to 22.40, letters were used instead).\n', forbidden=[SINK])
    add('process-argument.js', b'const cp = require("child_process"); cp.exec("report.pdf\\\"; whoami");\n', [SINK])

    env = {**os.environ, 'CLEAVE_TRAITS_DIR': str(ROOT), 'SCAN_NO_ANALYSIS_CACHE': '1',
           'FILEFACTS_CACHE': '0', 'STNG_STRING_CACHE': '0', 'CLEAVE_SKIP_CACHE': '1'}
    with tempfile.TemporaryDirectory(prefix='gif-good-controls-') as temp:
        work = Path(temp)
        for name, (data, _, _, _) in cases.items():
            (work / name).write_bytes(data)
        result = subprocess.run([os.environ.get('ATOMSCAN', str(ROOT.parent / 'scan/target/release/atomscan')),
                                 '--no-update', '--analyze', 'local', '--mode', 'slow', '--follow=none',
                                 '--format=json', str(work)], capture_output=True, text=True, env=env, timeout=300)
        assert result.returncode in (0, 1), result.stderr
        assert 'could not parse' not in result.stderr and 'skipped ' not in result.stderr, result.stderr
        reports = {}
        decoder = json.JSONDecoder()
        offset = 0
        while offset < len(result.stdout):
            while offset < len(result.stdout) and result.stdout[offset].isspace():
                offset += 1
            if offset == len(result.stdout):
                break
            report, offset = decoder.raw_decode(result.stdout, offset)
            for file in report.get('raw', {}).get('files', []):
                if file.get('path', '').startswith(str(work) + '/'):
                    reports[Path(file['path']).name] = file
        checks = []
        for name, (_, required, forbidden, no_flags) in cases.items():
            assert name in reports, name
            traits = reports[name].get('traits', [])
            ids = {t['id'] for t in traits}
            flags = [t['id'] for t in traits if t.get('crit', 0) >= 4]
            checks.append({'case': name, 'missing': sorted(required - ids),
                           'unexpected': sorted(forbidden & ids),
                           'unexpected_flags': flags if no_flags else []})
        args.report.write_text(json.dumps(checks, indent=2) + '\n')
        failures = [c for c in checks if c['missing'] or c['unexpected'] or c['unexpected_flags']]
        assert not failures, json.dumps(failures, indent=2)
        print(f'{len(checks)} static GIF triage regression cases passed')


if __name__ == '__main__':
    main()
