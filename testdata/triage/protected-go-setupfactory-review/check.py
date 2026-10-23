"""Static regression controls. Never executes specimen instructions.

Usage: python3 check.py AGENT REVIEW_SCRATCH
REVIEW_SCRATCH contains 1-go-functions.json and the recovered installer files.
"""
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

import pefile

agent = Path(sys.argv[1]).read_bytes()
assert hashlib.sha256(agent).hexdigest() == '41a5625a68c026160dcd3db49adefb60b372c553812ee965f009d0f451daf841'
root = Path(sys.argv[2])
controls = root / 'controls'
controls.mkdir(exist_ok=True)
pe = pefile.PE(data=agent)
base = pe.OPTIONAL_HEADER.ImageBase
image = pe.get_memory_mapped_image()
header = image.index(b'\xf1\xff\xff\xff\0\0\1\10')
count, _, text, names, _, _, _, table = struct.unpack_from('<8Q', image, header + 8)
assert 0 < count < 100000
functions = []
for i in range(count):
    entry, offset = struct.unpack_from('<II', image, header + table + i * 8)
    name_offset = struct.unpack_from('<i', image, header + table + offset + 4)[0]
    at = header + names + name_offset
    name = image[at:image.index(b'\0', at)].decode()
    end = struct.unpack_from('<I', image, header + table + (i + 1) * 8)[0]
    functions.append(dict(name=name, va=text + entry, size=end - entry))
c2 = 'objectives/command-and-control/remote-command/dispatch::anti-analysis-websocket-script-agent'
persist = 'objectives/persistence/login/registry/run-key::anti-analysis-websocket-agent-run-key'
trust = 'objectives/evasion/security-bypass/cert-store::anti-analysis-websocket-agent-root-install'
reader = 'micro-behaviors/communications/websocket/receive::go-websocket-read-dispatch-calls'
curl = 'objectives/anti-static/obfuscation/payload/fake-curl-dll::curl-export-memory-execution-loader'
dump = 'micro-behaviors/process/debug/dump::admin-manifest-minidump-api-profile'
kernel = 'micro-behaviors/process/terminate/kill::kernel-process-termination'
device = 'micro-behaviors/process/terminate/kill::kernel-device-process-termination-api-profile'
proxy = 'objectives/evasion/hijack-execution-flow/dll-hijacking/container::tampered-signed-opaque-import-proxy'
opaque = 'objectives/anti-static/obfuscation/name-mangling/export-name::sparse-packed-random-export-dll'
cases = []


def add(name, data, yes=(), no=()):
    path = controls / name
    path.write_bytes(data)
    cases.append((path, dict(yes), set(no)))


def remove_calls(caller_suffix, callee_suffix):
    caller = next(f for f in functions if f['name'].endswith(caller_suffix))
    targets = {f['va'] for f in functions if f['name'].endswith(callee_suffix)}
    changed = bytearray(agent)
    start = pe.get_offset_from_rva(caller['va'] - base)
    count = 0
    for at in range(start, start + caller['size'] - 4):
        if changed[at] == 0xe8:
            target = caller['va'] + at - start + 5 + struct.unpack_from('<i', changed, at + 1)[0]
            if target in targets:
                changed[at:at + 5] = b'\x90' * 5
                count += 1
    assert count
    return changed


all_agent = {c2: 5, persist: 5, trust: 5, reader: 3}
add('renamed-agent.exe', agent, all_agent.items())
add('different-package-owner.exe', agent.replace(b'core/cmd/agent/', b'else/cmd/owner/'), all_agent.items())
for name, caller, callee in [
    ('no-websocket-read', 'main.readLoop', 'websocket.(*Conn).Read'),
    ('no-dispatch', 'main.readLoop', 'handlers.(*Dispatcher).Dispatch'),
    ('no-script-exec', 'handlers.executeScript', 'os/exec.CommandContext'),
    ('no-antidebug', 'protect.RunChecks', 'protect.antiDebug'),
]:
    add(name + '.exe', remove_calls(caller, callee), no=(c2, persist, trust))
add('no-registry-writer.exe', remove_calls('persistence.Setup', 'registry.Key.setStringValue'),
    ((c2, 5), (trust, 5)), (persist,))
changed = bytearray(agent)
pos = pe.get_offset_from_rva(0x402950)
assert changed[pos:pos + 4] == b'ROOT'
changed[pos:pos + 4] = b'MYCA'
add('different-cert-store.exe', changed, ((c2, 5), (persist, 5)), (trust,))
add('unstructured-name-strings.exe', agent.replace(b'\xf1\xff\xff\xff\0\0\1\10', b'\0' * 8),
    no=(c2, persist, trust, reader))

# Real support components: suspicious signature inconsistency and legitimate
# process APIs survive, while neither a fake curl proxy nor credential theft
# is inferred from an elevated repair application.
add('repair.exe', (root / 'sha256-unpacked.exe').read_bytes(), ((dump, 3),), (curl,))
add('repair-with-dll-flag.dll', (root / 'repair-with-dll-flag.dll').read_bytes(), ((dump, 3),), (curl,))
add('security-driver.sys', (root / 'huorong/$SYSDIR/drivers/sysdiag.sys').read_bytes(),
    ((kernel, 4), (device, 4)))
host = (root / 'B11CWynFd.exe').read_bytes()
host_pe = pefile.PE(data=host)
add('renamed-proxy-host.exe', host, ((proxy, 5),))
add('renamed-sidecar.d', (root / 'hLzpZBD.d').read_bytes(), ((opaque, 5),))
changed = bytearray(host)
at = host_pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].get_file_offset()
changed[at:at + 8] = bytes(8)
add('unsigned-import-proxy.exe', changed, no=(proxy,))
changed = bytearray(host)
section = host_pe.sections[0]
changed[section.PointerToRawData:section.PointerToRawData + section.SizeOfRawData] = bytes(section.SizeOfRawData)
add('ordinary-code-import-proxy.exe', changed, no=(proxy,))
changed = bytearray(host)
for library in host_pe.DIRECTORY_ENTRY_IMPORT:
    for symbol in library.imports:
        at = host_pe.get_offset_from_rva(symbol.hint_name_table_rva) + 2
        changed[at:at + len(symbol.name)] = b'A' * len(symbol.name)
add('ordinary-import-names.exe', changed, no=(proxy,))

# A small inert hollow-curl DLL is a retained positive for the narrowed rule.
# This fixture contains API tables only; the entry point returns immediately.
def block(key, value=b'', children=b'', text=False):
    out = bytearray(struct.pack('<HHH', 0, len(value) // 2 if text else len(value), int(text)))
    out += key.encode('utf-16le') + b'\0\0'
    out += b'\0' * (-len(out) % 4)
    out += value
    out += b'\0' * (-len(out) % 4)
    out += children
    struct.pack_into('<H', out, 0, len(out))
    return bytes(out)


def curl_fixture(network=False):
    h = bytearray(0x200)
    h[:2] = b'MZ'
    struct.pack_into('<I', h, 0x3c, 0x80)
    h[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', h, 0x84, 0x14c, 3, 0, 0, 0, 0xe0, 0x2102)
    o = 0x98
    struct.pack_into('<H', h, o, 0x10b)
    struct.pack_into('<III', h, o + 16, 0x1000, 0x1000, 0x2000)
    struct.pack_into('<III', h, o + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<II', h, o + 56, 0x4000, 0x200)
    struct.pack_into('<HH', h, o + 68, 2, 0x140)
    struct.pack_into('<I', h, o + 92, 16)
    struct.pack_into('<II', h, o + 96, 0x2400, 0x200)
    struct.pack_into('<II', h, o + 104, 0x2000, 40)
    struct.pack_into('<II', h, o + 112, 0x3000, 0x400)
    for i, (name, rva, off, size, flags) in enumerate([
        (b'.text', 0x1000, 0x200, 0x200, 0x60000020),
        (b'.rdata', 0x2000, 0x400, 0x1000, 0x40000040),
        (b'.rsrc', 0x3000, 0x1400, 0x400, 0x40000040),
    ]):
        struct.pack_into('<8sIIIIIIHHI', h, o + 0xe0 + i * 40, name, size, rva, size, off, 0, 0, 0, 0, flags)
    d = bytearray(0x1000)
    struct.pack_into('<IIIII', d, 0, 0x2040, 0, 0, 0x20d0, 0x2090)
    d[0xd0:0xdd] = b'kernel32.dll\0'
    names = ['VirtualAlloc', 'VirtualProtect', 'GetProcAddress', 'GetModuleHandleA', 'CreateThread']
    if network:
        names += ['WSAStartup']
    at = 0x100
    for j, name in enumerate(names):
        struct.pack_into('<I', d, 0x40 + j * 4, 0x2000 + at)
        struct.pack_into('<I', d, 0x90 + j * 4, 0x2000 + at)
        value = b'\0\0' + name.encode() + b'\0'
        d[at:at + len(value)] = value
        at += len(value) + len(value) % 2
    struct.pack_into('<IIHHIIIIIII', d, 0x400, 0, 0, 0, 0, 0x2490, 1, 3, 3, 0x2440, 0x2460, 0x2480)
    d[0x490:0x49b] = b'loader.dll\0'
    at = 0x4b0
    for j, name in enumerate(['curl_easy_init', 'curl_easy_perform', 'curl_easy_cleanup']):
        struct.pack_into('<I', d, 0x440 + j * 4, 0x1000)
        struct.pack_into('<I', d, 0x460 + j * 4, 0x2000 + at)
        struct.pack_into('<H', d, 0x480 + j * 2, j)
        value = name.encode() + b'\0'
        d[at:at + len(value)] = value
        at += len(value)
    version = block('VS_VERSION_INFO', struct.pack('<13I', 0xfeef04bd, 0x10000, *([0] * 11)),
                    block('StringFileInfo', children=block('040904B0', children=
                          block('OriginalFilename', 'libcurl.dll\0'.encode('utf-16le'), text=True))))
    r = bytearray(0x400)
    for directory, ident, target in [(0, 16, 0x80000018), (0x18, 1, 0x80000030), (0x30, 0x409, 0x48)]:
        struct.pack_into('<IIHHHH', r, directory, 0, 0, 0, 0, 0, 1)
        struct.pack_into('<II', r, directory + 16, ident, target)
    struct.pack_into('<IIII', r, 0x48, 0x3058, len(version), 0, 0)
    r[0x58:0x58 + len(version)] = version
    return bytes(h) + b'\xc3' + bytes(0x1ff) + bytes(d) + bytes(r)


add('hollow-curl.dll', curl_fixture(), ((curl, 5),))
add('network-curl.dll', curl_fixture(True), no=(curl,))
add('hollow-curl.exe', curl_fixture().replace(b'\x02\x21', b'\x02\x01', 1), no=(curl,))

env = dict(os.environ, SCAN_HOPPER='', SCAN_FOLLOW='none', CLEAVE_TRAITS_DIR=str(Path.cwd()))
proc = subprocess.run(['atomscan', '--no-update', '--mode', 'slow', '--format', 'json'] +
                      [str(c[0]) for c in cases], env=env, capture_output=True, text=True)
(root / 'controls-scan.log').write_text(proc.stderr)
reports = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith('{')]
found = {r['raw']['files'][0]['path']: {t['id']: t['crit'] for f in r['raw']['files'] for t in f['traits']} for r in reports}
assert len(found) == len(cases), (len(found), len(cases), proc.stderr)
result = []
for path, yes, no in cases:
    got = found[str(path)]
    assert all(got.get(k) == v for k, v in yes.items()), (path.name, yes, {k: got.get(k) for k in yes})
    assert not no.intersection(got), (path.name, no.intersection(got))
    result.append(dict(case=path.name, required=yes, forbidden=sorted(no), passed=True))
(root / 'control-results.json').write_text(json.dumps(result, indent=2) + '\n')
print(len(result), 'static relationship controls passed')
