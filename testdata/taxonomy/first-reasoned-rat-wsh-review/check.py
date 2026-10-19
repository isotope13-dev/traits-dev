"""Generate inert static controls and verify capability/intent separation."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import struct
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--output-dir', type=Path, required=True)
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
a.output_dir.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[3]
GZIP = 'metadata/file/magic/numbers::gzip-magic-source-literals'
CHOICE = 'micro-behaviors/time/sleep/interval::choice-timed-default-delay'
DELETE = 'micro-behaviors/fs/delete/file/command::choice-delayed-file-delete-command'
NAME = 'metadata/binary/symbols/name::managed-connect-sub-socket-method-name'
RANSOM = 'objectives/impact/ransom/encrypt/config::ransom-note-paid-decryption-phrase'
DROP = 'objectives/execution/payload/file-exec::obfuscated-wsh-activex-savetofile-dropper'
ZONE = 'objectives/evasion/indicator-removal/ads::obfuscated-wsh-dropper-zone-overwrite'
PDF = 'metadata/file/naming::pdf-double-extension-script'
OLD_PDF = 'objectives/evasion/masquerade/file/double-ext::pdf-double-ext-obfuscated-script'
OLD_SUB = 'objectives/command-and-control/backdoor/binary::managed-subchannel-connect'
OLD_CHOICE = 'objectives/evasion/self-delete/file/delay::native-choice-del-self'
OLD_WORD = 'objectives/impact/ransom/encrypt/config::ransom-note-decrypt-word'
cases = []

def case(name, content, present=(), absent=()):
    path = a.output_dir / name
    path.write_bytes(content.encode() if isinstance(content, str) else content)
    cases.append((path, set(present), set(absent)))

def pe(text):
    # One read-only code section with RET at the entry point. Strings are inert.
    b = bytearray(1024)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x14c, 1, 0, 0, 0, 0xe0, 0x102)
    struct.pack_into('<H', b, 0x98, 0x10b)
    struct.pack_into('<I', b, 0xa8, 0x1000)
    struct.pack_into('<III', b, 0xb4, 0x400000, 0x1000, 0x200)
    struct.pack_into('<II', b, 0xd0, 0x2000, 0x200)
    struct.pack_into('<H', b, 0xdc, 3)
    struct.pack_into('<I', b, 0xf4, 16)
    struct.pack_into('<8sIIIIIIHHI', b, 0x178, b'.text\0\0\0', 512, 0x1000,
                     512, 0x200, 0, 0, 0, 0, 0x60000020)
    b[0x200] = 0xc3
    data = text.encode() + b'\0'
    b[0x210:0x210+len(data)] = data
    return bytes(b)

case('gzip-hex.js', 'var magic=[0x1f,0x8b,0x08];', [GZIP])
case('gzip-decimal.js', 'var magic=[31,139,8];', [GZIP])
case('arithmetic.js', 'var x=0x1f+0x8b; var y=[139,31,8];', absent=[GZIP])
case('reversed-header.js', 'var x=[0x8b,0x1f,0x08];', absent=[GZIP])
case('delay-only.exe', pe('choice /C Y /N /D Y /T 7'), [CHOICE], [DELETE, OLD_CHOICE])
case('delayed-cleanup.exe', pe('choice /C Y /N /D Y /T 7 & del log.txt'),
     [CHOICE, DELETE], [OLD_CHOICE])
case('method-reference.exe', pe('ConnectSubSockAsync'), [NAME], [OLD_SUB])
case('other-method.exe', pe('ConnectSockAsync'), absent=[NAME, OLD_SUB])
case('decrypt-method.exe', pe('Decrypt'), absent=[RANSOM, OLD_WORD])
case('decrypt-help.c', 'char *s="decrypt your files using your private key";', absent=[RANSOM])
case('paid-decryption.c', 'char *s="To decrypt your files you must pay the ransom";', [RANSOM])
case('document.PDF.JS', 'function generatedName12345() { return 1; }', [PDF], [OLD_PDF, DROP, ZONE])
stage = '''var progid="ADODB.Stream"; var stream=new ActiveXObject(progid);
var decoder=new ActiveXObject("Microsoft.XMLDOM");
var self=WScript["ScriptFullName"]; var payload=node.nodeTypedValue;
stream['SaveToFile'](target,2); shell.Run(target);
var key="a!b"['split']('!')['join']('');
'''
zone = '''var zone=":Z☍o☍n☍e.☍I☍d☍e☍n☍t☍i☍f☍i☍e☍r";
shell.Run('cmd /c echo. > "'+self+zone+'"');
'''
case('obfuscated-stage.js', stage, [DROP], [ZONE])
case('concealed-stage-and-zone.js', stage+zone, [DROP, ZONE], [
    'objectives/execution/payload/file-exec::wsh-obfuscated-savetofile-payload-dropper',
    'objectives/execution/payload/file-exec::wsh-unicode-padded-activex-script-dropper',
    'objectives/command-and-control/dropper/staging/encoded/script::wsh-unicode-padded-base64-dropper'])
case('zone-only.js', 'var progid="WScript.Shell"; var shell=new ActiveXObject(progid);'
     'var self=WScript["ScriptFullName"];'+zone, absent=[DROP, ZONE])
case('no-save.js', stage.replace("stream['SaveToFile'](target,2);", '')+zone,
     absent=[DROP, ZONE])

def check(item):
    path, present, absent = item
    r = subprocess.run([a.cleave, '--traits-dir', str(root), '--format', 'json', str(path)],
                       capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    findings = {t['id']: t for f in d['files'] for t in f.get('traits', [])}
    assert present <= findings.keys(), (path.name, 'missing', sorted(present-findings.keys()))
    assert not absent.intersection(findings), (path.name, 'unexpected', sorted(absent.intersection(findings)))
    if 'cleanup' in path.name:
        assert findings[DELETE]['crit'] == 3
    return {'case': path.name, 'required': sorted(present), 'forbidden': sorted(absent), 'passed': True}

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(check, cases))
(a.output_dir / 'results.json').write_text(json.dumps(results, indent=2)+'\n')
print(f'{len(results)} static positive and near-miss controls passed')
