#!/usr/bin/env python3
"""Check npm Node-script masquerade positives and ordinary-script controls."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    rule = 'objectives/evasion/masquerade/extension-mismatch::npm-script-node-non-script-suffix'
    cases = {
        # These mirror scripts found in the LaTeX extension's bundled npm
        # dependencies. Arguments and shell chaining must not make .js look
        # like a disguised non-script payload.
        'node-eval-package-json': ("node --eval 'console.log(require(\"./package.json\").version)'", False),
        'node-js-script-args': ('node Makefile.js lint', False),
        'node-js-script-shell-chain': ('node install/check.js || npm run build', False),
        'node-js-script-followed-by-command': ('node --prof test/profile.js && mv isolate.log v8.log', False),
        'ordinary-node-then-other-command': ('node scripts/build.js && npm run test', False),
        'node-json-script': ('node tools/version.json', False),
        'node-dat-payload': ('node install/update.dat', True),
        'node-dat-payload-with-options': ('node --no-warnings install/update.dat --quiet', True),
    }

    with tempfile.TemporaryDirectory(prefix='npm-masquerade-') as directory:
        paths = []
        for name, (command, expected) in cases.items():
            package = Path(directory) / name / 'package.json'
            package.parent.mkdir()
            package.write_text(json.dumps({'scripts': {'check': command}}))
            paths.append((name, package, expected))

        def check(case):
            name, path, expected = case
            result = subprocess.run([
                args.cleave, '--traits-dir', str(root), '--format', 'json', str(path),
            ], capture_output=True, text=True, check=True)
            traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
            found = [t for t in traits if t['id'] == rule]
            assert bool(found) == expected, (name, expected, found)
            assert all(t['crit'] == 4 for t in found)
            return name + ': passed'

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            for message in pool.map(check, paths):
                print(message, flush=True)


if __name__ == '__main__':
    main()
