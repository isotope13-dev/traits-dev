"""Static regression controls; generated PE entry points return immediately.

Usage: python3 check.py <scratch-directory>
The real injector fixture is upstream TripleCross code_caver.h, SHA-256
a35fd3f202c6aed1e60d4967450ece4eb3467c16f9dbb891542f5dcbdf492efc.
Source: https://github.com/h3xduck/TripleCross/blob/master/src/user/include/utils/mem/code_caver.h
No specimen or generated PE is executed.
"""
import ast
import base64
import concurrent.futures
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)

# Reuse only the inert PE builder, without running that checker's test body.
tree = ast.parse((ROOT / 'testdata/darkcleaner-chart-review/check.py').read_text())
builder = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'pe')
exec(compile(ast.Module(body=[builder], type_ignores=[]), '<PE builder>', 'exec'))

HIJACK = 'objectives/evasion/process/injection/hijack::'
MEM = 'micro-behaviors/process/inject/memory::memory-descriptor-shellcode-write-profile'
LIT = 'metadata/lang/source/literal::'
EXT = 'objectives/impact/ransom/extortion::'
ENC = 'objectives/impact/ransom/encrypt/bulk-encryption::native-base64-extortion-file-encryptor'
REC = 'objectives/impact/ransom/recovery-inhibition::native-extortion-shadow-copy-deletion'
TIMES = 'objectives/evasion/indicator-removal/timestamps::ransomware-restores-original-file-times'
AFF = 'objectives/impact/ransom/affiliate::'
OWA = 'objectives/credential-access/email/webmail/owa::owa-browser-state-credential-implant'
FORM = 'micro-behaviors/ui/window/form-input::'
C2 = 'objectives/command-and-control/backdoor/rat/tasking::'

cases = []


def case(name, blob, yes=(), no=()):
    p = OUT / name
    p.write_bytes(blob.encode() if isinstance(blob, str) else blob)
    cases.append((p, set(yes), set(no)))


source = (HERE / 'code-caver.h').read_text()
case('real-injector.c', source,
     [HIJACK+'code-cave-shellcode-injector', HIJACK+'got-hijack-injection', MEM])
case('references-without-write.c', source.replace('write(mem_fd,', 'read(mem_fd,'),
     [LIT+'code-cave-reference', LIT+'shellcode-write-string'],
     [HIJACK+'code-cave-shellcode-injector', HIJACK+'got-hijack-injection', MEM])
case('got-write-without-cave-seek.c', source.replace('lseek(mem_fd, cave_addr,', 'lseek(mem_fd, other_offset,'),
     [HIJACK+'got-hijack-injection'], [HIJACK+'code-cave-shellcode-injector', MEM])
case('reference-only.c', '''void probe(void) {
  int mem_fd = 1; int alias = mem_fd; int again = mem_fd;
  const char *cave = "code cave", *payload = "writing shellcode";
  unsigned long address = READ_KERN(syscall_table_addr[syscall_num]);
}''', [LIT+'code-cave-reference', LIT+'shellcode-write-string'],
     [HIJACK+'code-cave-shellcode-injector', HIJACK+'proc-mem-injection-source', MEM])

case('ordinary-login.js', '''const user = document.createElement('input');
user.autocomplete = 'username';
const pass = document.createElement('input'); pass.autocomplete = 'current-password';''',
     [FORM+'autocomplete-username-attribute', FORM+'autocomplete-current-password-attribute'], [OWA])
case('owa-capture.js', '''PageDataPayload.owaUserDefaultSettings = {};
localStorage.setItem('state', 'payload');
const user = document.createElement('input'); user.autocomplete = 'username';
const pass = document.createElement('input'); pass.autocomplete = 'current-password';
document.addEventListener('click', () => fetch('/capture', {method:'POST', body:user.value+pass.value}));''',
     [OWA, FORM+'autocomplete-current-password-attribute'])

imports = ('GetSystemInfo', 'GetDiskFreeSpaceW', 'GetTickCount64', 'WSASocketW',
           'connect', 'getaddrinfo', 'CreateProcessW', 'WaitForSingleObject', 'GetExitCodeProcess')
case('generic-windows-api-profile.exe', pe(imports=imports, messages=('WS2_32.dll',)),
     ['micro-behaviors/process/create/spawn::create-process-w',
      'micro-behaviors/process/control/wait::process-completion-api-set',
      'micro-behaviors/process/control/wait::get-exit-code-process',
      'micro-behaviors/process/control/wait::wait-for-single-object-api',
      'micro-behaviors/communications/socket/connect::connect-api'],
     [C2+'native-winsock-host-check-command-agent', C2+'windows-native-c2-tasking-agent'])
commands = ('!udp', '!std', '!vse', '!ntp', '!dns', '!tcp', '!xmas', '!http', 'WS2_32.dll')
case('network-attack-command-agent.exe',
     pe(imports=('socket', 'connect', 'send', 'system'), messages=commands),
     [C2+'windows-native-c2-tasking-agent'])

# Four distinct sigma words in code, matching the existing native crypto atom.
code = bytes.fromhex('c7 45 10 65 78 70 61 c7 45 14 6e 64 20 33 '
                     'c7 45 18 32 2d 62 79 c7 45 1c 74 65 20 6b')
helptext = 'Encryption of file(s) (e.g. 1.txt)modeEncryption mode (fast, medium, slow)'
quiet = 'Encrypt files and restore original last write date'
shadow = 'Successfully deleted shadow copies from '
kill = ('Successfully killed process:', 'Successfully killed service:',
        'Successfully killed processes by mask', 'Successfully killed services by mask')
note = b"Your data is stolen and encrypted. If you don't pay the ransom, the data will be published."
new_hostile = [ENC, REC, TIMES, 'objectives/impact/degrade/process::ransomware-file-holder-termination',
               'objectives/impact/degrade/services::ransomware-process-service-termination']
case('ordinary-encryptor.exe', pe(code=code, imports=('ReadFile', 'WriteFile'), messages=(helptext,)),
     ['micro-behaviors/fs/file/encrypt::file-encryption-cli-help'], new_hostile)
case('ordinary-termination-logs.exe', pe(imports=('RmShutdown',), messages=kill),
     ['micro-behaviors/process/terminate/kill::process-kill-success-log',
      'micro-behaviors/os/service/stop::service-kill-success-log'], new_hostile)
case('encoded-note-without-encryptor.exe', pe(messages=(base64.b64encode(note).decode(),)),
     [EXT+'base64-data-theft-extortion-note'], new_hostile)
case('payment-phrase-only.exe', pe(messages=(base64.b64encode(b'pay the ransom').decode(),)),
     [EXT+'base64-ransom-payment-phrase'], [EXT+'base64-data-theft-extortion-note', ENC])
for alignment in range(3):
    encoded = base64.b64encode(b'x'*alignment+note).decode()
    case(f'extortion-workflow-alignment-{alignment}.exe',
         pe(code=code, imports=('ReadFile', 'WriteFile', 'SetFileTime', 'DeviceIoControl', 'RmShutdown'),
            messages=(helptext, quiet, shadow, *kill, encoded)),
         new_hostile+[EXT+'base64-data-theft-extortion-note'])


def scan(item):
    path, yes, no = item
    r = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                        '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    if r.stderr.strip():
        raise AssertionError(r.stderr)
    d = json.loads(r.stdout)
    ids = {t['id'] for f in d['files'] for t in f.get('traits', [])}
    assert not yes-ids, (path.name, 'missing', sorted(yes-ids))
    assert not no & ids, (path.name, 'unexpected', sorted(no & ids))
    return {'file': path.name, 'required': sorted(yes), 'excluded': sorted(no), 'passed': True}


with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(scan, cases))
(OUT / 'regression-results.json').write_text(json.dumps(results, indent=2)+'\n')
print(f'{len(results)} static regression controls passed')
