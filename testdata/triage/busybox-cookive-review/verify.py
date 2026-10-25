"""Compare retained coverage and exercise IElevator/pipe boundary controls.
No generated PE is executed. All artifacts are written to the supplied scratch.
Usage: python3 verify.py SCRATCH BASELINE_TRAITS ORIGINAL_DLL
"""
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('pe_controls', ROOT / 'testdata/native-rat-loader-triage/verify.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
DEST, BASELINE, ORIGINAL = map(Path, sys.argv[1:])
DEST.mkdir(parents=True, exist_ok=True)
RELOCATIONS = json.loads((ROOT / 'testdata/triage/busybox-cookive-review/relocations.json').read_text())
KEY = 'objectives/credential-access/browser/app-bound::chromium-ielevator-com-decrypt-helper'
PIPE = 'objectives/exfiltration/stealer/browser::chromium-decrypted-key-pipe-response'
GUID = 'micro-behaviors/os/com/invoke::chromium-ielevator-guid-stack-dwords'
TABLE = 'micro-behaviors/os/application/target::chromium-brand-target-table'
ABE = 'objectives/credential-access/browser/multi-target::multi-brand-chromium-abe-harvest'
COOKIE = 'objectives/credential-access/browser/multi-target::chromium-multi-brand-cookie-harvest-pe'
GUID_BYTES = bytes.fromhex('CF BE 3A 46 0D 41 7F 40 8A F5 0D F3 5A 00 5C C8')
STACK = b''.join(b'\xc7\x85' + (0x160+i*4).to_bytes(4,'little') + GUID_BYTES[i*4:i*4+4] for i in range(4))
brands = b'Chrome Beta\0Brave\0Edge\0User Data\0chrome.exe\0'
cases = []
def add(name, blob, present=(), absent=(), retained=False):
    path = DEST / name
    path.write_bytes(blob)
    cases.append((path, set(present), set(absent), retained))
add('brand-table.exe', helper.pe_image(data=brands), [TABLE], [KEY, PIPE, ABE, COOKIE], True)
add('brand-key-positive.exe', helper.pe_image(data=brands+b'App-Bound Encryption Key\0'), [TABLE, ABE], [KEY, PIPE], True)
add('brand-cookie-positive.exe', helper.pe_image(data=brands+b'SELECT host_key, encrypted_value FROM cookies\0'), [TABLE, COOKIE], [KEY, PIPE], True)
add('guid-only.exe', helper.pe_image(code=STACK+b'\xc3'), [GUID], [KEY, PIPE])
add('guid-in-data.exe', helper.pe_image(data=STACK), [], [GUID, KEY, PIPE])
add('contiguous-interface-only.exe', helper.pe_image(data=GUID_BYTES), [], [KEY, PIPE], True)
add('partial-guid.exe', helper.pe_image(code=STACK[:-1]+b'\x00\xc3'), [], [GUID, KEY, PIPE])
# These copies are negative controls, never replacement samples or runtime tests.
blob = ORIGINAL.read_bytes()
assert STACK in blob
add('original-copy.exe', blob, [GUID, KEY, PIPE])
add('no-interface.exe', blob.replace(STACK, STACK[:-1]+b'\0'), [], [GUID, KEY, PIPE])
add('no-decrypt-name.exe', blob.replace(b'DecryptData', b'HarmlessLog'), [GUID], [KEY, PIPE])
add('no-pipe-wait.exe', blob.replace(b'WaitNamedPipeA', b'WaitOtherPipeA'), [GUID, KEY], [PIPE])
add('no-key-result.exe', blob.replace(b'Decrypted key is empty', b'Requested log is empty'), [GUID, KEY], [PIPE])
legacy = bytearray(blob.replace(STACK, STACK[:-1]+b'\0'))
legacy[0xaa60:0xaa70] = GUID_BYTES
add('contiguous-helper-positive.exe', bytes(legacy), [KEY], [], True)
add('subtraction-population.js', ('let result = a - b;\n'*31).encode(), ['metadata/file/arithmetic::js-binary-subtraction-cluster'], [], True)
for f in ['testdata/benign/ast-subtraction-with-dates.zip','testdata/native-browser-behavior-review/dictionary-near-miss.exe','testdata/native-browser-behavior-review/path-reference-positive.exe']:
    cases.append((ROOT/f,set(),set(),True))

# Existing encoded-exploit positives and near misses exercise moved YARA atoms.
for case in json.loads((ROOT/'testdata/semantic-browser-carriers/cases.json').read_text())['fixtures']:
    cases.append((ROOT/case['path'], set(case['matched']), set(case['not_matched']), True))
add('service-labels.go', b'package main\nvar name = "SystemUpdate TrustedInstaller"\n', [], [], True)
add('appdata-placeholder.exe', helper.pe_image(data=b'%appdata%\0'), ['micro-behaviors/os/env/path::appdata-env-path-reference'], [], True)
add('cookie-base64.sh', b'cat "$HOME/Library/Application Support/Chrome/Cookies" | base64\n', ['micro-behaviors/data/encode/base64::cookie-store-base64-pipe'], [], True)

def scan(path, rules):
    cmd = ['cleave','--traits-dir',str(rules),'--format','json',str(path)]
    p = subprocess.run(cmd,cwd=ROOT,env=dict(os.environ,CLEAVE_VALIDATE='0'),text=True,capture_output=True,check=True)
    j=json.loads(p.stdout)
    return {t['id']:t['crit'] for f in j['files'] for t in f.get('traits',[])}

def verify(case):
    path, present, absent, retained = case
    after=scan(path,ROOT)
    assert present <= after.keys(), (path.name,'missing',present-after.keys())
    assert not absent & after.keys(), (path.name,'unexpected',absent & after.keys())
    result={'name':path.name,'present':sorted(present),'absent':sorted(absent)}
    if retained:
        before=scan(path,BASELINE)
        previous={RELOCATIONS.get(k,k):v for k,v in before.items()}
        missing=set(previous)-set(after)
        # Low-tier findings are emitted only if a referencing composite fires.
        material={k:v for k,v in previous.items() if v>=3}
        assert not set(material)-after.keys(), (path.name,'lost notable/attack',set(material)-after.keys())
        assert all(after[k]>=v or k==TABLE for k,v in material.items()), (path.name,'reduced attack')
        result['lost_low_tier']=sorted(missing)
        result['hostile_before']=sorted(k for k,v in previous.items() if v==5)
        result['hostile_after']=sorted(k for k,v in after.items() if v==5)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(verify,cases))
(DEST/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS',len(results),'controls, including retained key/cookie detections and existing external fixtures')
