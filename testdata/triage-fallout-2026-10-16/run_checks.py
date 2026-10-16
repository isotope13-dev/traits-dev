"""Static scanner controls. Sample bytes are read/modified, never executed."""
import argparse
import json
from pathlib import Path
import struct
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--samples', type=Path, required=True)
parser.add_argument('--work', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
args.work.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]


def inert_pe(data, overlay=b''):
    """A non-launchable PE with one read-only section and no entry point."""
    buf = bytearray(1024 + ((len(data) + 511) // 512) * 512)
    buf[:2] = b'MZ'
    struct.pack_into('<I', buf, 0x3c, 0x80)
    buf[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', buf, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', buf, opt, 0x10b)
    struct.pack_into('<I', buf, opt + 28, 0x400000)
    struct.pack_into('<II', buf, opt + 32, 0x1000, 0x200)
    struct.pack_into('<II', buf, opt + 56, 0x3000, 0x400)
    struct.pack_into('<H', buf, opt + 68, 2)
    struct.pack_into('<I', buf, opt + 92, 16)
    sec = opt + 224
    buf[sec:sec + 8] = b'.rdata\0\0'
    struct.pack_into('<IIII', buf, sec + 8, len(data), 0x1000, len(buf) - 1024, 1024)
    struct.pack_into('<I', buf, sec + 36, 0x40000040)
    buf[1024:1024 + len(data)] = data
    return bytes(buf) + overlay


phish = 'objectives/credential-access/financial/credit-card/keyword::pe-card-verification-phish'
persist = 'objectives/persistence/login/registry/autostart::pin-lure-shellservice-autoload'
prompt = 'micro-behaviors/ui/dialog/prompt::pe-card-number-prompt'
secret = 'micro-behaviors/data/llm/agent::skill-secret-read-instruction'
agent = 'micro-behaviors/process/argument/option::rust-agent-option-literal'
schema = 'micro-behaviors/data/serialize/schema-object::computer-field-key'
api_profile = 'micro-behaviors/process/create/exec::minimal-export-winexec-systemdir-api-profile'
rotation = 'micro-behaviors/fs/write/file/executable::self-hash-rotation-relaunch'
prompts = b'\0'.join([
    b'Please, enter your ATM PIN',
    b'Please, enter your CVV2 (3-digit code on back of card)',
    b'Please, enter your Card Number',
    b'Please, select Card (Visa/MasterCard)',
]) + b'\0'
lure = b'Unable to authorize. ATM PIN-Code is required to complete the transaction.'
malware = (args.samples / 'e0fb9ce01a68/virussign.com_0f6fe2ba7a34134947ff0f281d6254e0.vir').read_bytes()
helper = (args.samples / '5b0298a13043/5b0298a130435bef714d146cf89520138244b1ca8cd20ad4da4d09a5e0b4c2bd').read_bytes()
# Preserve the DLL's real import/export/data sections, replace its code with
# a return and padding. This is a near miss for malicious launcher inference.
dll = bytearray(malware[0x7e84:0x7e84 + 0x1a00])
dll[0x400:0xa08] = b'\xc3' + b'\x90' * (0x608 - 1)
cases = [
    ('card-form.exe', inert_pe(prompts), [prompt], [phish, persist], 0),
    ('deceptive-form.exe', inert_pe(prompts + lure + b'\0'), [prompt, phish], [], 1),
    ('overlay-only.exe', inert_pe(b'ordinary resource\0', prompts + lure + b'\0'), [], [prompt, phish], 0),
    ('api-helper.dll', bytes(dll), [api_profile], [phish, persist], 0),
    ('lure-removed.exe', malware.replace(lure, b'X' * len(lure)), [prompt], [phish, persist], 0),
    ('renamed-helper.exe', helper, [rotation], [], 0),
    ('affirmative.md', b'The agent reads secrets from the configured credential file.\n', [secret], [], 0),
    ('negative.md', b'The agent cannot read MCP secrets or their process environments.\n', [], [secret], 0),
    ('agent.rs', b'fn run() { command.arg("--agent"); }\n', [agent], [], 0),
    ('agent-user.rs', b'fn run() { command.arg("--agent-user"); }\n', [], [agent], 0),
    ('computer-prose.exe', inert_pe(b'computer\0means a hardware system\0'), [], [schema], 0),
    ('computer-record.exe', inert_pe(b'{"computer":"workstation"}\0'), [schema], [], 0),
]
results = []
for name, data, present, absent, hostile_count in cases:
    path = args.work / name
    path.write_bytes(data)
    proc = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', str(path)], capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr)
    report = json.loads(proc.stdout)
    traits = {t['id']: t for f in report['files'] for t in f['traits']}
    hostile = sorted(k for k, v in traits.items() if v['crit'] == 5)
    suspicious = sorted(k for k, v in traits.items() if v['crit'] == 4)
    missing = sorted(set(present) - traits.keys())
    unexpected = sorted(set(absent) & traits.keys())
    passed = not missing and not unexpected and len(hostile) == hostile_count
    if name == 'renamed-helper.exe':
        passed = passed and suspicious == [rotation]
    result = dict(case=name, passed=passed, missing=missing, unexpected=unexpected,
                  hostile=hostile, suspicious=suspicious)
    results.append(result)
    print(json.dumps(result))
(args.work / 'control-results.json').write_text(json.dumps(results, indent=2) + '\n')
if not all(r['passed'] for r in results):
    raise SystemExit(1)
