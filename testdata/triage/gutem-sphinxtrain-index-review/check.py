#!/usr/bin/env python3
"""Check static observations; never execute the supplied source snippets."""
import argparse
import base64
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
work = args.scratch / 'controls'
work.mkdir(parents=True, exist_ok=True)
P = 'micro-behaviors/'
AWS = P+'communications/http/services/aws::python-imds-secret-inventory-references'
INV = P+'communications/http/services/cloud::secret-inventory-method-set'
B64 = P+'fs/path/credential::base64-kubernetes-serviceaccount-directory'
UPLOAD = P+'communications/http/upload::encoded-curl-file-upload'
OOB = P+'communications/url/host/oob::node-child-process-webhook-site-reference'
NAME = 'metadata/lang/source/naming/action::javascript-webhook-send-name'
HIDE = P+'ui/window/control::node-hide-console-call'
TERRAFORM = P+'fs/path/secret-config::terraform-credentials-path-reference'
UNIT = 'objectives/persistence/system/service/systemd::python-user-unit-secret-access'
retired = {
    'objectives/credential-access/cloud/aws-token::python-aws-imds-secret-inventory',
    'objectives/credential-access/cloud/secret-inventory::secrets-manager-inventory-api',
    'objectives/exfiltration/oob/endpoint::os-recon-to-oob-collector',
    'objectives/exfiltration/http/encoded::encoded-curl-archive-upload',
    'objectives/credential-access/cloud/container::b64-kubernetes-serviceaccount',
    'objectives/supply-chain/credential-theft/cloud-kube::python-user-systemd-backdoor-install',
    'objectives/exfiltration/messaging/webhook::javascript-send-to-webhook-method',
}
cases = {}
def add(name, source, required=(), forbidden=(), levels=None):
    p = work/name
    p.write_text(source)
    cases[name] = (set(required), set(forbidden), levels or {})

# Existing positive and benign SDK controls are retained across the relocation.
for name in ['secret-inventory-positive.py', 'secret-lifecycle-sdk-benign.py']:
    text = (root/'testdata/secret-lifecycle-sdk-precision'/name).read_text()
    add(name, text, [INV] if 'positive' in name else [], [] if 'positive' in name else [INV], {INV: 3} if 'positive' in name else {})
add('imds-inventory.py', '''methods = ["ListSecrets", "GetSecretValue"]
endpoint = "http://169.254.169.254/latest/api/token"
headers = {"X-Amz-Target": target}
''', [INV, AWS], levels={INV: 3, AWS: 3})
add('imds-alone.py', 'endpoint = "http://169.254.169.254/latest/api/token"\n', forbidden=[INV, AWS])
add('serviceaccount.py', 'encoded = '+repr(base64.b64encode(b'secrets/kubernetes.io/serviceaccount/token').decode())+'\n', [B64], levels={B64: 3})
add('serviceaccount-nearmiss.py', 'encoded = '+repr(base64.b64encode(b'public/kubernetes.io/serviceaccount/info').decode())+'\n', forbidden=[B64])
# This upload sends a caller-supplied file; neither archive nor theft is established.
source = 'subprocess.run(["curl", "-X", "POST", endpoint, "--data-binary", f"@{payload}"])'
add('file-upload.py', 'encoded = '+repr(base64.b64encode(source.encode()).decode())+'\n', [UPLOAD], levels={UPLOAD: 3})
add('post-without-file.py', 'encoded = '+repr(base64.b64encode(b'subprocess.run(["curl", "-X", "POST", endpoint])').decode())+'\n', forbidden=[UPLOAD])
# This is the actual unsupported old-rule combination, with no call or send.
add('oob-unused.js', 'const { spawn } = require("child_process");\nconst documentation = "https://webhook.site/11111111-2222-3333-4444-555555555555";\n', [OOB], levels={OOB: 3})
add('oob-alone.js', 'const documentation = "https://webhook.site/11111111-2222-3333-4444-555555555555";\n', forbidden=[OOB])
add('name-only.js', 'const vocabulary = "sendToWebhook";\n', [NAME], levels={NAME: 3})
add('hide.js', 'require("node-hide-console-window").hideConsole();\n', [HIDE], levels={HIDE: 3})
add('hide-quoted.js', 'const example = "require(\'node-hide-console-window\').hideConsole()";\n', forbidden=[HIDE])
add('hide-defined.js', 'function hideConsole() {}\n', forbidden=[HIDE])
add('terraform.js', 'const path = "~/.terraform.d/credentials.tfrc.json";\n', [TERRAFORM], levels={TERRAFORM: 3})
add('terraform-manifest.js', 'const path = "Cargo.toml";\n', forbidden=[TERRAFORM])
# Real, independently reviewed attack carriers outside this batch retain their
# separate OOB communication detections; they are not excluded as documentation.
external = [
    root/'testdata/helper-agent-triage/postinstall-oob-beacon.tgz',
    root/'testdata/hostile/supply-chain-corpus/py/pypi-driftwoodmesh-import-oob-beacon-linux.whl',
]
for p in external:
    target=work/p.name
    shutil.copyfile(p,target)
    cases[p.name]=(set(),set(),{})
command = [args.cleave, '--no-update-check', '--traits-dir', str(root), '--format=json', 'analyze', str(work)]
r = subprocess.run(command, capture_output=True, text=True, check=True)
(args.scratch/'controls-after.json').write_text(r.stdout)
(args.scratch/'controls-after.err').write_text(r.stderr)
dec = json.JSONDecoder(); text=r.stdout; reports=[]
while text.strip():
    text=text.lstrip();doc,end=dec.raw_decode(text);text=text[end:];reports.extend(doc['files'])
results={}
for report in reports:
    if '!!' in report['path'] or '##' in report['path']:continue
    name=Path(report['path']).name
    if name not in cases:continue
    traits={t['id']:t['crit'] for t in report.get('traits',[])}
    required,forbidden,levels=cases[name]
    assert not required-traits.keys(), (name,'missing',required-traits.keys())
    assert not (forbidden|retired)&traits.keys(), (name,'unexpected',(forbidden|retired)&traits.keys())
    for tid,level in levels.items():assert traits.get(tid)==level,(name,tid,traits.get(tid))
    if name in {p.name for p in external}:
        assert any(t['crit']>=4 for t in report.get('traits',[])),(name,'lost all attack detections')
    results[name]={'required':sorted(required),'levels':levels,'hostile':sum(t['crit']==5 for t in report.get('traits',[])),'suspicious':sum(t['crit']==4 for t in report.get('traits',[]))}
assert len(results)==len(cases),(len(results),len(cases))
(args.scratch/'controls-result.json').write_text(json.dumps(results,indent=2)+'\n')
print(f'{len(results)} static controls passed')
