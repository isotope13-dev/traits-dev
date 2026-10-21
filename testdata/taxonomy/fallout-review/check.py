#!/usr/bin/env python3
"""Check placement observations and unchanged consumers without running fixtures."""
import argparse
import json
from pathlib import Path
import subprocess
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--baseline-dir', type=Path)
args = parser.parse_args()

ALIAS = 'metadata/import/builtin::alias-'
GET = 'micro-behaviors/communications/http/get::requests-get'
FALLBACK = 'micro-behaviors/communications/http/lib/requests::requests-get-text'
PARAMS = 'metadata/lang/source/naming/setting::litellm-params-key'
LIBRARY = 'well-known/lib/ai/litellm::litellm-codebase'
RAW = 'micro-behaviors/communications/http/client/service::github-raw-python-client-cooccurrence'
DISCORD = 'objectives/command-and-control/dropper/delivery/cdn::discord-dropper-generic'
CASES = {
    'aliased.py': ([ALIAS + n for n in ('os', 'subprocess', 'base64', 'platform', 'getpass', 'urllib')], []),
    'plain.py': ([], [ALIAS + n for n in ('os', 'subprocess', 'base64', 'platform', 'getpass', 'urllib')]),
    'private.py': ([], [ALIAS + 'os']),
    'quoted-alias.py': ([], [ALIAS + 'base64']),
    'github-reference.py': ([], [GET, RAW]),
    'github-unrelated-request.py': ([GET, RAW], []),
    'setting.py': ([PARAMS], [LIBRARY]),
    'library.py': ([PARAMS, LIBRARY], []),
    'get.py': ([GET], [FALLBACK]),
    'get-prose.py': ([FALLBACK], [GET]),
    'github-client.py': ([GET, RAW], []),
    'discord-chain.py': ([GET, DISCORD], []),
    'discord-post-only.py': ([], [GET, DISCORD]),
}
ID_MAP = {'micro-behaviors/data/source/import::alias-' + n: ALIAS + n
          for n in ('os', 'subprocess', 'base64', 'platform', 'getpass', 'urllib')}
ID_MAP.update({
    'well-known/lib/ai/litellm::litellm-params-key': PARAMS,
    'micro-behaviors/communications/http/lib/requests::requests-get': GET,
    'micro-behaviors/communications/http/download/github::github-raw-python-fetch': RAW,
})

def scan(traits):
    # Copy controls out of testdata so a test-directory exclusion cannot mask
    # the client/URL observation being tested. Basenames and bytes are retained.
    with tempfile.TemporaryDirectory(prefix='fallout-controls-', dir=ROOT) as folder:
        targets = []
        for name in CASES:
            target = Path(folder) / name
            shutil.copyfile(HERE / name, target)
            targets.append(str(target))
        result = subprocess.run([args.cleave, '--traits-dir', str(traits),
                                 '--format', 'jsonl', 'analyze', *targets],
                                check=True, capture_output=True, text=True)
        return {Path(f['path']).name: {t['id']: t['crit'] for t in f.get('traits', [])}
                for line in result.stdout.splitlines() if line.strip()
                for f in json.loads(line).get('files', [])}

current = scan(ROOT)
for name, (required, forbidden) in CASES.items():
    traits = current[name]
    assert set(required) <= traits.keys(), (name, 'missing', set(required) - traits.keys())
    assert not set(forbidden) & traits.keys(), (name, 'unexpected', set(forbidden) & traits.keys())
    assert not ID_MAP.keys() & traits.keys(), (name, 'retired ID still emitted')
if args.baseline_dir:
    baseline = scan(args.baseline_dir)
    for name, traits in baseline.items():
        normalized = {ID_MAP.get(key, key): value for key, value in traits.items()}
        assert normalized == current[name], (name, 'placement changed detection',
                                             normalized.keys() - current[name].keys(),
                                             current[name].keys() - normalized.keys())
print(f'{len(CASES)} placement and consumer cases passed' +
      ('; identical findings after ID mapping' if args.baseline_dir else ''))
