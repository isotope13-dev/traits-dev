"""Static rule controls. Never execute or load the supplied binaries.

Usage: python3 check.py SAMPLE_ELF STOCK_XMRIG SCRATCH_DIR
The stock control is the original upstream XMRig 6.24.0 static x64 release.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
WRAP = 'objectives/evasion/hijack-execution-flow/wrapper::crontab-concealment-and-removal-resistance'
CRON = 'objectives/persistence/system/cron/job::concealed-crontab-recurring-relaunch'
UNIT = 'objectives/persistence/system/service/systemd::cron-concealing-implant-systemd-unit'
PACKAGE = 'objectives/evasion/indicator-removal/logs::package-log-removal'
WIPE = 'objectives/evasion/indicator-removal/logs::native-history-and-package-log-wipe'
TEMP = 'micro-behaviors/fs/delete/file/command::apt-yum-named-temp-file-removal'
HELPER = 'micro-behaviors/os/service/config::system-helper-service-path'
OLD_HELPER = 'objectives/evasion/masquerade/identity/service::system-helper-service-path'
KILL = 'objectives/evasion/hijack-execution-flow/wrapper::kill-function-discards-sigkill'


def main():
    sample, stock, scratch = map(Path, sys.argv[1:])
    work = scratch / 'controls'
    work.mkdir(parents=True, exist_ok=True)
    data = sample.read_bytes()
    clean = stock.read_bytes()
    assert hashlib.sha256(clean).hexdigest() == '0c748b9e8bc6b5b4fe989df67655f3301d28ef81617b9cbe8e0f6a19d4f9b657'
    cases = {}

    def emit(name, content, expected):
        (work / name).write_bytes(content)
        cases[name] = expected

    positive = {WRAP: True, CRON: True, UNIT: True, PACKAGE: False,
                WIPE: False, TEMP: True, HELPER: True, OLD_HELPER: False, KILL: True}
    emit('reviewed.elf', data, positive)
    for name, before, after in [
        ('visible-listing.elf', b'grep -v', b'grep -x'),
        ('no-remove-interception.elf', b'--remove', b'--other!'),
        ('no-reinstall.elf', b'| command crontab -; else command crontab -r;', b'| command crontab -r; else command crontab -r;'),
    ]:
        assert before in data
        expected = {**positive, WRAP: False, CRON: False, UNIT: False}
        emit(name, data.replace(before, after), expected)
    renamed = data.replace(b'snap', b'news').replace(b'.X0-lock', b'.YY-lock')
    renamed = renamed.replace(b'system-helper', b'daemon-helper')
    emit('renamed-targets.elf', renamed, {**positive, HELPER: False})
    emit('upstream-xmrig.elf', clean,
         {WRAP: False, CRON: False, UNIT: False, PACKAGE: False, WIPE: False})
    emit('real-package-logs.elf', clean + b'\0rm -f "$HOME/.bash_history" /var/log/apt/history.log /var/log/yum.log\0',
         {PACKAGE: True, WIPE: True, TEMP: False, WRAP: False})
    emit('temporary-names.elf', clean + b'\0rm -f /var/tmp/apt.log /var/tmp/yum.log\0',
         {PACKAGE: False, WIPE: False, TEMP: True, WRAP: False})
    emit('package-path-only.elf', clean + b'\0/var/log/apt/history.log\0',
         {PACKAGE: False, WIPE: False, TEMP: False})
    emit('different-command.elf', clean + b'\0rm -f /tmp/old; cat /var/log/yum.log\0',
         {PACKAGE: False, WIPE: False})
    emit('helper-path-only.elf', clean + b'\0/etc/systemd/system/system-helper.service\0',
         {HELPER: True, OLD_HELPER: False, WRAP: False, UNIT: False})
    emit('filtered-list-only.sh', b'#!/bin/bash\ncrontab() { command crontab -l 2>/dev/null | grep -v "$p"; }\n',
         {WRAP: False})
    emit('normal-remove.sh', b'#!/bin/bash\ncrontab() { command crontab "$@"; }\n',
         {WRAP: False})
    emit('ordinary-kill-wrapper.sh', b'#!/bin/bash\nkill() { command kill "$@"; }\n',
         {KILL: False})
    proc = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'jsonl', str(work)],
                          text=True, capture_output=True, check=True)
    (scratch / 'controls.jsonl').write_text(proc.stdout)
    (scratch / 'controls.stderr').write_text(proc.stderr)
    found = {}
    for line in proc.stdout.splitlines():
        report = json.loads(line)
        for entry in report['files']:
            name = Path(entry['path']).name
            if name not in cases:
                continue
            traits = {t['id']: t for t in entry['traits']}
            for trait, present in cases[name].items():
                assert (trait in traits) == present, (name, trait, present)
            if HELPER in traits:
                assert traits[HELPER]['crit'] == 3
            if TEMP in traits:
                assert traits[TEMP]['crit'] == 3
            found[name] = {'expected': cases[name], 'passed': True}
    assert set(found) == set(cases), sorted(set(cases) - set(found))
    (scratch / 'control-results.json').write_text(json.dumps(found, indent=2) + '\n')
    print(f'PASS: {len(found)} static positive, upstream and near-miss controls')


if __name__ == '__main__':
    main()
