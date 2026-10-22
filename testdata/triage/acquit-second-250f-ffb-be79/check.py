"""Static rule controls for the supplied ELF mutations; never execute a file.

Usage: check.py OUTER_ELF GENERIC_ELF SCRATCH [--cleave PATH]
The original-branch control is explicitly a one-byte reconstruction, not an
independently recovered original. The review also tests hash-verified originals.
"""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
LOOP = "micro-behaviors/communications/flood::x86-64-udp-flood-send-loop"
REMOTE = "objectives/impact/dos/attack/botnet::x86-64-framed-udp-flood"
TASK = "objectives/command-and-control/botnet/iot::x86-64-framed-attack-task-code"
MIRAI = "well-known/malware/botnet/mirai/stripped::stripped-mirai-iot-botnet"
NOLIBC = "objectives/anti-static/obfuscation/payload/import::nolibc-network-payload"
SHAPE = "micro-behaviors/os/syscall/raw::few-function-static-syscall-binary"
CREDENTIALS = "objectives/lateral-movement/brute-force/iot-creds::xor-encoded-iot-credential-table"

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument("outer",type=Path)
ap.add_argument("generic",type=Path)
ap.add_argument("scratch",type=Path)
ap.add_argument("--cleave",default="cleave")
args=ap.parse_args()
original=args.outer.read_bytes()
assert original[0x3374:0x3378]==bytes.fromhex("74 cb eb e1")
cases=[]
def add(name,data,yes=(),no=()):
    cases.append((name,bytes(data),set(yes),set(no)))
add("length-guard-repeat.elf",original,[LOOP,REMOTE,TASK,MIRAI])
changed=bytearray(original);changed[0x3375]=0xca
add("target-guard-repeat.elf",changed,[LOOP,REMOTE,TASK,MIRAI])
changed=bytearray(original);changed[0x3375]=0xcd
add("guard-spin.elf",changed,[TASK,MIRAI],[LOOP,REMOTE])
changed=bytearray(original);changed[0x3375]=0xcc
add("guard-port-io.elf",changed,[TASK,MIRAI],[LOOP,REMOTE])
changed=bytearray(original)
struct.pack_into("<i",changed,0x336d,0xb487-0x3371)
add("send-to-ret.elf",changed,[TASK,MIRAI],[LOOP,REMOTE])
changed=bytearray(original)
struct.pack_into("<i",changed,0x5b86,0xb487-0x5b8a)
add("body-recv-to-ret.elf",changed,[LOOP,MIRAI],[TASK,REMOTE])
changed=bytearray(original);changed[0x3334]^=1
add("length-slot-mismatch.elf",changed,[TASK,MIRAI],[LOOP,REMOTE])
changed=bytearray(original);struct.pack_into("<H",changed,18,183)
add("wrong-architecture.elf",changed,no=[LOOP,REMOTE,TASK])
changed=bytearray(original)
index=changed.rfind(b"\0.text\0");assert index>=0
changed[index+1:index+6]=b".blob"
add("outside-text.elf",changed,no=[LOOP,REMOTE,TASK])
add("erased-application.elf",args.generic.read_bytes(),[SHAPE,CREDENTIALS],[MIRAI,NOLIBC,LOOP,REMOTE,TASK])

with tempfile.TemporaryDirectory(prefix="elf-controls-",dir=args.scratch) as tmp:
    paths=[]
    for name,data,_,_ in cases:
        p=Path(tmp,name);p.write_bytes(data);paths.append(str(p))
    result=subprocess.run([args.cleave,"--traits-dir",str(ROOT),"--format","json",*paths],
                          text=True,capture_output=True,check=True)
    remaining=result.stdout.strip();decoder=json.JSONDecoder();files={}
    while remaining:
        report,end=decoder.raw_decode(remaining)
        files.update({Path(f["path"]).name:f for f in report["files"]})
        remaining=remaining[end:].lstrip()
    results=[]
    for name,_,yes,no in cases:
        ids={t["id"] for t in files[name].get("traits",[])}
        assert yes<=ids,(name,"missing",sorted(yes-ids))
        assert not no&ids,(name,"unexpected",sorted(no&ids))
        results.append({"case":name,"required":sorted(yes),"absent":sorted(no)})
    print(json.dumps(results,indent=2))
