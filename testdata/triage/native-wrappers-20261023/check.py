"""Focused controls on original specimens and byte variants, kept in scratch.

Usage: check.py <scratch/triage-bad> <sample-root>
CLEAVE may select the engine. No specimen bytes are stored in this repository.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

scratch, samples = map(Path, sys.argv[1:])
repo = Path(__file__).resolve().parents[3]
controls = scratch / "controls"
controls.mkdir(exist_ok=True)
exe = os.environ.get("CLEAVE", "cleave")
env = dict(os.environ, CLEAVE_VALIDATE="0")
records = []
debug = "objectives/anti-analysis/debugger-detect/check::peb-being-debugged-byte-branch"
heap = "objectives/anti-analysis/debugger-detect/check::x86-peb-ntglobalflag-mask-branch"
opaque = "objectives/anti-static/obfuscation/payload/resource::cyclic-xor-opaque-resource-decompressor"
footer = "objectives/impact/infect/binary/rewrite::prepender-host-copy-footer-routines"
old_footer = "objectives/impact/infect/binary/rewrite::recursive-prepending-footer-infector"
patching = "objectives/anti-static/obfuscation/instruction/junk::obfuscated-thunks-memory-patching-api-set"
old_injection = "objectives/anti-static/obfuscation/instruction/junk::obfuscated-thunk-injection-loader"
encryption = "metadata/binary/layout/overlay::inno-65-67-encrypted-file-data"
carrier = "metadata/binary/layout/overlay::unverified-certificate-carrier-multi-pe-overlay"
vendor = "metadata/binary/provenance/version-info::vmware-inc-company-string"

def check(label, path, present=(), absent=(), severity=None):
    p = subprocess.run([exe, "--traits-dir", str(repo), "--format", "json", str(path)],
                       text=True, capture_output=True, env=env)
    assert p.returncode == 0, (label, p.stderr)
    d = json.loads(p.stdout)
    f = d["files"][0]
    traits = {t["id"]: t["crit"] for t in f["traits"]}
    assert set(present) <= traits.keys(), (label, "missing", set(present) - traits.keys())
    assert not set(absent) & traits.keys(), (label, "unexpected", set(absent) & traits.keys())
    for k, v in (severity or {}).items():
        assert traits[k] == v, (label, k, traits[k])
    records.append({"case": label, "passed": True})
    print("PASS: " + label, file=sys.stderr, flush=True)

def variant(name, data):
    p = controls / name
    p.write_bytes(data)
    return p

def mutate(data, pattern, byte_index, value):
    pattern = bytes.fromhex(pattern)
    offset = data.index(pattern)
    result = bytearray(data)
    result[offset + byte_index] = value
    return result

oxi = samples / "a4403e20eb24/OXI_Joiner.exe"
packed = samples / "761fb84b4c1c/2026-10-23_6b85d7a6ad7fac9af4ff136e1b847e6f_akira_cloudeye_elex_rhadamanthys"
tool = samples / "207eb6ffea67/1a9086e432f5630af5cf9d38891771c9.exe"
b = oxi.read_bytes()
check("OXI original", oxi, [debug, heap, opaque])
check("OXI renamed", variant("ordinary-name.exe", b), [debug, heap, opaque])
check("PEB byte changed", variant("peb-field.exe", mutate(b, "64 a1 30 00 00 00 80 78 02 00", 8, 3)), [heap, opaque], [debug])
check("PEB mask changed", variant("heap-mask.exe", mutate(b, "64 a1 30 00 00 00 f7 40 68 70 00 00 00", 9, 0)), [debug, opaque], [heap])
check("XOR operation removed", variant("no-xor.exe", mutate(b, "ac 32 82 50 34 40 00 aa", 1, 0x90)), [debug, heap], [opaque])

b = packed.read_bytes()
check("embedded infector original", packed, [footer, carrier])
check("embedded infector renamed", variant("package.exe", b), [footer, carrier])
check("footer write removed", variant("no-footer-write.exe", mutate(b, "8d45f06a04505759e8b80d0000", 0, 0x90)), [carrier], [footer])
check("EOF seek changed", variant("no-eof-reader.exe", mutate(b, "6a02834dfcff6af8", 1, 1)), [carrier], [footer])
check("stream copy removed", variant("no-stream-copy.exe", mutate(b, "ff75f0565950e8", 0, 0x90)), [carrier], [footer])
check("plain NSIS header without infection code", variant("nsis-header.exe", b[:64512]), absent=[footer])
check("Inno encryption and vendor observations", tool, [encryption, vendor])
b = tool.read_bytes()
offset = b.index(b"Inno Setup Setup Data (6.7.0)", 842240) + 68
assert b[offset] == 1
m = bytearray(b)
m[offset] = 0
check("Inno unencrypted declaration", variant("inno-unencrypted.exe", m), [vendor], [encryption])
check("plain version label in runtime", variant("inno-loader-only.exe", b[:842240]), [vendor], [encryption])
m = bytearray(b)
company = b.index("VMware, Inc.".encode("utf-16le"))
m[company] = ord("X")
filename = b.index("oijezduh.exe".encode("utf-16le"))
m[filename:filename + 24] = "VMware, Inc.".encode("utf-16le")
check("vendor name in another resource field", variant("vendor-other-field.exe", m), [encryption], [vendor])

old = scratch / "positive/hopper/2026-10-16_d1751f4cab02eac760fe6006bacb5598_cobalt-strike_elex_hijackloader_nymaim_rhadamanthys_smoke-loader_stealc_tofsee"
check("previous prepender retains attack coverage", old, [old_footer, "well-known/malware/worm/usashohdi::usashohdi"])
for n in ["g1_a.exe", "g2_c.exe"]:
    check("self-patching obfuscated member " + n, scratch / "tool-extracted/tmp" / n,
          [patching], [old_injection], {patching: 4})
old = scratch / "positive/hopper/2026-10-05_015614711dd45e85d526579fb20188d9_akira_elex"
check("original thunk positive retains obfuscation", old, [patching], [old_injection], {patching: 4})
print(json.dumps({"controls": records}, indent=2))
