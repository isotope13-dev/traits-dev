"""Check the provider, source-comment and protobuf behavior boundaries."""
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def objects(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        obj, end = decoder.raw_decode(text)
        yield obj
        text = text[end:]


def check(cases_path):
    scan = subprocess.run(
        ['cleave', '--traits-dir', str(ROOT), '--format', 'json', str(cases_path.parent)],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    if scan.stderr.strip():
        raise AssertionError(scan.stderr)
    reports = {
        Path(report['path']).name: report
        for obj in objects(scan.stdout)
        for report in obj.get('files', [obj])
        if 'path' in report
    }
    for case in json.loads(cases_path.read_text())['fixtures']:
        name = Path(case['path']).name
        matched = {trait['id'] for trait in reports[name].get('traits', [])}
        missing = set(case.get('matched', [])) - matched
        unexpected = set(case.get('not_matched', [])) & matched
        assert not missing and not unexpected, (name, missing, unexpected)
        print(f'PASS {name}')


if __name__ == '__main__':
    check(HERE / 'cases.json')
    check(HERE.parent / 'logging-field-stem' / 'cases.json')
