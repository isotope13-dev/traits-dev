#!/usr/bin/env python3
"""Focused controls for decoded-command coverage and matcher relocations."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SHELL = 'micro-behaviors/process/create/shell/pipeline::'
STREAM = 'micro-behaviors/process/io/stream::'
OBF = 'objectives/anti-static/obfuscation/eval/interpreter::'
HOST = 'micro-behaviors/os/sysinfo/hostname::shell-hostname-command-text'
UNAME = 'micro-behaviors/os/sysinfo/platform/kernel::shell-uname-all-command-text'
RELEASE = 'micro-behaviors/os/sysinfo/platform/files::os-release-read'
HEX = '62756e20696e7374616c6c206261642d706b67'
CASES = {
    'survey.sh': ('id; whoami; hostname; uname -a; cat /etc/os-release\n',
                  [HOST, UNAME, RELEASE], []),
    'words.sh': ("printf '%s' hostname uname\nprintf '%s' 'uname -a'\n",
                 [], [HOST, UNAME, RELEASE]),
    'transport.sh': ('xxd -r -p | sh\n',
                     [SHELL + 'xxd-hexdecode-shell-stdin'],
                     [OBF + 'xxd-hexdecode-pipe-shell']),
    'hex-sink.sh': (f'echo {HEX} | xxd -r -p | sh\n',
                    [SHELL + 'xxd-hexdecode-shell-stdin',
                     OBF + 'xxd-hexdecode-pipe-shell'], []),
    'short-hex.sh': ("echo 6964 | xxd -r -p | sh\n",
                      [OBF + 'xxd-hexdecode-pipe-shell'], []),
    'hex-data.sh': (f'echo {HEX} | xxd -r -p > message.txt\n',
                    [],
                    [SHELL + 'xxd-hexdecode-shell-stdin',
                     OBF + 'xxd-hexdecode-pipe-shell']),
    'stream.py': ('command = "echo \'{PAYLOAD}\' | decoder"\n',
                  [], []),
}
# Existing positives outside this review batch must retain their attack signals.
EXISTING = {
    'testdata/obfuscation/shell/06_hex.sh': [OBF + 'xxd-hexdecode-pipe-shell'],
    'testdata/hostile/dev-tcp-executable-test.sh': [
        'objectives/command-and-control/reverse-shell/dev-tcp::dev-tcp-bash-stdin-redirect'],
    'testdata/hostile/dev-tcp-alternate-test.sh': [
        'objectives/command-and-control/reverse-shell/dev-tcp::dev-tcp-bash-stdin-redirect'],
}
with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
    checks = {}
    for name, (source, present, absent) in CASES.items():
        p = Path(tmp) / name
        p.write_text(source)
        checks[str(p)] = (present, absent)
    for name, present in EXISTING.items():
        checks[str(ROOT / name)] = (present, [])
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', *checks], text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr)
    decoder = json.JSONDecoder()
    remaining = result.stdout
    reports = []
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        reports.extend(report['files'])
    for path, (present, absent) in checks.items():
        report = next(f for f in reports if Path(f['path']).resolve() == Path(path).resolve())
        actual = {t['id'] for t in report.get('traits', [])}
        assert set(present) <= actual, (path, 'missing', set(present) - actual)
        assert not set(absent) & actual, (path, 'unexpected', set(absent) & actual)
    trace = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         'test-rules', str(Path(tmp) / 'stream.py'), '--rules',
         STREAM + 'echo-identifier-literal-pipeline-fragment'],
        text=True, capture_output=True, check=True)
    assert 'NOT MATCHED' not in trace.stdout, trace.stdout
    assert 'MATCHED' in trace.stdout, trace.stdout
print(f'{len(checks)} focused controls passed')
