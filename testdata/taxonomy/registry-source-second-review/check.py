#!/usr/bin/env python3
"""Check behavior boundaries on copies outside test-path suppressors."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        value, end = decoder.raw_decode(text)
        yield value
        text = text[end:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--traits-dir', type=Path, default=ROOT)
    parser.add_argument('--capture', type=Path)
    parser.add_argument('--capture-only', action='store_true')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='registry-review-') as td:
        directory = Path(td)
        names = []
        for source in HERE.iterdir():
            if source.suffix in {'.lnk', '.pth', '.cpp'}:
                shutil.copyfile(source, directory / source.name)
                names.append(source.name)
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir',
             str(args.traits_dir.resolve()), '--format', 'jsonl', str(directory)],
            text=True, capture_output=True, check=True)
        files = {Path(f['path']).name: f for d in documents(result.stdout)
                 for f in d['files'] if f['path'] in
                 {str(directory / name) for name in names}}
        assert set(files) == set(names), (set(files), set(names), result.stderr)
        if args.capture:
            args.capture.write_text(json.dumps(files, indent=2) + '\n')
        if args.capture_only:
            return
        for name, spec in json.loads((HERE / 'cases.json').read_text()).items():
            traits = {t['id']: t for t in files[name].get('traits', [])}
            for trait in spec.get('matched', []):
                assert trait in traits, (name, 'missing', trait)
            for trait in spec.get('not_matched', []):
                assert trait not in traits, (name, 'unexpected', trait)
            for trait, crit in spec.get('criticality', {}).items():
                assert traits[trait]['crit'] == crit, (name, trait, traits[trait])
            if spec.get('no_hostile'):
                assert all(t['crit'] < 5 for t in traits.values()), (name, traits)
        print(f'Passed {len(files)} behavior-boundary controls')


if __name__ == '__main__':
    main()
