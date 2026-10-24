#!/usr/bin/env python3
"""Compile-only and inert Mach-O controls for the knjrbfw drift corrections."""
import json
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
HIDDEN = 'micro-behaviors/fs/path/cache::hidden-library-cache-entry'
POLICY = 'micro-behaviors/os/security/policy::jvm-system-security-manager-reference'
BYPASS = 'objectives/evasion/security-bypass/policy/execution::jvm-security-policy-bypass'
FAMILY = 'well-known/malware/backdoor/silencelift::silencelift-behavior'
IOTOP = 'micro-behaviors/os/sysinfo/performance::ruby-iotop-command-reference'
CONCH_PATH = '/Library/Caches/.com.apple.sqliteConchHostId'


def macho(path, strings):
    # A return instruction and NUL-separated text, never executed. Keeping the
    # strings in __text exercises the existing SILENCELIFT consumer's scope.
    payload = b'\xc3\0' + b'\0'.join(s.encode() for s in strings) + b'\0'
    header = struct.pack('<8I', 0xfeedfacf, 0x1000007, 3, 6, 1, 152, 0x85, 0)
    segment = struct.pack('<II16sQQQQIIII', 0x19, 152, b'__TEXT', 0, 4096,
                          0, 4096, 7, 5, 1, 0)
    section = struct.pack('<16s16sQQIIIIIIII', b'__text', b'__TEXT', 256,
                          len(payload), 256, 0, 0, 0, 0x80000400, 0, 0, 0)
    path.write_bytes(((header + segment + section).ljust(256, b'\0') + payload).ljust(4096, b'\0'))


def scan(path):
    run = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format',
                          'json', str(path)], capture_output=True, text=True,
                         check=False)
    assert run.returncode == 0, (path.name, run.stderr)
    report = json.loads(run.stdout)
    traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
    return traits


results = []

def check(path, yes=(), no=()):
    traits = scan(path)
    missing, unwanted = set(yes) - traits.keys(), set(no) & traits.keys()
    assert not missing and not unwanted, (path.name, missing, unwanted)
    if HIDDEN in traits:
        assert traits[HIDDEN]['crit'] == 3, (path.name, traits[HIDDEN])
    results.append({'file': path.name, 'present': list(yes), 'absent': list(no)})
    print('PASS', path.name)

for name, paths, yes, no in [
    ('coordination', [CONCH_PATH], [HIDDEN], []),
    ('hidden', ['/Library/Caches/.payload'], [HIDDEN], []),
    ('renamed', ['/Library/Caches/.alternate.42/cache.bin'], [HIDDEN], []),
    ('suffix', [CONCH_PATH + '.backup'], [HIDDEN], []),
    ('child', [CONCH_PATH + '/payload'], [HIDDEN], []),
    ('both', [CONCH_PATH, '/Library/Caches/.payload'], [HIDDEN], []),
    ('same-string', [CONCH_PATH + ' /Library/Caches/.payload'], [HIDDEN], []),
]:
    p = OUT / (name + '.dylib')
    macho(p, paths)
    check(p, yes, no)

behaviors = ['pkill -STOP agent', 'pkill -CONT agent',
             '{"bot_id":"control"}', 'CGSSessionScreenIsLocked']
for name, paths in [
    ('consumer', ['/Library/Caches/.payload']),
    ('consumer-with-conch', [CONCH_PATH, '/Library/Caches/.other']),
]:
    p = OUT / (name + '.dylib')
    macho(p, paths + behaviors)
    check(p, [HIDDEN, FAMILY])

src = Path(__file__).resolve().parent
subprocess.run(['javac', '--release', '8', '-Xlint:-options', '-d', str(OUT),
                *map(str, sorted(src.glob('*.java')))], check=True)
check(OUT / 'PolicyChange.class', [POLICY, BYPASS])
check(OUT / 'OwnSetter.class', no=[POLICY, BYPASS])
check(OUT / 'PropertyOnly.class', no=[POLICY, BYPASS])
for name, content, yes in [
    ('monitor.rb', 'cmd = "iotop -bPk"\nIO.popen(cmd)\n', [IOTOP]),
    ('mention.rb', '# iotop -bPk\nputs "hello"\n', []),
    ('substring.rb', 'cmd = "myiotop -bPk"\nIO.popen(cmd)\n', []),
    ('filename.rb', 'files = ["lib/knj/iotop.rb"]\n', []),
    ('absolute.rb', 'cmd = "/usr/bin/iotop -bPk"\nIO.popen(cmd)\n', [IOTOP]),
]:
    p = OUT / name
    p.write_text(content)
    check(p, yes, [] if yes else [IOTOP])

(OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
