#!/usr/bin/env python3
"""Check wording, bundle-property boundaries, and retained attack coverage."""
import argparse
import json
import pathlib
import plistlib
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--scratch', required=True)
args = parser.parse_args()
base = pathlib.Path(__file__).resolve().parent
cases = json.loads((base / 'cases.json').read_text())['fixtures']
property_id = 'metadata/binary/bundle::executable-plist-missing-identity-fields'
chrome_sparse_id = 'metadata/binary/bundle::chrome-executable-missing-identity-fields'
chrome_id = 'metadata/binary/bundle::chrome-executable-without-google-id-prefix'
retired_ids = {
    'objectives/evasion/masquerade/brand/product::stub-chrome-brand-bundle',
    'objectives/evasion/masquerade/brand/product::macos-brand-confusion-chrome',
}
with tempfile.TemporaryDirectory(prefix='bundle-observations-', dir=args.scratch) as tmp:
    layouts = {
        'chrome': {'CFBundleExecutable': 'Chrome', 'CFBundleIconFile': 'icon.icns'},
        'renamed': {'CFBundleExecutable': 'Utility', 'CFBundleIconFile': 'icon.icns'},
        'extra-key': {'CFBundleExecutable': 'Utility', 'CFBundleName': 'Utility', 'NSHighResolutionCapable': True},
        'identified': {'CFBundleExecutable': 'Chrome', 'CFBundleIdentifier': 'com.google.Chrome', 'CFBundleVersion': '1', 'CFBundlePackageType': 'APPL'},
        'custom-id': {'CFBundleExecutable': 'Chrome', 'CFBundleIdentifier': 'org.example.browser-wrapper'},
        'official-child-id': {'CFBundleExecutable': 'Chrome', 'CFBundleIdentifier': 'com.google.Chrome.beta'},
    }
    for name, fields in layouts.items():
        path = pathlib.Path(tmp) / name / 'Info.plist'
        path.parent.mkdir()
        path.write_bytes(plistlib.dumps(fields))
        expected = {
            property_id: name in {'chrome', 'renamed', 'extra-key'},
            chrome_sparse_id: name == 'chrome',
            chrome_id: name in {'chrome', 'custom-id'},
        }
        cases.append({'path': str(path), 'matched': [t for t, matched in expected.items() if matched], 'not_matched': [t for t, matched in expected.items() if not matched] + sorted(retired_ids)})
    proc = subprocess.run([args.cleave, '--format', 'jsonl', *[c['path'] for c in cases]], check=True, capture_output=True, text=True)
    files = [f for line in proc.stdout.splitlines() for f in json.loads(line)['files']]
    for case in cases:
        report = next(f for f in files if f['path'] == case['path'])
        traits = {t['id'] for t in report.get('traits', [])}
        missing = set(case['matched']) - traits
        unexpected = set(case['not_matched']) & traits
        assert not missing | unexpected, (case['path'], missing, unexpected)
        for trait in report.get('traits', []):
            if trait['id'] in {chrome_sparse_id, chrome_id}:
                assert trait['crit'] in (3, 'notable'), trait
        print('PASS', case['path'])
