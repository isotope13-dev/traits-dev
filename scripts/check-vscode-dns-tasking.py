#!/usr/bin/env python3
"""Scan retained and synthetic controls without running extension code."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    fixtures = root / 'testdata/taxonomy/vscode-dns-tasking'
    for name, digest in json.loads((fixtures / 'sha256.json').read_text()).items():
        assert hashlib.sha256((fixtures / name).read_bytes()).hexdigest() == digest, name
    rule = 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-bundled-dns-code-execution'
    old = 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-dns-bitmask-collection'
    original = fixtures / 'email-grabber-original.vsix'
    with zipfile.ZipFile(original) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
    source = members['extension/run.js']
    assert source.count(b'eval(receivedCmd)') == 1
    assert source.count(b'.resolveTxt(') == 1
    without_eval = source.replace(b'eval(receivedCmd)', b'String(receivedCmd)')
    with tempfile.TemporaryDirectory(prefix='vscode-dns-controls-') as directory:
        folder = Path(directory)
        cases = [(original, True)]

        def archive_case(name, contents, expected):
            path = folder / (name + '.vsix')
            with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
                for member, data in contents.items():
                    archive.writestr(member, data)
            cases.append((path, expected))

        archive_case('no-eval', {**members, 'extension/run.js': without_eval}, False)
        archive_case('no-txt', {**members, 'extension/run.js': source.replace(b'.resolveTxt(', b'.resolve4(')}, False)
        archive_case('split-evidence', {
            **members, 'extension/run.js': without_eval,
            'extension/other.js': b'exports.evaluate = value => eval(value);\n',
        }, False)
        archive_case('unrelated-dependencies', {
            'extension/package.json': json.dumps({
                'name': 'document-helper', 'version': '1.0.0', 'publisher': 'control',
                'engines': {'vscode': '^1.89.0'}, 'main': './extension.js',
                'activationEvents': ['onStartupFinished'],
            }),
            'extension/extension.js': b"const vscode = require('vscode'); exports.activate = () => {};\n",
            **{'extension/node_modules/control/' + name: (fixtures / name).read_bytes()
               for name in ['proxy-dns.js', 'stream-hex-test.js', 'flate-stream.js']},
        }, False)
        standalone = folder / 'run.js'
        standalone.write_bytes(source)
        cases.append((standalone, False))

        def check(case):
            path, expected = case
            result = subprocess.run([
                args.cleave, '--traits-dir', str(root), '--format', 'json', str(path),
            ], capture_output=True, text=True, check=True)
            traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
            found = [t for t in traits if t['id'] == rule]
            assert bool(found) == expected, (path.name, expected, found)
            assert all(t['crit'] == 5 for t in found)
            assert not any(t['id'] == old for t in traits)
            return path.name + ': passed'

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            for message in pool.map(check, cases):
                print(message, flush=True)


if __name__ == '__main__':
    main()
