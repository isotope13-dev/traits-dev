"""Focused controls; sample bytes stay outside the rule repository.

Usage: python3 check.py <infector> <manifest> <scratch-directory>
Uses CLEAVE when set, otherwise the installed cleave executable.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys


repo = Path(__file__).resolve().parents[3]
sample, manifest, scratch = map(Path, sys.argv[1:])
scratch.mkdir(parents=True, exist_ok=True)
behavior = "objectives/impact/infect/binary/rewrite::recursive-prepending-footer-infector"
family = "well-known/malware/worm/usashohdi::usashohdi"
elex = "well-known/malware/trojan/elex/worm/elex-lure::elex-shohdi-photo-worm-variant"
dump = "micro-behaviors/os/privilege/manifest::dump-permission"
custom = "metadata/permission/manifest::android-nonplatform-permission-reference"
records = []


def check(label, path, present=(), absent=(), max_crit=None):
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(repo),
         "--format", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(result.stdout)
    primary = report["files"][0]
    traits = {t["id"]: t["crit"] for t in primary.get("traits", [])}
    assert set(present) <= traits.keys(), (label, "missing", set(present) - traits.keys())
    assert not set(absent) & traits.keys(), (label, "unexpected", set(absent) & traits.keys())
    if max_crit is not None:
        assert max(traits.values(), default=0) <= max_crit, (label, traits)
    records.append({"case": label, "passed": True})


def variant(name, data):
    path = scratch / name
    path.write_bytes(data)
    return path


data = sample.read_bytes()
check("original infection", sample, [behavior, family], [elex])
anonymous = data.replace(b"UsaShohdi", b"ZzzZzzzzz").replace(b"ccApp.exe", b"xxApp.exe")
check("family names removed", variant("anonymous.exe", anonymous), [behavior], [family, elex])
writer = bytearray(data)
assert writer[0x1BB2:0x1BB5] == bytes.fromhex("8d45f0")
writer[0x1BB2] = 0x90
check("writer instruction removed", variant("no-writer.exe", writer), absent=[behavior, family, elex])
reader = bytearray(data)
assert reader[0x17FA:0x17FC] == bytes.fromhex("6a02")
reader[0x17FB] = 1
check("EOF seek changed", variant("no-reader.exe", reader), absent=[behavior, family, elex])
check("standalone infector stub", variant("stub.exe", data[:0xF000]), [behavior, family], [elex])
host_offset, host_size = struct.unpack("<II", data[-17:-9])
assert host_offset + host_size == len(data) - 17
check("displaced original host", variant("host.exe", data[host_offset:host_offset + host_size]), absent=[behavior, family, elex])
check("game manifest", manifest, absent=[dump], max_crit=3)
guard = b'<receiver android:name="androidx.work.impl.diagnostics.DiagnosticsReceiver" android:permission="android.permission.DUMP"/>'
prefix = b'<manifest xmlns:android="http://schemas.android.com/apk/res/android">'
check("DUMP receiver guard", variant("guard.xml", prefix + guard + b"</manifest>"), absent=[dump])
request = b'<uses-permission android:name="android.permission.DUMP"/>'
check("DUMP grant beside diagnostic receiver", variant("request.xml", prefix + request + guard + b"</manifest>"), [dump])
internet = b'<uses-permission android:name="android.permission.INTERNET"/>'
check("platform permission is not app custom", variant("internet.xml", prefix + internet + b"</manifest>"), absent=[custom], max_crit=3)
print(json.dumps({"controls": records}, indent=2))
