#!/usr/bin/env python3
"""Check original samples and byte-mutated controls without executing them.

Usage: check.py <DOS/HTML sample> <web-app HTA sample> <scratch directory>
Only the original bytes and controls generated from them are scanned.
"""
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
virus, launcher, scratch = map(Path, sys.argv[1:])
scratch.mkdir(parents=True, exist_ok=True)
original = virus.read_bytes()
decode = "micro-behaviors/data/decode/xor::dos-call-relative-com-mask-decode"
loop = "objectives/impact/infect/binary/dos/overwrite::dos-bp-sized-search-image-overwrite"
infect = "objectives/impact/infect/binary/dos/overwrite::dos-hidden-mask-search-self-overwriter"
polyglot = "objectives/anti-static/polyglot/format::html-title-jump-dos-overwriter"
conceal = "objectives/anti-static/obfuscation/encoding/xor::html-jump-xor-hidden-com-mask"
script = "micro-behaviors/process/interpreter/eval/source::html-classic-script-src"
all_dos = {decode, loop, infect, polyglot, conceal}
cases = []


def case(name, data, required=(), forbidden=()):
    path = scratch / name
    path.write_bytes(data)
    cases.append((path, set(required), set(forbidden)))


case("original.html", original, all_dos)
# The key and ciphertext both change; no specimen-specific key is required.
variant = bytearray(original)
mask_at = original.index(bytes.fromhex("b5 b1 dc f0 d2 9f"))
key_at = original.index(bytes.fromhex("ac 34 9f aa e2 fa")) + 2
variant[mask_at:mask_at + 6] = bytes(x ^ 0x42 for x in b"*.CoM\0")
variant[key_at] = 0x42
case("rekeyed.html", variant, all_dos)
# Changing the key alone no longer proves that the mask decodes to COM.
variant = bytearray(original)
variant[key_at] = 0x42
case("wrong-key.html", variant, {loop, polyglot}, {decode, infect, conceal})
# An incorrect CALL displacement must not bind a coincidental decoder.
variant = original.replace(bytes.fromhex("e8 0a 00"), bytes.fromhex("e8 0b 00"))
assert variant != original
case("wrong-call.html", variant, {loop, polyglot}, {decode, infect, conceal})
# Read instead of write, or a different buffer, is not self-overwrite.
for name, before, after in [
    ("read-only.html", "b4 40 cd 21", "b4 3f cd 21"),
    ("other-buffer.html", "33 d2 fe c6 b4 40", "33 d2 fe c2 b4 40"),
]:
    variant = original.replace(bytes.fromhex(before), bytes.fromhex(after))
    assert variant != original
    case(name, variant, {decode, conceal}, {loop, infect, polyglot})
# HTML without the appended native body must not satisfy an attack rule.
case("title-only.html", original[:original.index(bytes.fromhex("90 fc 90"))],
     (), all_dos)
case("launcher.hta", launcher.read_bytes(), {script}, all_dos)
case("quoted-script.html", b'<html><script src="./app.js"></script></html>',
     {script}, all_dos)
case("comment.html", b'<html><!-- <script src="./app.js"></script> --></html>',
     (), all_dos | {script})
case("inert-script.html",
     b'<html><script src="./app.js" type="application/json"></script></html>',
     (), all_dos | {script})
case("link.html", b'<html><a href="./app.js">Source</a></html>',
     (), all_dos | {script})

output = subprocess.check_output(
    ["cleave", "--traits-dir", str(root), "--format", "json", *map(str, (c[0] for c in cases))],
    text=True,
)
reports = []
decoder = json.JSONDecoder()
while output.strip():
    report, end = decoder.raw_decode(output.lstrip())
    reports.extend(report["files"])
    output = output.lstrip()[end:]
for path, required, forbidden in cases:
    report = next(r for r in reports if Path(r["path"]).name == path.name)
    traits = {t["id"]: t for t in report["traits"]}
    assert not required - traits.keys(), (path.name, "missing", required - traits.keys())
    assert not forbidden & traits.keys(), (path.name, "unexpected", forbidden & traits.keys())
    for ident in {infect, polyglot} & required:
        assert traits[ident]["crit"] == 5, (path.name, ident)
print(f"PASS: {len(cases)} original, re-keyed, and near-miss controls")
