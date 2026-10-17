#!/usr/bin/env python3
"""Check build-record placement, heading context, and module-set near misses."""
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = Path(__file__).resolve().parent
PREFIX = 'metadata/build/artifact::'
COMPOSITES = {
    'agobot3-vs6-build-log', 'rxbot-vs6-build-log',
    'rxbot-renamed-variant-build-log', 'sdbot-vs6-build-log',
}
EXPECTED = {
    'ordinary.html': {'html-build-log'},
    'results.html': {'html-build-log'},
    'comment-only.html': set(),
    'references-only.html': set(),
    'agobot.html': {'html-build-log', 'agobot3-vs6-build-log'},
    'agobot-near-miss.html': {'html-build-log'},
    'rxbot.html': {'html-build-log', 'rxbot-vs6-build-log',
                   'rxbot-renamed-variant-build-log'},
    'renamed.html': {'html-build-log', 'rxbot-renamed-variant-build-log'},
    'sdbot-overlap.html': {'html-build-log', 'sdbot-vs6-build-log'},
}


def check(report):
    decoder = json.JSONDecoder()
    files = {}
    while report.strip():
        obj, end = decoder.raw_decode(report.lstrip())
        report = report.lstrip()[end:]
        for item in obj.get('files', []):
            files[Path(item['path']).name] = item
    for name, expected in EXPECTED.items():
        traits = files[name]['traits']
        assert all(t['crit'] < 4 for t in traits), (name, 'unexpected suspicious/hostile')
        assert not any(t['id'].startswith('well-known/malware/') for t in traits), name
        actual = {t['id'][len(PREFIX):] for t in traits
                  if t['id'].startswith(PREFIX)} & (COMPOSITES | {'html-build-log'})
        assert actual == expected, (name, expected, actual)
    # A filename reference remains visible even without build-log headings.
    refs = {t['id'] for t in files['references-only.html']['traits']}
    assert PREFIX + 'mainctrl-module-reference' in refs
    assert PREFIX + 'rbot-module-reference' in refs
    print(f'{len(EXPECTED)} build-record controls passed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.report:
        output = args.report.read_text()
    else:
        output = subprocess.check_output(
            [args.cleave, '--traits-dir', str(ROOT), '--format', 'json'] +
            [str(FIXTURES / name) for name in EXPECTED], text=True)
    check(output)
