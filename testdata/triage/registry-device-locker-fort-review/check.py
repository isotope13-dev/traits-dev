"""Offline regression controls. Never launches a specimen or contacts a target."""
import argparse
import ast
import base64
import collections
import json
from pathlib import Path
import random
import re
import string
import subprocess
import types

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def simulate_fort(path):
    # Only inspected constant assignments and function definitions are loaded.
    # All external effects are supplied by the fakes below; main is never run.
    tree = ast.parse(path.read_text())
    tree.body = [n for n in tree.body if isinstance(n, (ast.Assign, ast.FunctionDef))]
    events = []
    class Clock:
        now = 100
        def time(self): return self.now
        def sleep(self, seconds):
            events.append(['sleep', seconds])
            self.now += seconds
    class Cipher:
        def decrypt(self, data):
            events.append(['AES.decrypt', data.hex()])
            return b'recovered\x00'
    class AES:
        MODE_CBC = 2
        @staticmethod
        def new(key, mode, iv):
            events.append(['AES.new', key.decode(), mode, iv.hex()])
            return Cipher()
    ns = dict(__name__='offline_review', base64=base64, json=json, random=random,
              re=re, string=string, time=Clock(), AES=AES)
    exec(compile(tree, str(path), 'exec'), ns)
    encoded = base64.b64encode(b'IVIV' + b'0123456789abcdef').decode()
    class Session:
        def __init__(self, brute=False):
            self.brute = brute
            self.count = 0
            self.cookies = types.SimpleNamespace(get_dict=lambda: {'ccsrftoken': 'test'})
        def post(self, url, **kwargs):
            events.append(['POST', url, kwargs])
            self.count += 1
            return types.SimpleNamespace(status_code=200, text='2' if self.brute and self.count == 1 else 'ok')
        def get(self, url, **kwargs):
            events.append(['GET', url, kwargs])
            return types.SimpleNamespace(status_code=200, text='set password ENC ' + encoded)
    s = Session()
    user, password = ns['exploit_cve_2025_64446']('https://device.invalid', s)
    assert user == password and len(user) == 8
    header = json.loads(base64.b64decode(events[0][2]['headers']['CGIINFO']))
    assert header['username'] == 'admin' and header['profname'] == 'prof_admin'
    assert events[0][2]['json']['data']['trusthostv4'] == '0.0.0.0/0'
    assert events[1][2]['auth'] == (user, password)
    assert ns['download_and_parse_config']('https://device.invalid', s) == ['recovered']
    ns['blocked_hosts'].clear()
    assert ns['brute_force_fortigate']('device.invalid', 'https://device.invalid', Session(True), [('a','a'), ('b','b')]) == ('b','b')
    assert ['sleep', 60] in events
    # Random credentials vary; do not record them as a specimen signature.
    for e in events:
        if e[0] == 'POST' and 'json' in e[2]:
            e[2]['json']['data']['name'] = '<generated>'
            e[2]['json']['data']['password'] = '<generated>'
        if e[0] == 'GET' and 'auth' in e[2]: e[2]['auth'] = ['<generated>', '<generated>']
    return events


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--samples-root', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    cases = json.loads((HERE/'cases.json').read_text())['fixtures']
    cases += [
        {'path': str(args.samples_root/'add21a42a1e6/device-relay.html'), 'matched': ['objectives/credential-access/phishing/device-code::device-code-session-relay'], 'counts': [2,0]},
        {'path': str(args.samples_root/'ea13c6e29a3a/gentlemen_locker.go'), 'matched': ['objectives/persistence/system/scheduled-task::go-boot-task-with-defender-blinding', 'objectives/persistence/login/scheduled-task/cli::go-logon-task-with-defender-blinding', 'objectives/persistence/login/registry/run-key::go-run-key-with-defender-blinding', 'objectives/evasion/self-delete/file/script::go-formatted-executable-and-batch-self-delete', 'objectives/impact/services/stop::go-service-disable-with-recovery-destruction', 'micro-behaviors/fs/write/content::go-free-space-query-and-zero-write-loop']},
        {'path': str(args.samples_root/'57a5e02b20cb/fort.py'), 'matched': ['objectives/lateral-movement/brute-force/password/appliance::python-fortinet-online-credential-guessing','micro-behaviors/communications/tls/verify/disable::python-session-request-verify-false','objectives/persistence/login/account/create::fortinet-unrestricted-admin-account-create'], 'levels': {'objectives/credential-access/files/appliance::fortios-default-key-config-password-decrypt': 4}},
    ]
    paths = [str(ROOT/c['path']) for c in cases]
    result = subprocess.run(['cleave','--traits-dir',str(ROOT),'--format','json',*paths], cwd=ROOT, capture_output=True, text=True)
    if result.returncode: raise RuntimeError(result.stderr)
    reports, tail = [], result.stdout.strip()
    decoder = json.JSONDecoder()
    while tail:
        report, end = decoder.raw_decode(tail)
        reports.append(report)
        tail = tail[end:].lstrip()
    files = {str(Path(f['path']).resolve()): f for report in reports for f in report['files']}
    records = []
    for c, p in zip(cases,paths):
        f = files[str(Path(p).resolve())]
        traits = {t['id']:t['crit'] for t in f.get('traits',[])}
        assert set(c.get('matched',[])) <= traits.keys(), (p, 'missing', set(c.get('matched',[]))-traits.keys())
        assert not set(c.get('not_matched',[])) & traits.keys(), (p,'unexpected',set(c.get('not_matched',[]))&traits.keys())
        for name, level in c.get('levels',{}).items(): assert traits.get(name) == level, (p,name,traits.get(name))
        counts = collections.Counter(traits.values())
        if 'max_hostile' in c: assert counts[5] <= c['max_hostile'], (p,'hostile',counts[5])
        if 'counts' in c: assert [counts[5],counts[4]] == c['counts'], (p,counts)
        records.append({'path': c['path'], 'hostile':counts[5], 'suspicious':counts[4], 'passed':True})
    args.output.write_text(json.dumps({'static_controls':records,'fort_mock_trace':simulate_fort(args.samples_root/'57a5e02b20cb/fort.py')},indent=2)+'\n')
    print(f'{len(records)} static controls and offline Python execution-path checks passed')

if __name__ == '__main__': main()
