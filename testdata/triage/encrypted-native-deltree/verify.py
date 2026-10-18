"""Generate and scan inert controls; never execute the generated files."""
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
pe_image = runpy.run_path(str(ROOT / 'testdata/native-rat-loader-triage/verify.py'))['pe_image']


def macho(code, arm=False):
    header = struct.pack('<8I', 0xfeedfacf, 0x100000c if arm else 0x1000007,
                         0 if arm else 3, 2, 1, 152, 0, 0)
    segment = struct.pack('<II16sQQQQiiII', 0x19, 152, b'__TEXT',
                          0x100000000, 0x1000, 0, 0x1000, 5, 5, 1, 0)
    section = struct.pack('<16s16sQQIIIIIIII', b'__text', b'__TEXT',
                          0x100000200, len(code), 0x200, 2, 0, 0, 0x80000400, 0, 0, 0)
    return ((header + segment + section).ljust(0x200, b'\0') + code).ljust(0x1000, b'\0')


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    dispatch = 'objectives/anti-static/obfuscation/control-flow/dispatch::'
    root = 'objectives/impact/destroy/filesystem::deltree-drive-root-destruction'
    rebuild = 'objectives/anti-static/obfuscation/payload/loader::flattened-pe-signature-restoration'
    masked = dispatch + 'masked-arithmetic-dispatch-state'
    tls = dispatch + 'tls-state-relative-table-flattening'
    # Ordinary TLS access is not a concealed dispatcher. Five full relative
    # table dispatches are required; a four-dispatch near miss stays below it.
    branch = bytes.fromhex('65 48 8B 0C 25 58 00 00 00 48 0F 44 C8 48 63 01 48 01 E8 FF E0')
    restore = bytes.fromhex('41 C6 04 07 50 66 41 C7 07 4D 5A')
    arm_state = bytes.fromhex('E9 13 40 B9 29 65 1C 1B E9 13 00 B9 E9 13 40 B9 28 01 08 4A E8 17 00 B9 72 FF FF 17')
    cases = [
        ('root-command.j', b'deltree/y \\*.*', {root}, set()),
        ('root-command.bat', b'@DELTREE /Y C:\\*.*\r\n', {root}, set()),
        ('quoted-warning.txt', b'Never run deltree/y \\*.* on your computer.', set(), {root}),
        ('selected-tree.bat', b'deltree/y C:\\cache\\*.*', set(), {root}),
        ('flattened-reconstruction.exe', pe_image(code=b'\xc3'+branch*5+restore), {tls, rebuild}, set()),
        ('four-dispatches.exe', pe_image(code=b'\xc3'+branch*4+restore), set(), {tls, rebuild}),
        ('signature-in-data.exe', pe_image(code=b'\xc3'+branch*5, data=restore), {tls}, {rebuild}),
        ('arm-masked.macho', macho(arm_state*5, True), {masked}, set()),
        ('arm-four.macho', macho(arm_state*4, True), set(), {masked}),
    ]
    for name, data, required, forbidden in cases:
        if len(sys.argv) > 2 and name not in sys.argv[2:]:
            continue
        target = dest / name
        target.write_bytes(data)
        proc = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'json', str(target)],
                              check=True, stdout=subprocess.PIPE,
                              env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        report = json.loads(proc.stdout)
        ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
        assert required <= ids, (name, 'missing', required-ids)
        assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
