#!/usr/bin/env python3
"""Check neutral observations and retained attack coverage."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        value, end = decoder.raw_decode(text)
        yield from value['files']
        text = text[end:]


def main():
    cases = json.loads((HERE / 'cases.json').read_text())
    targets = [str((HERE / case['file']).resolve()) for case in cases]
    result = subprocess.run(
        ['cleave', '--traits-dir', str(ROOT), '--format', 'json', *targets],
        capture_output=True, text=True, check=True,
    )
    assert 'validation failed' not in result.stderr, result.stderr
    found = {f['path']: {t['id'] for t in f.get('traits', [])}
             for f in reports(result.stdout)}
    for case, target in zip(cases, targets):
        ids = found[target]
        for trait in case.get('present', []):
            assert trait in ids, (case['file'], 'missing', trait)
        for trait in case.get('absent', []):
            assert trait not in ids, (case['file'], 'unexpected', trait)
    print(f"PASS: {len(cases)} neutral, near-miss, and attack controls")


if __name__ == '__main__':
    main()
