#!/usr/bin/env python3
"""Regression checks for C triage claims and their required evidence."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
cases = {
    'declarations.h': 'void getProcessHandles(); void remoteCloseHandle(); void isFileObj(); void isDiskFile();\n',
    'close.c': 'void f(){ getProcessHandles(); remoteCloseHandle(); isFileObj(); DuplicateHandle(a,b,c,d,0,0,DUPLICATE_CLOSE_SOURCE); }\n',
    'inject.c': 'void f(){ CreateProcessA(a,b,c,d,e,CREATE_SUSPENDED,f,g,h,i); GetThreadContext(t,c); SetThreadContext(t,c); WriteProcessMemory(p,a,b,n,0); VirtualAllocEx(p,0,n,MEM_COMMIT,PAGE_EXECUTE_READWRITE); }\n',
    'hollow.c': 'void f(){ CreateProcessA(a,b,c,d,e,CREATE_SUSPENDED,f,g,h,i); GetThreadContext(t,c); SetThreadContext(t,c); WriteProcessMemory(p,a,b,n,0); NtUnmapViewOfSection(p,a); }\n',
    'shadow.c': 'char *path="/etc/shadow"; void f(){ bpf_probe_write_user(a,b,c); }\n',
    'sudo.c': 'char *path="/etc/sudoers"; void f(){ bpf_probe_write_user(a,b,c); }\n',
    'hooks.cpp': 'void winhook_iathook() { x->FirstThunk; int a = IMAGE_DIRECTORY_ENTRY_IMPORT; }\n'
                 'void winhook_inlinehooks() { MH_Initialize(); MH_CreateHook(a,b,c); }\n',
}
with tempfile.TemporaryDirectory(prefix='c-triage-evidence-') as temp:
    root = Path(temp)
    for name, source in cases.items():
        (root / name).write_text(source)
    result = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                             '--format=json', *(str(root / name) for name in cases)],
                            check=True, capture_output=True, text=True)
    reports = {Path(f['path']).name: f
             for line in result.stdout.splitlines() if line
             for f in json.loads(line)['files']}
    found = {name: {t['id'] for t in f.get('traits', [])} for name, f in reports.items()}
    checks = [
        ('objectives/evasion/file-unlock/handle-hijack::handle-hijack-file-unlock', 'close.c', 'declarations.h'),
        ('objectives/execution/payload/process-inject/hollowing/source::c-source-process-hollowing', 'hollow.c', 'inject.c'),
        ('objectives/evasion/kernel-hide/ebpf::sudoers-manipulation', 'sudo.c', 'shadow.c'),
    ]
    for trait, positive, negative in checks:
        assert trait in found[positive], (positive, trait)
        assert trait not in found[negative], (negative, trait)
    hook_traits = {t['id']: t['crit'] for t in reports['hooks.cpp'].get('traits', [])}
    for suffix in ('iat-hooking-source', 'inline-hooking-source'):
        assert hook_traits['micro-behaviors/process/hook/interception::' + suffix] in (3, 'notable')
    print('C triage claims require their distinguishing evidence.')
