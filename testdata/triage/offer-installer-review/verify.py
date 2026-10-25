"""Check bound Sandboxie probes, hidden WSH templates and neutral wording.

Run: python3 testdata/triage/offer-installer-review/verify.py <scratch-directory>
Generated PE entry points are RET; probe excerpts are never executed.
"""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
source = ROOT / 'testdata/taxonomy/reasoned-input-review/verify.py'
saved_args = sys.argv
sys.argv = [str(source), str(OUT / 'existing')]
namespace = runpy.run_path(str(source))
sys.argv = saved_args
image = namespace['image']
SANDBOX = 'objectives/anti-analysis/sandbox-detect/artifact/known::x86-sandboxie-module-presence-probe'
HIDDEN = 'micro-behaviors/process/create/flags::wscript-shell-run-hidden-window'
IDENTITY = 'well-known/tool/sysadmin/sandboxie::sandboxie-component'
CPUID = 'micro-behaviors/os/virtualization/hypervisor::cpuid-hypervisor-vendor-query'
CANCEL = 'micro-behaviors/communications/transfer::bitsadmin-cancel-command-text'
CASES = []


def case(name, data, yes=(), no=()):
    path = OUT / name
    path.write_bytes(data)
    CASES.append((path, set(yes), set(no)))


def wide_probe(wrong_module=False, wrong_api=False, no_test=False):
    data = bytearray(image(wrong_module=wrong_module, wrong_api=wrong_api))
    data = data.replace(b'GetModuleHandleA\0', b'GetModuleHandleW\0')
    module = 'SbieDll\0'.encode('utf-16le')
    data[0x450:0x450 + len(module)] = module
    data[0x21b:0x227] = bytes.fromhex('90 90 74 06 6a 07 58 c3 33 c0 c3 90' if no_test else
                                            '85 c0 74 06 6a 07 58 c3 33 c0 c3 90')
    return bytes(data)


case('wide-short-conditional-probe.exe', wide_probe(), [SANDBOX], [IDENTITY])
case('wide-unrelated-module.exe', wide_probe(wrong_module=True), [], [SANDBOX, IDENTITY])
case('wide-unrelated-api.exe', wide_probe(wrong_api=True), [], [SANDBOX, IDENTITY])
case('wide-no-presence-test.exe', wide_probe(no_test=True), [], [SANDBOX, IDENTITY])
# Both observed instruction orders must retain the same neutral query fact.
for name, code in [('cpuid-clear-first.exe', '33 c9 89 45 e8 b8 00 00 00 40 0f a2'),
                   ('cpuid-clear-last.exe', 'b8 00 00 00 40 33 c9 53 0f a2')]:
    data = bytearray(image(wrong_module=True))
    code = bytes.fromhex(code)
    data[0x290:0x290 + len(code)] = code
    case(name, bytes(data), [CPUID], [SANDBOX])
data = bytearray(image(wrong_module=True))
code = bytes.fromhex('33 c9 89 45 e8 b8 01 00 00 00 0f a2')
data[0x290:0x290 + len(code)] = code
case('ordinary-cpu-feature-leaf.exe', bytes(data), [], [CPUID])
script = 'Set WshShell = CreateObject("WScript.Shell")\r\ncmds=WshShell.RUN("%s",0,False)\r\ncmds=WshShell.RUN("bitsadmin /cancel %s",0,False)'
data = bytearray(image(wrong_module=True))
encoded = (script + '\0').encode('utf-16le')
data[0xb00:0xb00 + len(encoded)] = encoded
case('embedded-hidden-wsh.exe', bytes(data), [HIDDEN, CANCEL], [SANDBOX])
case('cancel-job.cmd', b'bitsadmin.exe /cancel transferJob\r\n', [CANCEL])
case('transfer-job.cmd', b'bitsadmin /transfer job /download https://example.org/file C:\\file\r\n', [], [CANCEL])
case('unrelated-run.js', b'const label = "Other.Shell"; worker.Run("job", 0, false);', [], [HIDDEN])
case('ordinary-operation-label.js', b'const span = { operation: "pressKey" };',
     ['metadata/lang/source/naming/resource::press-key-operation-label'],
     ['objectives/command-and-control/remote-command/socketio-control::socketio-event-press-key'])
case('dataset-api-doc.js', b'/** Delete a dataset by ID. */\nfunction deleteDataset(id) {}',
     ['metadata/lang/natural/phrasing::dataset-delete-encrypt-wording'],
     ['objectives/impact/ransom/encrypt/runtime-generated::llm-generated-ransomware-code'])
case('n8n-execution-config.js', b'const mode = process.env.EXECUTIONS_MODE;',
     ['micro-behaviors/os/env/provider::n8n-runtime-env-reference'])
proc = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                       '--disable', 'third-party,radare2', '--json',
                       *[str(p) for p, _, _ in CASES]], capture_output=True, text=True)
if proc.returncode:
    raise RuntimeError(proc.stderr)
reports = [json.loads(line) for line in proc.stdout.split('\n') if line.strip()]
files = [f for report in reports for f in report.get('files', [report])]
for path, yes, no in CASES:
    matched = [f for f in files if Path(f['path']).name == path.name]
    assert matched, (path.name, 'missing report')
    traits = {t['id'] for f in matched for t in f.get('findings', f.get('traits', []))}
    assert yes <= traits, (path.name, 'missing', yes - traits)
    assert not no & traits, (path.name, 'unexpected', no & traits)
    print(path.name, 'PASS')
(OUT / 'results.json').write_text(json.dumps({'cases': len(CASES), 'passed': True}, indent=2) + '\n')
