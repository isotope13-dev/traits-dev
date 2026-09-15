#!/usr/bin/env python3
"""Static regressions for opaque manifest data and false clone evidence."""
import base64
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CONFIG = 'metadata/package/config::npm-base64-tag-command-tables'
CLONE = 'objectives/supply-chain/impersonation/npm-clone::big-js-clone-lint-builder-dependency'
RECONSTRUCT = 'objectives/anti-static/obfuscation/string/reconstruct::js-string-deobfuscation'


def opaque(seed, size):
    return hashlib.shake_256(seed.encode()).digest(size)


def main():
    base = {'name': 'arithmetic-fork', 'version': '1.2.3',
            'repository': {'url': 'https://github.com/MikeMcl/big.js.git'},
            'author': {'name': 'Upstream author', 'email': 'upstream@gmail.com'}}
    tags = [base64.b64encode(opaque(str(i), 16)).decode() for i in range(6)]
    command = base64.b64encode(opaque('command', 96)).decode()
    configs = {
        'paired': {'tags': tags, 'cmds': [command]},
        'urlsafe': {'tags': [base64.urlsafe_b64encode(opaque(str(i), 32)).decode().rstrip('=')
                             for i in range(6)],
                    'cmds': [base64.urlsafe_b64encode(opaque('alternate', 96)).decode()]},
        'tags-only': {'tags': tags},
        'commands-only': {'cmds': [command]},
        'few-tags': {'tags': tags[:3], 'cmds': [command]},
        'ordinary': {'tags': ['release', 'arithmetic', 'decimal', 'library'], 'cmds': ['node build.js']},
        'invalid': {'tags': [s + '!' for s in tags], 'cmds': [command]},
        'wrong-type': {'tags': {'0': tags[0]}, 'cmds': command},
    }
    with tempfile.TemporaryDirectory(prefix='npm-opaque-config-') as tmp:
        root = Path(tmp)
        paths = []
        for name, config in configs.items():
            manifest = dict(base, config=config)
            path = root / name / 'package.json'
            path.parent.mkdir()
            path.write_text(json.dumps(manifest, indent=2))
            paths.append(path)
        for name in ['fork', 'upstream', 'payload-dependency', 'repository-credit']:
            manifest = copy.deepcopy(base)
            if name == 'upstream':
                manifest['name'] = 'big.js'
            elif name == 'payload-dependency':
                manifest['dependencies'] = {'lint-builder': '1.0.0'}
            elif name == 'repository-credit':
                manifest['repository']['url'] = 'https://github.com/zerorooot/project.git'
            path = root / name / 'package.json'
            path.parent.mkdir()
            path.write_text(json.dumps(manifest, indent=2))
            paths.append(path)
        js = {
            'arithmetic': 'function format(n) { const a = n.split(""); a.reverse(); a.push(n.charAt(0)); return a.join(""); }',
            'encoded': 'const parts = [' + ','.join('"' + r'\x61\x62\x63\x64' + '"' for _ in range(5)) + ']; const message = parts.join("");',
        }
        for name, source in js.items():
            path = root / name / 'index.js'
            path.parent.mkdir()
            path.write_text(source)
            paths.append(path)
        result = subprocess.run([
            os.environ.get('ATOMSCAN', 'atomscan'), '--no-update', '--mode', 'slow',
            '--follow=none', '--format', 'json', 'path', *map(str, paths)],
            cwd=ROOT, env=dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), CLEAVE_ANALYSIS_MEMO_MB='0'),
            text=True, capture_output=True)
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)
        reports = []
        remaining = result.stdout.strip()
        while remaining:
            report, end = json.JSONDecoder().raw_decode(remaining)
            reports.append(report)
            remaining = remaining[end:].lstrip()
        assert len(reports) == len(paths), (len(reports), len(paths), result.stderr)
        for report in reports:
            path = Path(report['raw']['files'][0]['path'])
            name = path.parent.name
            traits = {t['id']: t['crit'] for f in report['raw']['files'] for t in f.get('traits', [])}
            assert (CONFIG in traits) == (name in {'paired', 'urlsafe', 'few-tags'}), (name, traits)
            assert (CLONE in traits) == (name == 'payload-dependency'), (name, traits)
            assert (RECONSTRUCT in traits) == (name == 'encoded'), (name, traits)
            if name != 'payload-dependency':
                assert all(c < 5 for c in traits.values()), (name, traits)
            if name in {'upstream', 'repository-credit', 'arithmetic'}:
                assert all(c < 4 for c in traits.values()), (name, traits)
        print(f'Passed {len(paths)} static manifest and JavaScript controls')


if __name__ == '__main__':
    main()
