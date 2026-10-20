#!/usr/bin/env python3
"""Non-runnable PE controls: call binding, parasite roles, and URL severity.

Entry is a RET, snippets have no import table, and no payload is included.
Run with python3 testdata/triage/rc4-ramnit-native/check.py.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
PARTS = {
    'mapper': bytes.fromhex('51 8b 44 24 08 53 55 56 66 81 38 4d 5a 57 74 08 5f 5e 5d 33 c0 5b 59 c3 8b 78 3c 03 f8 89 7c 24 10 81 3f 50 45 00 00 74 08 5f 5e 5d 33 c0 5b 59 c3 8b 47 50 8b 4f 34 8b 35 24 30 40 00 6a 04 68 00 20 00 00 50 51 ff d6 8b e8 85 ed 75 1a 8b 57 50 6a 04 68 00 20 00 00 52 50 ff d6 8b e8 85 ed 75 06 5f 5e 5d 5b 59 c3 6a 14 6a 00 ff 15 28 30 40 00 50 ff 15 2c 30 40 00 8b d8 33 c0 6a 04 68 00 10 00 00 89 6b 04 89 43 0c 89 43 08 89 43 10 8b 47 50 50 55 ff d6 8b 4f 54 6a 04 68 00 10 00 00 51 55 ff d6 8b 74 24 18 8b 57 54 8b f8 53 8b 4e 3c 03 ca 8b d1 c1 e9 02 f3 a5 8b ca 83 e1 03 f3 a4 8b 4c 24 1c 8b 74 24 14 56 51 8b 51 3c 03 c2 89 03 89 68 34 e8 75 00 00 00 8b 4e 34 8b c5 83 c4 0c 2b c1 74 0a 50 53 e8 f2 01 00 00 83 c4 08 53 e8 69 02 00 00 83 c4 04 85 c0 74 23 53 e8 1c 01 00 00 8b 03 83 c4 04 8b 40 28 85 c0 74 29 03 c5 85 c0 74 0b 6a 00 6a 01 55 ff d0 85 c0 75 11 53 e8 09 04 00 00 83 c4 04 33 c0 5f 5e 5d 5b 59 c3 c7 43 10 01 00 00 00 5f 5e 8b c3 5d 5b 59 c3'),
    'prga': bytes.fromhex('8b 44 24 0c 56 57 33 c9 33 f6 33 ff 85 c0 76 7c 8b 44 24 0c 53 55 8b 6c 24 18 41 81 e1 ff 00 00 80 79 08 49 81 c9 00 ff ff ff 41 8a 14 01 8b da 81 e3 ff 00 00 00 03 f3 81 e6 ff 00 00 80 79 08 4e 81 ce 00 ff ff ff 46 8a 1c 06 88 54 24 18 88 1c 01 8b 5c 24 18 88 14 06 33 d2 8a 14 01 81 e3 ff 00 00 00 03 d3 81 e2 ff 00 00 80 79 08 4a 81 ca 00 ff ff ff 42 8a 14 02 8a 1c 2f 32 da 8b 54 24 1c 88 1c 2f 47 3b fa 72 90 5d 5b 5f 5e c3'),
    'wrapper': bytes.fromhex('81 ec 0c 01 00 00 b0 39 6a 0a 88 44 24 0b 88 44 24 0c 8d 44 24 04 8d 4c 24 10 50 51 c6 44 24 0c 4b c6 44 24 0d 6f c6 44 24 0e 74 c6 44 24 0f 68 c6 44 24 10 65 c6 44 24 11 72 c6 44 24 12 35 c6 44 24 15 00 e8 67 f8 ff ff 8b 94 24 20 01 00 00 8b 84 24 1c 01 00 00 52 8d 4c 24 1c 50 51 e8 ed f8 ff ff 81 c4 24 01 00 00 c3'),
    'chain': bytes.fromhex('55 83 e1 03 53 f3 a4 89 44 24 1c e8 e2 fe ff ff 53 e8 cc f1 ff ff 8b f0 83 c4 10 85 f6'),
    'arithmetic': bytes.fromhex('8b 4c 24 08 8a 14 08 80 c2 7a 88 14 08 8b 4c 24 08 8a 14 08 80 f2 59 88 14 08 40 3b c6 7c e1'),
    'prologue': bytes.fromhex('60 e8 00 00 00 00 5d 8b c5 81 ed 32 6f 01 20 2b 85 50 72 01 20 89 85 4c 72 01 20 b0 00 86 85 9e 74 01 20 3c 01 0f 85 de 02 00 00'),
    'dropper': bytes.fromhex('0b d2 75 07 8b 95 60 72 01 20 4a 8a 9c 2a 64 72 01 20 32 1f 88 1f 47 4a e2 e6 68 ff 00 00 00 8d 85 92 72 01 20 50 6a 00 ff 95 0e 74 01 20 8b c8 8d 9d 92 72 01 20 03 c3 fd 8b f8 b0 2e f2 ae 47 fc 8d b5 8a 72 01 20 b9 08 00 00 00 f3 a4 6a 00 68 80 00 00 00 6a 02 6a 00 6a 02 68 00 00 00 40 8d 85 92 72 01 20 50 ff 95 06 74 01 20 83 f8 ff 0f 84 86 00 00 00 50 8b d0 6a 00 8d 85 48 72 01 20 50 ff b5 9a 74 01 20 8d 9d 9e 74 01 20 43 53 52 ff 95 0a 74 01 20 ff 95 fa 73 01 20 fc b9 44 00 00 00 8d bd 92 73 01 20 b0 00 f3 aa b9 10 00 00 00 8d bd d6 73 01 20 b0 00 f3 aa 8d 85 d6 73 01 20 50 8d 85 92 73 01 20 50 6a 00 6a 00 6a 00 6a 00 6a 00 6a 00 8d 85 92 72 01 20 50 6a 00 ff 95 12 74 01 20'),
    'resume': bytes.fromhex('8b 85 4c 72 01 20 2b 85 54 72 01 20 89 44 24 1c 61 ff e0'),
}

MAP = "micro-behaviors/process/deploy/image-map::x86-rc4-buffer-to-manual-pe-map"
LOAD = "objectives/command-and-control/dropper/image-map::concealed-rc4-native-image-loader"
PARASITE = "objectives/impact/infect/virus::x86-xor-sibling-drop-launch-host-resume"
RAMNIT = "well-known/malware/worm/ramnit::ramnit-sibling-dropper"
DLL = "micro-behaviors/communications/http/url/path::http-dll-url-in-binary"
IP = "micro-behaviors/communications/http/url/external-ip::url-external-ip-binary"
LOOPBACK = "micro-behaviors/communications/http/url/host::loopback-client-url-cooccurrence"
OLD_LOOPBACK = "micro-behaviors/communications/http/url/path::loopback-client-url-cooccurrence"


def pe():
    image = bytearray(0x2800)
    image[:2] = b"MZ"
    struct.pack_into("<I", image, 0x3c, 0x80)
    image[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", image, 0x84, 0x14c, 2, 0, 0, 0, 0xe0, 0x102)
    o = 0x98
    struct.pack_into("<H", image, o, 0x10b)
    struct.pack_into("<III", image, o + 16, 0x2f00, 0x1000, 0x3000)
    struct.pack_into("<III", image, o + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into("<II", image, o + 56, 0x4000, 0x400)
    struct.pack_into("<H", image, o + 68, 2)
    struct.pack_into("<I", image, o + 92, 16)
    for i, (name, va, raw, size, flags) in enumerate([
        (b".text", 0x1000, 0x400, 0x2000, 0x60000020),
        (b".data", 0x3000, 0x2400, 0x400, 0xc0000040),
    ]):
        struct.pack_into("<8sIIIIIIHHI", image, o + 0xe0 + 40*i,
                         name, size, va, size, raw, 0, 0, 0, 0, flags)
    image[0x2300] = 0xc3
    return image


def loader(shift=0):
    image = pe()
    positions = {"mapper": 0x400, "prga": 0xa60, "wrapper": 0x1110,
                 "chain": 0x121e, "arithmetic": 0xdad}
    for key, offset in positions.items():
        image[offset+shift:offset+shift+len(PARTS[key])] = PARTS[key]
    blob = b"q"*28 + b"+" + b"r"*48 + b"="
    image[0x2400:0x2400+len(blob)] = blob
    return image


def parasite():
    image = pe() + bytearray(0x400)
    for key, offset in [("prologue",0x2800),("dropper",0x2a01),("resume",0x2b09)]:
        image[offset:offset+len(PARTS[key])] = PARTS[key]
    return image


cases = {}
def add(name, data, required=None, forbidden=()):
    cases[name] = (bytes(data), required or {}, set(forbidden))

add("linked-loader.exe", loader(), {MAP:3, LOAD:5})
a=loader(0x80)
# Rotate compiler immediates and stack key bytes without requiring a URL.
a[0xdad+0x80+9] ^= 0x31
a[0xdad+0x80+22] ^= 0x22
a[0x1110+0x80+7] ^= 0x12
add("relocated-key-variant.exe", a, {MAP:3, LOAD:5})
for name, offset in [("wrong-transform-target",0x122a),("wrong-mapper-target",0x1230),
                     ("wrong-prga-target",0x116f)]:
    a=loader();a[offset] ^= 1
    add(name+".exe",a,forbidden=[MAP,LOAD])
a=loader();a[0xdad:0xdad+len(PARTS["arithmetic"])] = b"\0"*len(PARTS["arithmetic"])
add("unconcealed-crypto-mapper.exe",a,{MAP:3},[LOAD])
a=loader();a[0x50b] = 0x90
add("header-parser-without-entry-call.exe",a,forbidden=[MAP,LOAD])
add("parasite.exe",parasite(),{PARASITE:5,RAMNIT:5})
a=parasite();a[0x2b09:0x2b1c] = b"\0"*len(PARTS["resume"])
add("no-host-resume.exe",a,forbidden=[PARASITE,RAMNIT])
a=parasite();a[0x2800:0x282b] = b"\0"*len(PARTS["prologue"])
add("no-family-prologue.exe",a,{PARASITE:5},[RAMNIT])
a=parasite();a[0x2ae0] ^= 1
add("no-process-launch.exe",a,forbidden=[PARASITE,RAMNIT])
for name,url,required,forbidden in [
    ("domain-dll",b"https://assets.invalid/path/plugin.DLL?v=2",{DLL:4},[IP]),
    ("public-ip-dll",b"http://205.209.162.14/NetSyst96.dll",{DLL:4,IP:4},[]),
    ("public-ip-status",b"http://93.184.216.34/status",{IP:4},[DLL]),
    ("loopback",b"http://127.0.0.1/status",{},[IP,DLL]),
    ("private-ip",b"http://10.1.2.3/status",{},[IP,DLL]),
    ("bad-ip",b"http://999.999.999.999/status",{},[IP,DLL]),
    ("dll-documentation",b"https://docs.invalid/plugin.dll.html",{},[DLL,IP]),
    ("dll-query-only",b"https://docs.invalid/page?name=plugin.dll",{},[DLL,IP]),
    ("dll-hostname",b"https://example.dll/guide",{},[DLL,IP]),
]:
    a=pe();a[0x2400:0x2400+len(url)] = url
    add(name+".exe",a,required,forbidden)
add("loopback-client.py",b"import requests\nrequests.get('http://127.0.0.1/status')\n",{LOOPBACK:3},[OLD_LOOPBACK])
add("loopback-reference.py",b"URL='http://127.0.0.1/status'\n",{},[LOOPBACK,OLD_LOOPBACK])

with tempfile.TemporaryDirectory(prefix="native-rc4-controls-") as temp:
    directory=Path(temp)
    for name,(content,_,_) in cases.items(): (directory/name).write_bytes(content)
    result=subprocess.run([os.environ.get("CLEAVE","cleave"),"--traits-dir",str(ROOT),
        "--format","jsonl",str(directory)],text=True,capture_output=True,check=True)
    reports=[f for line in result.stdout.splitlines() for f in json.loads(line)["files"]]
    assert len(reports)==len(cases),(len(reports),len(cases),result.stderr)
    for report in reports:
        name=Path(report["path"]).name
        _,required,forbidden=cases[name]
        emitted={t["id"]:t["crit"] for t in report["traits"]}
        for trait,crit in required.items(): assert emitted.get(trait)==crit,(name,trait,crit,emitted.get(trait))
        assert not forbidden & emitted.keys(),(name,forbidden & emitted.keys())
    print(f"Passed {len(cases)} native loader, parasite, URL and relocation controls")
