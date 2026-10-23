#!/usr/bin/env python3
"""Check native behavior relationships without executing any specimen code.

Requires pefile (use the recorded analysis venv), original SHA-256-pinned
samples, and the manually recovered stage listed in review.json.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import pefile

p=argparse.ArgumentParser()
p.add_argument('--inventory',required=True)
p.add_argument('--output',required=True)
p.add_argument('--atomscan',default='../scan/target/release/atomscan')
p.add_argument('--stage',default='/tmp/endpoint-review-20261023/native/6d6a677eea21/mapped-0x801a4000-rebuilt.dll')
p.add_argument('--go-functions',default='/tmp/endpoint-review-20261023/native/41a5625a68c0/go-functions.json')
p.add_argument('--go-calls',default='/tmp/endpoint-review-20261023/native/41a5625a68c0/go-calls.json')
a=p.parse_args()
rows=json.loads(Path(a.inventory).read_text())
if isinstance(rows,dict):rows=rows['samples']
def sample(prefix):
    row=next(s for s in rows if s['sha256'].startswith(prefix))
    data=Path(row['local_path']).read_bytes()
    assert hashlib.sha256(data).hexdigest()==row['sha256']
    return data

xor='micro-behaviors/data/decode/stream::x64-word-mixer-inplace-xor-loop'
dispatch='objectives/anti-static/obfuscation/control-flow/dispatch::repeated-cmov-relative-branch-tables-x64'
http='micro-behaviors/communications/http/client/winhttp::indirect-winhttp-secure-request-shape-x64'
facade='objectives/evasion/masquerade/version-resource/claim::unsigned-defender-export-rwx-loader-list'
lists='micro-behaviors/os/module/link::native-ldr-adjacent-list-insertion-x64'
rwx='micro-behaviors/mem/alloc/virtual::x64-call-rwx-protect-fourth-arg'
command='micro-behaviors/process/create/command-handler::go-script-handler-command-context-call'
registry='micro-behaviors/os/registry/manipulate::go-persistence-registry-value-write-call'
root='micro-behaviors/crypto/certificate/install::go-root-certificate-request-routine'
debug='objectives/anti-analysis/debugger-detect/combined-checks::go-check-driver-calls-antidebug'
vm='objectives/anti-analysis/environment-detect/check::go-check-driver-calls-antivm'
go_ids={command,registry,root,debug,vm}

with tempfile.TemporaryDirectory(prefix='endpoint-native-coverage-') as directory:
    tmp=Path(directory);cases=[]
    def add(name,data,yes=None,no=()):
        path=tmp/name;path.write_bytes(data);cases.append((path,yes or {},set(no)))
    exe=sample('88a45d')
    add('renamed-native.exe',exe,{xor:3,dispatch:4,http:3})
    add('ordinary-http-flags.exe',exe.replace(bytes.fromhex('c744243000008000'),bytes.fromhex('c744243000000000')),{dispatch:4},(http,))
    changed=exe.replace(bytes.fromhex('42303c06'),bytes.fromhex('42323c06'))
    assert changed!=exe
    add('no-inplace-xor.exe',changed,{dispatch:4},(xor,))
    # Changing cipher constants preserves the recognized buffer operation.
    changed=exe.replace(bytes.fromhex('3bb57013dbace828'),bytes.fromhex('47b57013dbace828'))
    assert changed!=exe
    add('different-mixer-constant.exe',changed,{xor:3})
    stage=Path(a.stage).read_bytes()
    assert hashlib.sha256(stage).hexdigest()=='1dff04e5387093e4e4262b62875d59d44fb2e559cf79c5db074bdcb474436138'
    add('recovered-stage.dll',stage,{xor:3,dispatch:4,http:3})
    dll=sample('6d6a67')
    add('renamed-module.dll',dll,{facade:5,lists:4,rwx:3})
    assert b'MpAllocMemory' in dll
    add('no-defender-memory-export.dll',dll.replace(b'MpAllocMemory',b'XxAllocMemory'),{lists:4},(facade,))
    rwx_block=bytes.fromhex('41b94000000031c9ba')
    assert rwx_block in dll
    add('non-executable-allocation.dll',dll.replace(rwx_block,bytes.fromhex('41b90400000031c9ba')),{lists:4},(facade,rwx))
    insert=bytes.fromhex('488b4c246848890a48894e18')
    assert insert in dll
    add('no-adjacent-loader-link.dll',dll.replace(insert,bytes.fromhex('488b4c246848890a48894e10')),{rwx:3},(facade,lists))

    go=sample('41a562')
    add('agent.exe',go,{command:3,registry:3,root:4,debug:4,vm:4})
    add('changed-package-owner.exe',go.replace(b'core/cmd/agent/',b'else/cmd/owner/'),{command:3,registry:3,root:4,debug:4,vm:4})
    calls=json.loads(Path(a.go_calls).read_text())
    pe=pefile.PE(data=go)
    def remove_calls(caller_suffix,target_suffix):
        changed=bytearray(go);count=0
        for caller,items in calls.items():
            if caller.endswith(caller_suffix):
                for c in items:
                    if c['target'].endswith(target_suffix):
                        pos=pe.get_offset_from_rva(int(c['at'],16)-pe.OPTIONAL_HEADER.ImageBase)
                        assert changed[pos]==0xe8
                        changed[pos:pos+5]=b'\x90'*5;count+=1
        assert count
        return bytes(changed)
    add('handler-has-no-exec-call.exe',remove_calls('handlers.executeScript','os/exec.CommandContext'),no=(command,))
    add('persistence-has-no-writer-call.exe',remove_calls('persistence.Setup','registry.Key.setStringValue'),no=(registry,))
    add('checks-have-no-debug-call.exe',remove_calls('protect.RunChecks','protect.antiDebug'),no=(debug,))
    add('checks-have-no-vm-call.exe',remove_calls('protect.RunChecks','protect.antiVM'),no=(vm,))
    changed=bytearray(go)
    pos=pe.get_offset_from_rva(0x402950)
    assert changed[pos:pos+4]==b'ROOT'
    changed[pos:pos+4]=b'MYCA'
    add('different-certificate-store.exe',changed,{command:3,registry:3},(root,))
    # Keep all names and strings, but remove pclntab's structural authority.
    add('unstructured-go-name-strings.exe',go.replace(b'\xf1\xff\xff\xff\0\0\1\10',b'\0'*8),no=go_ids)
    # A signed vendor driver alone establishes none of these capabilities.
    cheat=sample('c1c295');driver=cheat[0x148600:0x148600+97168]
    add('standalone-vendor-driver.sys',driver,no={facade,lists,http,xor,dispatch}|go_ids)

    proc=subprocess.run([a.atomscan,'--no-update','--mode','slow','--format','json','path']+[str(c[0]) for c in cases],capture_output=True,text=True,env=dict(os.environ,CLEAVE_TRAITS_DIR=str(Path.cwd()),XDG_CACHE_HOME=str(tmp/'cache')))
    assert proc.returncode in (0,1,2),proc.stderr
    found={}
    for line in proc.stdout.splitlines():
        files=json.loads(line)['raw']['files']
        found[files[0]['path']]={t['id']:t['crit'] for f in files for t in f.get('traits',[])}
    assert len(found)==len(cases),(len(found),len(cases),proc.stderr)
    result=[]
    for path,yes,no in cases:
        got=found[str(path)]
        assert all(got.get(k)==v for k,v in yes.items()),(path.name,yes,{k:v for k,v in got.items() if k in set(yes)|no})
        assert not no.intersection(got),(path.name,no.intersection(got))
        result.append({'case':path.name,'required':yes,'forbidden':sorted(no),'passed':True})
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print(len(result),'native relationship checks passed')
