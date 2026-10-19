"""Static matcher controls. No fixture or reviewed executable is executed."""
import concurrent.futures
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ENGINE = os.environ.get('CLEAVE', 'cleave')
ENV = dict(os.environ, CLEAVE_VALIDATE='0')

def scan(path):
    result = subprocess.run([ENGINE, '--traits-dir', str(ROOT), '--format', 'json', str(path)],
                            env=ENV, capture_output=True, text=True, check=True)
    report = json.loads(result.stdout)
    return {t['id']: t for f in report['files'] for t in f['traits']}

def check(case):
    with tempfile.TemporaryDirectory(prefix='control-', dir=ROOT) as directory:
        copied = Path(directory) / case['path']
        shutil.copyfile(HERE / case['path'], copied)
        traits = scan(copied)
    missing = set(case['matched']) - traits.keys()
    unexpected = set(case['not_matched']) & traits.keys()
    assert not missing and not unexpected, (case['path'], missing, unexpected)
    if case['no_elevated']:
        assert not any(t['crit'] >= 4 for t in traits.values()), (case['path'], traits)
    return 'PASS ' + case['path']

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    for message in pool.map(check, json.loads((HERE / 'cases.json').read_text())['fixtures']):
        print(message, flush=True)

# Optional real-sample controls strip one required role at a time. Copies stay
# in a temporary directory and retain valid CLR string lengths and PE layout.
if len(sys.argv) > 1:
    sample = Path(sys.argv[1])
    target = 'objectives/command-and-control/remote-command/tasking::managed-keylogger-http-command-executor'
    assert target in scan(sample), sample
    content = sample.read_bytes()
    with tempfile.TemporaryDirectory(prefix='managed-review-', dir=ROOT) as directory:
        for name, text, encoding in [('executor', 'StartCommandExecutor', 'ascii'),
                                      ('response', 'GetResponseStream', 'ascii'),
                                      ('record', 'CMD_OUT:', 'utf-16le')]:
            token = text.encode(encoding)
            assert token in content, (name, token)
            replacement = ('X' * len(text)).encode(encoding)
            changed = Path(directory) / (name + '.exe')
            changed.write_bytes(content.replace(token, replacement))
            assert target not in scan(changed), name
            print('PASS managed missing ' + name, flush=True)
