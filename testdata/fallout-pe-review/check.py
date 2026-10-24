"""Static controls for IFEO, recurring tasks and source/trigger placement.

Usage: python3 testdata/fallout-pe-review/check.py SAMPLE SCRATCH
Mutations are never executed. Original CLR structure is retained so controls
exercise the actual binary matchers, rather than treating string stubs as CIL.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OLD = 'objectives/exfiltration/stealer/multi-source::managed-keylog-records-with-http-upload'
INPUT = 'objectives/exfiltration/stealer/input::managed-keylog-records-with-http-upload'
IFEO = 'objectives/impact/degrade/process::managed-keylogger-ifeo-tool-hijack-profile'
TASK = 'objectives/persistence/system/scheduled-task::managed-keylogger-recurring-task-profile'
SCHEDULE = 'micro-behaviors/os/autorun/task-trigger::schtasks-minute-or-hourly-option'
OLD_SCHEDULE = 'micro-behaviors/os/autorun/scheduled::schtasks-short-repeat-schedule'


def main():
    sample, scratch = map(Path, sys.argv[1:])
    scratch.mkdir(parents=True, exist_ok=True)
    data = sample.read_bytes()

    def replace_ascii(blob, old, new):
        assert len(old) == len(new)
        assert old.encode() in blob
        return blob.replace(old.encode(), new.encode())

    def replace_wide(blob, old, new):
        assert len(old) == len(new)
        assert old.encode('utf-16le') in blob
        return blob.replace(old.encode('utf-16le'), new.encode('utf-16le'))

    cases = [
        ('renamed.exe', data, True, True, True),
        ('no-ifeo.exe', replace_wide(data, 'Image File Execution Options',
                                   'Image File Inspection Tables'), False, True, True),
        ('no-key-create.exe', replace_ascii(data, 'CreateSubKey', 'InspectKey__'), False, True, True),
        ('no-keylogger.exe', replace_ascii(replace_wide(data, 'keylogger', 'eventloop'),
                                           'StartKeylogger', 'StartEventloop'), False, False, False),
        ('no-http-upload.exe', replace_ascii(data, 'UploadString', 'InspectValue'), True, False, True),
        ('no-repeat.exe', replace_wide(data, '/sc minute /mo 30', '/sc onidle /mo 30'), True, True, False),
    ]
    results = []
    for name, blob, ifeo, uploaded, task in cases:
        target = scratch / name
        target.write_bytes(blob)
        report = json.loads(subprocess.check_output([
            os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
            '--disable', 'third-party', '--format', 'json', str(target)]))
        traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
        assert OLD not in traits, name
        assert (INPUT in traits) == uploaded, (name, 'input profile')
        assert (IFEO in traits) == ifeo, (name, 'IFEO profile')
        assert (TASK in traits) == task, (name, 'recurring-task profile')
        for trait in (INPUT, IFEO, TASK):
            if trait in traits:
                assert traits[trait]['crit'] == 5, (name, trait)
        results.append({'case': name, 'ifeo': ifeo, 'input_profile': uploaded, 'recurring_task': task, 'passed': True})
        print('PASS', name, flush=True)
    # A benign fixture with inert keylogging/dropper API references must not
    # acquire an objective merely by naming IFEO or a keyboard API.
    benign = ROOT / 'testdata/benign/keylog-dropper-controls.exe'
    report = json.loads(subprocess.check_output([
        os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
        '--disable', 'third-party', '--format', 'json', str(benign)]))
    ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    assert not {INPUT, IFEO, TASK, OLD} & ids
    results.append({'case': str(benign.relative_to(ROOT)), 'passed': True})
    print('PASS', benign.name, flush=True)
    # A schedule type remains the same observation with /MO 1, 30 or 999;
    # it does not prove a short repetition interval or hostile persistence.
    for name, command, expected in [
        ('minute.ps1', 'schtasks /create /tn Maintenance /sc minute /mo 30', True),
        ('hourly.ps1', 'schtasks /create /tn Maintenance /sc hourly /mo 999', True),
        ('argv.py', 'args = ["/sc", "minute", "/mo", "30"]', True),
        ('daily.ps1', 'schtasks /create /tn Maintenance /sc daily /mo 1', False),
    ]:
        target = scratch / name
        target.write_text(command + '\n')
        report = json.loads(subprocess.check_output([
            os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
            '--disable', 'third-party', '--format', 'json', str(target)]))
        ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
        assert (SCHEDULE in ids) == expected, name
        assert not {OLD_SCHEDULE, INPUT, IFEO, TASK} & ids, name
        results.append({'case': name, 'schedule_option': expected, 'passed': True})
        print('PASS', name, flush=True)
    (scratch / 'control-results.json').write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
