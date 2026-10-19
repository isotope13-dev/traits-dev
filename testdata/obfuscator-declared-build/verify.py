"""A declared obfuscator build downgrades the plain-name runtime.

Run: python3 testdata/obfuscator-declared-build/verify.py <scratch-dir>

A commercial CLI that declares `javascript-obfuscator` as a
devDependency and builds through its own wrapper script
(`scripts/build.ts`, with a `--no-mangle` sibling) ships a plain-name
string-array runtime on purpose: the finding stays notable, not
suspicious. The same runtime with no declared build stays suspicious.

Packages are staged in the scratch directory because the context only
pools at archive/package scope.
"""
import json
import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TRAIT = ('objectives/anti-static/obfuscation/obfuscator/js-obfuscator::'
         'plain-javascript-obfuscator-string-array-runtime')

MANIFEST = {
    "name": "declared-build-controls",
    "version": "1.0.0",
    "scripts": {"build": "node --experimental-strip-types scripts/build.ts",
                "build:no-mangle": "node scripts/build.ts --no-mangle"},
    "devDependencies": {"javascript-obfuscator": "^5.6.0"},
}


def scan(path):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'),
        text=True, capture_output=True, check=True)
    decoder = json.JSONDecoder()
    output = result.stdout
    hits = []
    while output.strip():
        report, end = decoder.raw_decode(output.lstrip())
        output = output.lstrip()[end:]
        hits.extend(t for entry in report['files']
                    for t in entry.get('traits', []) if t['id'] == TRAIT)
    return hits


def stage(dest: Path, declared: bool):
    pkg = dest / 'package'
    (pkg / 'dist').mkdir(parents=True, exist_ok=True)
    manifest = dict(MANIFEST)
    if not declared:
        manifest.pop('devDependencies')
    (pkg / 'package.json').write_text(json.dumps(manifest, indent=2))
    shutil.copyfile(HERE / 'dist-index.js', pkg / 'dist' / 'index.js')
    archive = dest.with_suffix('.tgz')
    with tarfile.open(archive, 'w:gz') as tf:
        tf.add(pkg, arcname='package')
    return archive


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)

    declared = stage(dest / 'declared', declared=True)
    hits = scan(declared)
    assert hits and all(t['crit'] < 4 for t in hits), hits
    print('PASS declared', flush=True)

    undeclared = stage(dest / 'undeclared', declared=False)
    hits = scan(undeclared)
    assert hits and any(t['crit'] >= 4 for t in hits), hits
    print('PASS undeclared', flush=True)


if __name__ == '__main__':
    main()
