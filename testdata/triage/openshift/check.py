#!/usr/bin/env python3
"""Run content controls outside test paths so path exclusions cannot mask failures."""
import json
import pathlib
import shutil
import subprocess
import tempfile

here = pathlib.Path(__file__).resolve().parent
root = here.parents[2]
cases = json.loads((here / 'cases.json').read_text())['fixtures']
with tempfile.TemporaryDirectory(prefix='ci-trait-controls-') as tmp:
    for case in cases:
        shutil.copyfile(root / case['path'], pathlib.Path(tmp) / pathlib.Path(case['path']).name)
    result = subprocess.run(['cleave', '--traits-dir', str(root), '--format', 'json', tmp],
                            text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    if 'warning' in result.stderr.lower() or 'validation failed' in result.stderr.lower():
        raise AssertionError(result.stderr)
    remaining = result.stdout
    decoder = json.JSONDecoder()
    findings = {}
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        for file in report['files']:
            findings[pathlib.Path(file['path']).name] = {trait['id'] for trait in file.get('traits', [])}
    for case in cases:
        ids = findings[pathlib.Path(case['path']).name]
        missing = set(case['matched']) - ids
        unexpected = set(case['not_matched']) & ids
        assert not missing and not unexpected, (case['path'], missing, unexpected)
print(f'{len(cases)} content controls passed')
