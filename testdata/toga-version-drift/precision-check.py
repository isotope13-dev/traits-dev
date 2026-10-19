#!/usr/bin/env python3
"""Exercise documentation/glob and syntax/identity boundaries outside test paths."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
GLOB = 'objectives/collection/file-targeting/filter::credential-wildcard-name-filter'
HOOK = 'metadata/lang/source/syntax::frontend-component-hook-literal'
CORE = 'metadata/lang/source/syntax::frontend-component-primitive-literal'
SYNTAX = 'metadata/lang/source/syntax::frontend-component-syntax-literal'
OLD = 'well-known/lib/web/site-platforms/package-ecosystem::has-frontend-framework'
parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
cases = [
    ('bold-login', '// 1. **Login** clears the cache.\n', set(), {GLOB, HOOK, CORE, SYNTAX}),
    ('credential-glob', "const filter = '*login*';\n", {GLOB}, {HOOK, CORE, SYNTAX}),
    ('hook-literal', "const example = 'useEffect(';\n", {HOOK}, {GLOB, CORE}),
    ('primitive-literal', "const example = 'React.createElement';\n", {CORE}, {GLOB, HOOK}),
    ('hook-call', 'useEffect(() => {});\n', set(), {GLOB, HOOK, CORE, SYNTAX}),
    ('hook-comment', '// useEffect( is mentioned here.\n', set(), {GLOB, HOOK, CORE, SYNTAX}),
]
with tempfile.TemporaryDirectory(prefix='toga-precision-', dir=args.scratch) as staging:
    for name, source, required, forbidden in cases:
        target = Path(staging) / (name + '.js')
        target.write_text(source)
        result = subprocess.run([
            os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
            '--format', 'json', str(target),
        ], text=True, capture_output=True, check=True)
        report = json.loads(result.stdout)
        traits = {t['id'] for f in report['files'] for t in f.get('traits', [])}
        assert required <= traits, (name, 'missing', required - traits)
        assert not forbidden & traits, (name, 'unexpected', forbidden & traits)
        assert not any(t.startswith(OLD) for t in traits), (name, 'retired identity')
        print(name, 'PASS')
