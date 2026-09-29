#!/usr/bin/env python3
"""Check the email clipboard capability on source and static controls."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    fixtures = root / 'testdata/taxonomy/vscode-dns-tasking'
    source_path = fixtures / 'email-grabber-extension.js'
    digest = json.loads((fixtures / 'sha256.json').read_text())[source_path.name]
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == digest
    rule = 'micro-behaviors/os/clipboard/write::email-list-clipboard-write'
    cases = [
        ('original-extension', source_path, True),
        ('direct-list-export', None, True),
        ('comment-only', None, False),
        ('string-only', None, False),
        ('different-data', None, False),
    ]
    sources = {
        'direct-list-export': "const emailList = emails.join('\\n'); vscode.env.clipboard.writeText(emailList);\n",
        'comment-only': "// emailList is sent with vscode.env.clipboard.writeText(emailList)\nconst value = 1;\n",
        'string-only': "const docs = 'emailList vscode.env.clipboard.writeText(emailList)';\n",
        'different-data': "const emailList = emails.join('\\n'); vscode.env.clipboard.writeText(themeName);\n",
    }
    with tempfile.TemporaryDirectory(prefix='vscode-email-clipboard-') as directory:
        temporary = Path(directory)
        paths = []
        for name, path, expected in cases:
            if path is None:
                path = temporary / (name + '.js')
                path.write_text(sources[name])
            paths.append((name, path, expected))

        def check(case):
            name, path, expected = case
            result = subprocess.run([
                args.cleave, '--traits-dir', str(root), '--format', 'json', str(path),
            ], capture_output=True, text=True, check=True)
            traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
            found = [t for t in traits if t['id'] == rule]
            assert bool(found) == expected, (name, expected, found)
            assert all(t['crit'] == 3 for t in found), (name, found)
            assert all('T1114' not in t.get('atk', '') for t in found)
            return name + ': passed'

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            for message in pool.map(check, paths):
                print(message, flush=True)


if __name__ == '__main__':
    main()
