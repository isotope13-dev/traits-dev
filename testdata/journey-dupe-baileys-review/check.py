"""Static regressions; never import, install or execute a specimen."""
import argparse
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--dupe', type=Path, required=True)
a = parser.parse_args()
repo = Path(__file__).resolve().parents[2]
fixtures = Path(__file__).resolve().parent
relay = 'objectives/command-and-control/reverse-shell/stream-bridge::python-select-interactive-shell-relay'
getter = 'objectives/credential-access/gaming/minecraft::difference-built-token-getter-builder'
field = 'micro-behaviors/data/format/json::jvm-difference-session-id-json-fragments'
launch = 'objectives/execution/payload/file-exec::fabric-obfuscated-token-png-launcher'
upload = 'objectives/exfiltration/stealer/token::fabric-png-loader-session-upload'

def scan(path):
    run = subprocess.run([a.cleave, '--traits-dir', str(repo), '--format', 'json', 'analyze', str(path)],
                         capture_output=True, text=True, check=True, timeout=180)
    d = json.loads(run.stdout)
    return {t['id']: t for f in d['files'] for t in f.get('traits', [])}

with tempfile.TemporaryDirectory(prefix='fallout-static-') as temp:
    temp = Path(temp)
    src = (fixtures / 'relay.py').read_text()
    variants = {
        'relay': (src, True),
        'renamed-relay': (src.replace('peer', 'channel').replace('child', 'worker')
                           .replace('source', 'stream').replace('buffer', 'chunk'), True),
        'different-buffer': (src.replace('peer.sendall(buffer)', 'peer.sendall(other)'), False),
        'non-shell-child': (src.replace('["/bin/bash", "-i"]', '["cat"]'), False),
        'no-socket-dial': (src.replace('socket.create_connection', 'get_test_peer'), False),
        'no-conditional-read': (src.replace('source.recv(4096) if source is peer else os.read(source.fileno(), 4096)',
                                              'os.read(source.fileno(), 4096)'), False),
    }
    for name, (source, expected) in variants.items():
        p = temp / (name + '.py'); p.write_text(source)
        assert (relay in scan(p)) == expected, name
        print('PASS', name)
    p = temp / 'setup.py'; p.write_text((fixtures / 'setup.py').read_text())
    traits = scan(p)
    assert not [t for t in traits.values() if t['crit'] >= 4], 'ordinary build conviction'
    required = {
        'micro-behaviors/communications/ip/literal::setup-command-http-ip-cooccurrence',
        'micro-behaviors/communications/http/client/library::setup-command-http-body-cooccurrence',
        'micro-behaviors/os/env/config::setup-database-url-setting',
        'micro-behaviors/process/create/subprocess::run-ast',
    }
    assert required <= traits.keys(), required - traits.keys()
    print('PASS build status near miss: network, execution and database facts retained')
    with zipfile.ZipFile(a.dupe) as z:
        raw = z.read('net/fabric/fwJsU.class')
        # Mutate immediate operands, never execute the class. The same five
        # decoded getter characters survive different arithmetic constants.
        pattern = re.compile(b'\x19.\x11..\x11..\x64\x92\xb6..\x57', re.S)
        transformed = bytearray(raw)
        for m in pattern.finditer(raw):
            for offset in (3, 6):
                value = struct.unpack_from('>h', raw, m.start() + offset)[0]
                if value < 32767:
                    struct.pack_into('>h', transformed, m.start() + offset, value + 1)
        p = temp / 'ChangedOperands.class'; p.write_bytes(transformed)
        assert getter in scan(p), 'operand-dependent signature'
        print('PASS arithmetic operands can change')
        # Mutate the immediate T in the 14-character getter builder only.
        blocks = list(re.finditer(b'(?:\x19.[\x11\x13]..[\x11\x13]..\x64\x92\xb6..\x57){14}', raw, re.S))
        expected = ((1, 101), (4, 99), (6, 101), (9, 84), (11, 107))
        blocks = [m for m in blocks if all(
            raw[m.start()+i*14+2] == 0x11 and raw[m.start()+i*14+5] == 0x11
            and struct.unpack_from('>h', raw, m.start()+i*14+3)[0]
                - struct.unpack_from('>h', raw, m.start()+i*14+6)[0] == value
            for i, value in expected)]
        assert len(blocks) == 1
        changed = bytearray(raw); offset = blocks[0].start() + 9 * 14 + 4
        changed[offset] ^= 1
        p = temp / 'OtherGetter.class'; p.write_bytes(changed)
        assert getter not in scan(p), 'getter semantic near miss'
        print('PASS changed getter character rejected')
        p = temp / 'Renamed.jar'
        with zipfile.ZipFile(p, 'w') as out:
            for info in z.infolist():
                data = z.read(info.filename)
                if info.filename.endswith(('.class', '.json', '.MF')):
                    data = data.replace(b'net/fabric', b'pkg/hidden').replace(b'net.fabric', b'pkg.hidden')
                out.writestr(info.filename.replace('net/fabric', 'pkg/hidden'), data)
        assert {launch, upload, getter, field} <= scan(p).keys()
        print('PASS renamed package namespace retains payload and theft coverage')
print('PASS all static regression checks')
