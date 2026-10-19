"""Build inert byte fixtures and check capability/intent boundaries. Never execute them."""
import argparse
import concurrent.futures
import json
import struct
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
args.output_dir.mkdir(parents=True, exist_ok=True)
cases = []
FLOOD = 'micro-behaviors/communications/flood::table-indexed-datagram-loop'
KILLER = 'objectives/impact/degrade/rival-bot/competitor::multiarch-bot-procfs-rival-killer'
DOS = 'objectives/impact/dos/udp::procfs-killer-datagram-flooder'
MOTW = 'objectives/evasion/indicator-removal/ads::wsh-concealed-zone-stream-overwrite'
PADDED = 'micro-behaviors/fs/path/stream::punctuation-separated-zone-identifier'


def elf(name, arch, text=b'', rodata=b''):
    """No program headers or entry point; executable bytes are scan data only."""
    bits = 64 if arch == 'x64' else 32
    base = 0x400000 if bits == 64 else 0x8000
    b = bytearray(0x4000)
    labels = b'\0.text\0.rodata\0.shstrtab\0'
    ident = b'\x7fELF' + bytes([2 if bits == 64 else 1, 1, 1]) + b'\0' * 9
    if bits == 64:
        struct.pack_into('<16sHHIQQQIHHHHHH', b, 0, ident, 2, 62, 1,
                         0, 0, 0x3000, 0, 64, 0, 0, 64, 4, 3)
        fmt = '<IIQQQQIIQQ'
    else:
        struct.pack_into('<16sHHIIIIIHHHHHH', b, 0, ident, 2, 40, 1,
                         0, 0, 0x3000, 0, 52, 0, 0, 40, 4, 3)
        fmt = '<10I'
    for i, (label, offset, flags, content) in enumerate([
            (1, 0x1000, 6, text), (7, 0x2000, 2, rodata),
            (15, 0x2800, 0, labels)], 1):
        b[offset:offset + len(content)] = content
        struct.pack_into(fmt, b, 0x3000 + i * struct.calcsize(fmt), label,
                         3 if i == 3 else 1, flags, base + offset,
                         offset, len(content), 0, 0, 4, 0)
    path = args.output_dir / name
    path.write_bytes(b)
    return path


def case(path, matched=(), absent=()):
    cases.append({'path': str(path.resolve()), 'matched': list(matched),
                  'not_matched': list(absent)})


ssdp = (b'M-SEARCH * HTTP/1.1\r\nHOST: 255.255.255.255:1900\r\n'
        b'MAN: "ssdp:discover"\r\nMX: 1\r\n'
        b'ST: urn:dial-multiscreen-org:service:dial:1\r\n\0')
context = (ssdp + b'agent_x86\0agent_mips\0agent_arm\0/proc/%d/exe\0'
           b'/proc/%d/maps\0Killed process: %s, PID: %d\0' + b'11.22.33.44\0')
loops = {
    'x64': bytes.fromhex('89 C1 BE 0D 00 00 00 41 8B 3C 9F F7 E5 48 FF C3 C1 EA 02 0F AF D6 29 D1 48 63 C1 B9 00 40 00 00 48 C1 E0 04 48 63 90 00 00 40 00 48 8B B0 10 00 40 00 E8 00 00 00 00 4C 39 E3 75 BF 45 85 ED 7E A7'),
    'arm': bytes.fromhex('93 10 82 E0 22 21 A0 E1 02 32 A0 E1 02 31 43 E0 02 30 83 E0 00 20 63 E0 82 01 A0 E1 05 00 80 E0 82 11 95 E7 01 39 A0 E3 04 20 90 E5 04 01 98 E7 00 00 00 EB 01 40 84 E2 07 00 54 E1 ED FF FF BA 00 40 A0 E3 FB FF FF EA')}
kills = {
    'x64': bytes.fromhex('31 C0 E8 00 00 00 00 BE 09 00 00 00 89 EF E8 00 00 00 00'),
    'arm': bytes.fromhex('00 50 8D E5 00 00 00 EB 05 00 A0 E1 09 10 A0 E3 00 00 00 EB')}
wrappers = {
    'x64': bytes.fromhex('B8 3E 00 00 00 0F 05'),
    'arm': bytes.fromhex('80 40 2D E9 25 70 A0 E3 00 00 00 EF')}
for arch in loops:
    FLOOD = 'micro-behaviors/communications/flood::' + ('x64' if arch == 'x64' else 'arm') + '-table-indexed-datagram-loop'
    code = loops[arch] + b'\0' * 16 + kills[arch] + b'\0' * 16 + wrappers[arch]
    case(elf(arch + '-attack-context.elf', arch, code, context), [FLOOD, KILLER, DOS])
    case(elf(arch + '-loop-only.elf', arch, loops[arch]), [FLOOD], [KILLER, DOS])
    case(elf(arch + '-context-no-loop.elf', arch, kills[arch] + wrappers[arch], context),
         [KILLER], [FLOOD, DOS])
    case(elf(arch + '-no-sigkill.elf', arch, loops[arch] + wrappers[arch], context),
         [FLOOD], [KILLER, DOS])
    case(elf(arch + '-discovery-only.elf', arch, b'', ssdp), absent=[KILLER, DOS])
    # Identical loop bytes in a non-code section are data, not a send loop.
    case(elf(arch + '-rodata-loop.elf', arch, b'', loops[arch] + context), absent=[FLOOD, DOS])

for name, number in [('socket', 281), ('connect', 283), ('send', 289), ('recv', 291), ('sendto', 290)]:
    trait = 'micro-behaviors/communications/socket/syscall::arm-' + name + '-literal-syscall-wrapper'
    for distance in (0x28, 0x30):
        code = bytes([distance]) + bytes.fromhex('70 9F E5 00 00 00 EF')
        code += b'\0' * distance + struct.pack('<I', number)
        case(elf(f'{name}-pool-{distance:x}.elf', 'arm', code), [trait])
    # Number at +56 cannot satisfy a PC-relative load selecting +48.
    wrong = bytes.fromhex('28 70 9F E5 00 00 00 EF') + b'\0' * 48 + struct.pack('<I', number)
    case(elf(name + '-wrong-pool.elf', 'arm', wrong), absent=[trait])

empty_redirect = json.dumps('cmd /c echo. > "')
log_redirect = json.dumps('cmd /c echo. > "log.txt"')
for name, source, matched, absent in [
    ('padded-stream.js', 'var stream=":Z☍o☍n☍e.☍I☍d☍e☍n☍t☍i☍f☍i☍e☍r";', [PADDED], [MOTW]),
    ('plain-stream.js', 'var stream=":Zone.Identifier";', [], [PADDED, MOTW]),
    ('unrelated-echo.js', 'var shell=new ActiveXObject(progid); shell.Run(' + log_redirect + ');', [], [MOTW]),
    ('concealed-stream-overwrite.js', 'var shell=new ActiveXObject(progid); var stream=":Z☍o☍n☍e.☍I☍d☍e☍n☍t☍i☍f☍i☍e☍r"; var self=WScript["ScriptFullName"]; shell.Run(' + empty_redirect + '+self+stream);', [PADDED, MOTW], []),
]:
    path=args.output_dir/name;path.write_text(source);case(path,matched,absent)

# Preserve actual source launches while moving their observations by mechanism.
for name, source, trait in [
    ('inline-code.py', 'import subprocess\ncode="print(1)"\nsubprocess.run(["python", "-c", code])\n', 'micro-behaviors/process/create/eval::python-interpreter-code-argument'),
    ('self-interpreter.py', 'import subprocess,sys\nsubprocess.Popen([sys.executable, "-c", "print(1)"])\n', 'micro-behaviors/process/create/eval::sys-executable-c-popen'),
    ('bash-input.py', 'import subprocess\nsubprocess.run(["bash"], input="echo ok")\n', 'micro-behaviors/process/create/shell/stdin-feed::python-bash-stdin-script'),
    ('go-context.go', 'package main\nimport("context";"os/exec")\nfunc main(){ _ = exec.CommandContext(context.Background(), "echo", "ok") }\n', 'micro-behaviors/process/create/subprocess::go-exec-command-context'),
]:
    path = args.output_dir / name
    path.write_text(source)
    case(path, [trait])
go_cases = Path('testdata/taxonomy/go-powershell-dispatch/cases.json')
for existing in json.loads(go_cases.read_text())['fixtures']:
    case(Path(existing['path']), existing['matched'], existing['not_matched'])
manifest = args.output_dir / 'cases.json'
manifest.write_text(json.dumps({'id_map': {}, 'fixtures': cases}, indent=2) + '\n')

def check_case(case):
    result = subprocess.run([args.cleave, '--format', 'json', case['path']],
                            capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    observed = {t['id'] for f in data['files'] for t in f.get('traits', [])}
    missing = set(case['matched']) - observed
    unexpected = set(case['not_matched']) & observed
    if missing or unexpected:
        raise AssertionError((Path(case['path']).name, sorted(missing), sorted(unexpected)))
    return Path(case['path']).name

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for name in pool.map(check_case, cases):
        print('PASS', name, flush=True)
print(f'{len(cases)} boundary fixtures passed')
