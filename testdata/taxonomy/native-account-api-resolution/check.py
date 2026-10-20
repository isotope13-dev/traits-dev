"""Inert PE controls binding API names and imported calls to resolver code."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
USER = "micro-behaviors/os/user/account::net-user-add-resolved-global"
GROUP = "micro-behaviors/os/group/membership::net-local-group-add-members-resolved-global"
PROFILE = "micro-behaviors/os/user/account::resolved-admin-account-api-set"
TARGETS = {USER, GROUP, PROFILE}


def image(*, code=True, admin=True, user=True, wrong_target=False,
          wrong_call=False, outside_text=False, also_imported=False):
    # A RET entry point, two never-executed resolver thunks, read-only names,
    # real import descriptors/thunks, and writable global pointer slots.
    data = bytearray(0xe00)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 0x3c, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", data, 0x84, 0x14c, 3, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into("<H", data, opt, 0x10b)
    for off, value in {16:0x1000,20:0x1000,24:0x2000,28:0x400000,
                       32:0x1000,36:0x200,56:0x4000,60:0x200,
                       68:3,92:16,104:0x2200,108:40}.items():
        struct.pack_into("<I", data, opt+off, value)
    for index, (name, rva, raw, size, flags) in enumerate([
        (b".text",0x1000,0x200,0x200,0x60000020),
        (b".rdata",0x2000,0x400,0x800,0x40000040),
        (b".data",0x3000,0xc00,0x200,0xc0000040),
    ]):
        struct.pack_into("<8sIIIIIIHHI", data, opt+224+index*40,
                         name,size,rva,size,raw,0,0,0,0,flags)
    for raw, value in [
        (0x420,b"NetUserAdd" if user else b"NetUserGet"),
        (0x440,b"NetLocalGroupAddMembers"),
        (0x480,"NETAPI32.dll".encode("utf-16le")),
        (0x4b0,b"Administrators" if admin else b"Users"),
    ]:
        data[raw:raw+len(value)] = value
    struct.pack_into("<IIIII",data,0x600,0x2280,0,0,0x2240,0x22c0)
    data[0x640:0x64d] = b"KERNEL32.dll\0"
    imports = ["LoadLibraryW","GetProcAddress"]
    if also_imported:
        imports += ["NetUserAdd","NetLocalGroupAddMembers"]
    cursor = 0x700
    for index, name in enumerate(imports):
        value = b"\0\0"+name.encode()+b"\0"
        data[cursor:cursor+len(value)] = value
        struct.pack_into("<I",data,0x680+index*4,cursor+0x1c00)
        struct.pack_into("<I",data,0x6c0+index*4,cursor+0x1c00)
        cursor += len(value)
    data[0x200] = 0xc3
    if code:
        for index, target in enumerate([0x402020,0x402040]):
            if wrong_target and index == 0:
                target = 0x4020b0  # Administrator text is not an API name.
            lookup = 0x4022c0 if wrong_call else 0x4022c4
            thunk = (b"\x68"+struct.pack("<I",target)+b"\x68"+
                     struct.pack("<I",0x402080)+b"\xff\x15"+
                     struct.pack("<I",0x4022c0)+b"\x50\xff\x15"+
                     struct.pack("<I",lookup)+b"\xa3"+
                     struct.pack("<I",0x403000+index*4)+b"\xc3")
            raw = (0x800 if outside_text else 0x220)+index*32
            data[raw:raw+len(thunk)] = thunk
    return data


def scan(path):
    result = subprocess.run([
        os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
        "--disable", "radare2,upx", "--format", "json", str(path),
    ], check=True, text=True, capture_output=True, cwd=ROOT)
    traits = [t for f in json.loads(result.stdout)["files"]
              for t in f.get("traits", [])]
    assert not [t["id"] for t in traits if t["crit"] >= 4], path.name
    return {t["id"] for t in traits} & TARGETS


cases = [
    ("admin-utility-resolvers",image(),TARGETS),
    ("names-without-code",image(code=False),set()),
    ("no-admin-group",image(admin=False),{USER,GROUP}),
    ("different-api-name",image(user=False),{GROUP}),
    ("wrong-api-pointer",image(wrong_target=True),{GROUP}),
    ("wrong-import-call",image(wrong_call=True),set()),
    ("thunks-in-data",image(outside_text=True),set()),
    ("resolves-and-imports",image(also_imported=True),TARGETS),
]

with tempfile.TemporaryDirectory(prefix="account-resolution-controls-") as temp:
    for name, data, expected in cases:
        path = Path(temp)/(name+".exe")
        path.write_bytes(data)
        actual = scan(path)
        assert actual == expected, (name,expected,actual)
        print(name+": PASS",flush=True)
