#!/usr/bin/env python3
"""Static controls only. Generated PE fixtures begin with RET and are never run."""
import argparse
import base64
import json
import os
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
p = argparse.ArgumentParser()
p.add_argument('output', type=Path)
args = p.parse_args()
args.output.mkdir(parents=True, exist_ok=True)


def pe(strings):
    size = (len(strings) + 511) & ~511
    data = bytearray(0x400 + size)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x8664, 2, 0, 0, 0, 0xf0, 0x22)
    o = 0x98
    struct.pack_into('<H', data, o, 0x20b)
    struct.pack_into('<II', data, o+16, 0x1000, 0x1000)
    struct.pack_into('<Q', data, o+24, 0x140000000)
    struct.pack_into('<II', data, o+32, 0x1000, 0x200)
    struct.pack_into('<II', data, o+56, 0x2000+((size+4095)&~4095), 0x200)
    struct.pack_into('<H', data, o+68, 3)
    struct.pack_into('<I', data, o+108, 16)
    for i, (name, rva, ptr, sz, flags) in enumerate([
        (b'.text', 0x1000, 0x200, 0x200, 0x60000020),
        (b'.rdata', 0x2000, 0x400, size, 0x40000040),
    ]):
        pos = 0x188+i*40
        data[pos:pos+8] = name.ljust(8, b'\0')
        struct.pack_into('<IIII', data, pos+8, sz, rva, sz, ptr)
        struct.pack_into('<I', data, pos+36, flags)
    data[0x200] = 0xc3
    data[0x400:0x400+len(strings)] = strings
    return bytes(data)


NAME = 'objectives/anti-analysis/environment-detect/set-check::encoded-batch-analysis-name-comparison'
OBF = 'objectives/anti-static/obfuscation/string/concat::encoded-batch-caret-env-command-fragments'
VM = 'objectives/anti-analysis/vm-detect/wmi::encoded-manufacturer-vm-vendor-branch'
TOKEN = 'micro-behaviors/data/embedded/payload/trailer::repeated-token-field-delimiter'
NVM = 'well-known/tool/development/toolchain/nvm-windows::nvm4w-go-module-path'
FNV = 'micro-behaviors/data/checksum::fnv1a-name-reference'
HYPERV = 'micro-behaviors/os/virtualization/hypervisor::hyperv-vendor-reference'
BAD_HV = 'objectives/anti-analysis/environment-detect/runtime::runtime-vm-detection-evidence'
CRASH = 'objectives/anti-analysis/self-terminate::anti-analysis-self-destruct'
FRP = 'micro-behaviors/communications/proxy/tunnel::frp-command-config-name-reference'
# The engine omits low-value any-of wrappers; assert their execution leaf.
SHELL = 'micro-behaviors/process/create/shell/command-string::embedded-sh-c-literal'
CASES = []


def case(name, data, required=(), forbidden=(), suffix='.exe'):
    path = args.output/(name+suffix)
    path.write_bytes(data)
    CASES.append((path, set(required), set(forbidden)))


def encoded(script):
    return pe(base64.b64encode(script)+b'\0')


fragments = b''.join(b'%^%'+letter+b'%'+b'AbCdEfGh'*8+b'%' for letter in [b's', b'e', b't'])
probe = b'computersystem get manufacturer,model | findstr /i "'+b'vmware virtualbox qemu'+b'" >nul && goto :done\r\n'
compare = b'if /i "!identity!"=="sandbox" goto :done\r\n'
case('encoded-name-compare', encoded(compare), [NAME], [VM, OBF])
case('ordinary-hostname', encoded(b'echo %COMPUTERNAME%\r\n'), [], [NAME, VM, OBF])
case('ordinary-sandbox-prose', encoded(b'echo "sandbox"\r\n'), [], [NAME, VM, OBF])
case('obfuscated-vm-gate', encoded(fragments+b' "x=y"\r\n'+probe+compare), [NAME, OBF, VM])
case('unobfuscated-vm-inventory', encoded(probe), [], [OBF, VM])
case('obfuscation-without-vm-query', encoded(fragments+b'\r\n'), [OBF], [VM])
case('different-query', encoded(fragments+b'\r\n'+probe.replace(b'manufacturer,model', b'caption')), [OBF], [VM])
case('two-fragments', encoded(fragments[:fragments.rfind(b'%^%')]+b'\r\n'), [], [OBF, VM])
case('bare-nvm-token', pe(b'NVM4W\0'), [], [NVM])
case('embedded-base64-nvm-token', pe(b'xSlAxRy94VkVxeDQ1S1gvQjhuNVM4WFhuMFRmdG9vbXdKeXBRaCtjTU\0'), [], [NVM])
case('nvm-main-module', pe(b'github.com/coreybutler/nvm-windows/src/nvm.go\0'), [NVM])
case('nvm-author-module', pe(b'github.com/author/author-nvm/cmd/register\0'), [NVM])
case('fnv-name', pe(b'Uses FNV-1a hashing\0'), [FNV])
case('incidental-base64-fnv', pe(b'FpxS1cwTDRrNkdPUStLRFlVMkFnV1A4T3pZS2h0NkgveGRaK0JGYi95\0'), [], [FNV])
token = b'AbCdEfGhIjKlMnOpQrSt'
case('same-token-fields', pe(b'\0'+(token+b'0')*3+b'payload\0'), [TOKEN])
case('different-token-fields', pe(b'\0'+token+b'0'+b'BcDeFgHiJkLmNoPqRsTu0'+token+b'0payload\0'), [], [TOKEN])
case('base64-instruction-text', pe(b'EiD+Xd2Crp3AAAA6XoGAABIidBIweAGSAHYSIsISDGMJMAAAABIi0gISDGMJMgAAABIi0gQSDGMJNAAAABIi0gYSDGMJNgAAABIi0ggSDGMJOAA\0'), [], [TOKEN])
case('frpc-reference', b'frpc -c config.toml\n', [FRP], suffix='.sh')
case('frps-reference', b'frps -c config.toml\n', [FRP], suffix='.sh')
case('shell-inline', b'const command = "sh -c echo-ready";\n', [SHELL], suffix='.js')
case('hyperv-inventory', pe(b'Microsoft Hv\0'), [HYPERV], [BAD_HV])
case('hyperv-self-destruct', pe(b'Microsoft Hv\0analysis rejection *(uintptr_t*)0 = 0\0'), [HYPERV, CRASH])
KEY = 'micro-behaviors/communications/http/services/google::google-api-key-packed'
key = b'AIza'+b'B'*35
case('google-packed-key', pe(b'project.firebaseapp.com'+key+b'FIREBASE_CONFIGPath__Pyx\0'), [KEY])
case('google-key-in-base64-carrier', pe(b'@'+b'A'*1600+key+b'C'*1600+b'==\0'), [], [KEY])
case('google-key-alone', pe(key+b'\0'), [KEY])
cmd = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'jsonl']
r = subprocess.run(cmd+[str(c[0]) for c in CASES], capture_output=True, text=True)
if r.returncode:
    raise SystemExit(r.stderr)
(args.output/'controls.after.jsonl').write_text(r.stdout)
reports = [json.loads(line) for line in r.stdout.splitlines() if line.strip()]
files = {str(Path(f['path']).resolve()): f for d in reports for f in d.get('files', [d])}
for path, required, forbidden in CASES:
    ids = {t['id'] for t in files[str(path.resolve())].get('traits', [])}
    assert required <= ids, (path.name, 'missing', required-ids)
    assert not forbidden & ids, (path.name, 'unexpected', forbidden & ids)
    print('PASS', path.name)
print(len(CASES), 'static controls passed')
