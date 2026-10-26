"""Run static detection controls; never execute the JavaScript fixtures.

Usage: python3 testdata/browser-stored-code/verify.py SAMPLE_DIR CLEAVE_FIXTURE_DIR
SAMPLE_DIR contains suspicious/{october-cms-loader.js,march-cms-loader.js,
renamed-loader.ts,decoded-renamed-loader.js}; controls live in cleave's fixtures.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SYNTHETIC = 'objectives/anti-static/obfuscation/eval/browser::synthetic-click-code-evaluation'
REPLAY = 'objectives/execution/payload/script-eval::web-storage-event-code-replay'
OLD = 'objectives/command-and-control/dropper/script-eval/response-eval/http::dist-tail-injects-encoded-remote-script'


def main():
    samples, controls = (Path(arg).resolve() for arg in sys.argv[1:])
    expected = {
        samples / 'suspicious' / name: {SYNTHETIC, REPLAY}
        for name in ('october-cms-loader.js', 'march-cms-loader.js',
                     'renamed-loader.ts', 'decoded-renamed-loader.js')
    }
    for name in ('preferences.js', 'ordinary-click.js', 'static-handler.js',
                 'unrelated-click.js', 'comments.js', 'reassigned-element.js',
                 'ordinary-encoded-loader.js', 'cached-without-trigger.js'):
        expected[controls / name] = set()
    for name in ('unrelated-storage.js', 'shadowed-storage.js'):
        expected[controls / name] = {SYNTHETIC}
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', *map(str, expected)],
        check=True, text=True, capture_output=True,
    )
    decoder, output, seen = json.JSONDecoder(), result.stdout.strip(), set()
    while output:
        report, consumed = decoder.raw_decode(output)
        output = output[consumed:].lstrip()
        for file in report['files']:
            path = Path(file['path']).resolve()
            ids = {trait['id'] for trait in file['traits']}
            actual = ids & {SYNTHETIC, REPLAY}
            assert actual == expected[path], (path, actual, expected[path])
            assert OLD not in ids, (path, 'unsupported bundle-tail verdict')
            seen.add(path)
    assert seen == set(expected), ('missing reports', set(expected) - seen)
    print(f'{len(seen)} static cases passed: 4 supported samples, 10 controls')


if __name__ == '__main__':
    main()
