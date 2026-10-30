#!/usr/bin/env python3
"""Regress native PNG pixel reconstruction using synthetic and real-CLI fixtures."""
import argparse
import json
import lzma
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'objectives/anti-static/obfuscation/steganography/image::png-pixel-'
RULES = {kind: PREFIX + 'script' for kind in ['shell', 'python', 'javascript', 'powershell']}
RULES.update({'elf': PREFIX + 'executable', 'elf-header': PREFIX + 'executable-header',
              'zip': PREFIX + 'archive', 'json': PREFIX + 'json', 'url': PREFIX + 'url'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--atomscan', default=os.environ.get('ATOMSCAN', str(ROOT.parent / 'scan/target/debug/atomscan')))
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--write-fixtures', action='store_true')
    args = parser.parse_args()
    env = {**os.environ, 'CLEAVE_TRAITS_DIR': str(ROOT), 'SCAN_NO_ANALYSIS_CACHE': '1', 'CLEAVE_SKIP_CACHE': '1'}
    with tempfile.TemporaryDirectory(prefix='png-native-') as temp:
        work = Path(temp)
        source = work / 'source'
        subprocess.run([sys.executable, str(ROOT / 'scripts/fixture-builders/make-png-stego-controls.py'),
                        '--out-dir', str(source)], check=True, capture_output=True)
        cases = json.loads((source / 'manifest.json').read_text())['cases']
        # Retained fixtures produced by stegano-lsb 3.0.0, independently
        # extracted with zsteg. They test an implementation other than ours.
        # They are parked with the other pixel-payload carriers until an
        # engine with pixel reconstruction ships; see that directory's README.
        for name in ['stegano-sequential.png', 'stegano-prime.png']:
            path = ROOT / 'docs/taxonomy-audit/triage/png-bad-20261030/fixtures' / name
            assert path.exists(), path
            cases.append(dict(path=str(path), expected_kind='shell', expected_max_crit=4))
        scan_dir = work / 'images'
        scan_dir.mkdir()
        expected = {}
        for index, case in enumerate(cases):
            original = Path(case['path'])
            path = scan_dir / f'asset{index:03d}.png'
            shutil.copy2(original, path)
            expected[path.name] = {**case, 'case': original.name}
            if args.write_fixtures and not original.name.startswith('stegano-'):
                kind = case['expected_kind']
                classification = 'baseline' if kind is None else 'hostile' if kind == 'elf' else 'suspicious'
                dest = ROOT / 'testdata' / classification / 'generated/taxonomy/png-pixel-stego' / original.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                data = original.read_bytes()
                if len(data) > 20 * 1024:
                    dest.with_name(dest.name + '.xz').write_bytes(lzma.compress(data))
                else:
                    dest.write_bytes(data)
        start = time.monotonic()
        run = subprocess.run([args.atomscan, '--no-update', '--analyze=local', '--mode=slow',
                              '--follow=none', '--format=json', str(scan_dir)], env=env,
                             capture_output=True, text=True, timeout=300)
        elapsed = time.monotonic() - start
        assert run.returncode in (0, 1), run.stderr
        assert 'could not parse' not in run.stderr and 'skipped trait' not in run.stderr, run.stderr
        reports = {}
        for line in run.stdout.split('\n'):
            if line.strip():
                for file in json.loads(line).get('raw', {}).get('files', []):
                    reports[Path(file['path']).name] = file
        checks = []
        for name, case in expected.items():
            assert name in reports, name
            findings = reports[name].get('traits', [])
            flags = [t for t in findings if t['crit'] >= 4]
            kind = case['expected_kind']
            wanted = RULES.get(kind)
            level = 5 if kind == 'elf' else 4
            matched = next((t for t in findings if t['id'] == wanted), None)
            reconstructed = any(t['id'] == 'metadata/image/pixel::png-reconstructed-pixel-payload' for t in findings)
            checks.append(dict(case=case['case'], expected_kind=kind,
                               passed=(not flags if kind is None else reconstructed and matched is not None and matched['crit'] == level)
                                      and all(t['crit'] <= case['expected_max_crit'] for t in flags),
                               flags=flags, findings=findings))
        result = dict(cases=len(checks), passed=sum(c['passed'] for c in checks), elapsed_seconds=round(elapsed, 3),
                      atomscan=args.atomscan, checks=checks, stderr=run.stderr)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
        failures = [c for c in checks if not c['passed']]
        assert not failures, json.dumps(failures, indent=2)
        print(f'{len(checks)} native PNG pixel-payload cases passed in {elapsed:.2f}s')


if __name__ == '__main__':
    main()
