"""Check collected, unpacked PE bytes and missing-role variants, never execute."""
import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
TASK = 'objectives/persistence/system/scheduled-task::go-credential-stealer-timed-task-profile'
THEFT = 'objectives/credential-access/browser/chromium::go-browser-login-query-with-keylogging'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('unpacked', type=Path)
    parser.add_argument('scratch', type=Path)
    args = parser.parse_args()
    data = args.unpacked.read_bytes()
    args.scratch.mkdir(parents=True, exist_ok=True)
    old = b'github.com/capnspacehook/taskmaster.(*TaskService).CreateTask'
    assert old in data and b'TimeTrigger' in data
    variants = {
        'task-present': data,
        'no-creation': data.replace(old, old.replace(b'CreateTask', b'InspectJob')),
        'no-time-trigger': data.replace(b'TimeTrigger', b'TypeTrigger'),
    }
    paths = []
    for name, contents in variants.items():
        path = args.scratch / (name + '.exe')
        path.write_bytes(contents)
        paths.append(str(path))
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--format', 'jsonl', *paths], capture_output=True,
                            text=True, check=True)
    reports = [json.loads(line) for line in result.stdout.split('\n') if line.strip()]
    for report in reports:
        entry = report['files'][0]
        name = Path(entry['path']).stem
        ids = {t['id'] for t in entry.get('traits', [])}
        assert THEFT in ids, name
        assert (TASK in ids) == (name == 'task-present'), name
        print('PASS', name)


if __name__ == '__main__':
    main()
