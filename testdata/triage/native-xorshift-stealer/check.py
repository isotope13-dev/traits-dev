#!/usr/bin/env python3
"""Inert PE controls: rekeying, operand binding, roles and evidence beyond eight hits."""
import argparse
import importlib.util
import json
from pathlib import Path
import random
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("generator", Path(__file__).with_name("generate.py"))
GEN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GEN)
ENCODED = {identifier: directory + "::" + identifier for directory, identifier, _, _ in GEN.TARGETS}
BROWSER = "objectives/credential-access/browser/chromium::keystream-browser-password-harvest"
DISCORD = "objectives/credential-access/discord/token::keystream-discord-token-harvest"
SEND = "objectives/exfiltration/messaging/telegram::keystream-credential-document-sender"
RUN = "objectives/persistence/login/startup/registry::keystream-run-key-self-copy"
HOSTILE = {BROWSER, DISCORD, SEND}
TOKEN_FORMATS = b"dQw4w9WgXcQ:[^\\s\\\"]+\0[\\w-]{24,26}\\.[\\w-]{6}\\.[\\w-]{25,110}\0"


def keystream(plaintext, seed):
    result = bytearray()
    for i, byte in enumerate(plaintext):
        state = seed + i * 0x7c15
        result.append(byte ^ ((state ^ (state >> 7) ^ (state << 6)) & 255))
    return result


def snippet(plaintext, seed, shape="ebp8", wrong_source=False, wrong_call=False):
    encrypted = keystream(plaintext, seed)
    assert len(encrypted) % 4 == 0
    first = {"ebp8": -112, "ebp32": -512, "esp8": 16, "mixed": 120}[shape]
    blob = bytearray()
    for i in range(0, len(encrypted), 4):
        slot = first + i
        if shape == "esp8":
            blob += b"\xc7\x44\x24" + bytes([slot])
        elif -128 <= slot <= 127:
            blob += b"\xc7\x45" + bytes([slot & 255])
        else:
            blob += b"\xc7\x85" + struct.pack("<i", slot)
        blob += encrypted[i:i + 4]
    blob += b"\x68" + struct.pack("<I", 0x408000)
    slot = first + (4 if shape == "esp8" else 0) + (4 if wrong_source else 0)
    if shape == "esp8":
        blob += b"\x8d\x4c\x24" + bytes([slot])
    elif -128 <= slot <= 127:
        blob += b"\x8d\x4d" + bytes([slot & 255])
    else:
        blob += b"\x8d\x8d" + struct.pack("<i", slot)
    call = len(blob)
    blob += b"\xe8\0\0\0\0" + b"\xcc" * 19
    target = len(blob)
    struct.pack_into("<i", blob, call + 1, target - call - 5 + (900 if wrong_call else 0))
    blob += b"\x90" * 16
    blob += bytes.fromhex("b8 b9 79 37 9e f7 e6 8b d8 b8 15 7c 4a 7f f7 e6 03 da 8b f8 81 c7")
    blob += struct.pack("<I", seed & 0xffffffff) + bytes.fromhex("8b cf 81 d3")
    blob += struct.pack("<I", seed >> 32) + bytes.fromhex("8b d3 0f a4 ca 0d c1 e1 0d c3")
    return blob + b"\xcc" * 800


def pe_image(code, data=b"", lookup=True, executable=True):
    """Immediate-return PE; snippets are unreachable and never run."""
    align = lambda n, unit: (n + unit - 1) // unit * unit
    code = b"\xc3" + b"\xcc" * 31 + code
    text_size = align(len(code), 512)
    data_rva = align(0x1000 + text_size, 4096)
    raw_data = 0x400 + text_size
    rdata = bytearray(1024)
    imports = {
        "KERNEL32.dll": ["GetModuleFileNameA", "CopyFileA"] + (["GetProcAddress"] if lookup else []),
        "ADVAPI32.dll": ["RegOpenKeyExA", "RegSetValueExA"],
    }
    position = 80
    for index, (library, names) in enumerate(imports.items()):
        name_rva = data_rva + position
        encoded = library.encode() + b"\0"
        rdata[position:position + len(encoded)] = encoded
        position = align(position + len(encoded), 4)
        thunk = position
        position += 4 * (len(names) + 1)
        for i, name in enumerate(names):
            position = align(position, 2)
            struct.pack_into("<I", rdata, thunk + i * 4, data_rva + position)
            encoded = b"\0\0" + name.encode() + b"\0"
            rdata[position:position + len(encoded)] = encoded
            position += len(encoded)
        struct.pack_into("<IIIII", rdata, index * 20,
                         data_rva + thunk, 0, 0, name_rva, data_rva + thunk)
    rdata = rdata[:align(position, 16)] + data
    data_size = align(len(rdata), 512)
    header = bytearray(0x400)
    header[:2] = b"MZ"
    struct.pack_into("<I", header, 0x3c, 0x80)
    header[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", header, 0x84, 0x14c, 2, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into("<H", header, opt, 0x10b)
    struct.pack_into("<I", header, opt + 16, 0x1000)
    struct.pack_into("<I", header, opt + 28, 0x400000)
    struct.pack_into("<II", header, opt + 32, 4096, 512)
    struct.pack_into("<II", header, opt + 56, align(data_rva + data_size, 4096), 0x400)
    struct.pack_into("<H", header, opt + 68, 2)
    struct.pack_into("<I", header, opt + 92, 16)
    struct.pack_into("<II", header, opt + 96 + 8, data_rva, 60)
    for offset, name, size, va, raw, flags in [
        (0x178, b".text", text_size, 0x1000, 0x400, 0x60000020 if executable else 0x40000040),
        (0x1a0, b".rdata", data_size, data_rva, raw_data, 0x40000040),
    ]:
        struct.pack_into("<8sIIIIIIHHI", header, offset, name, size, va, size, raw, 0, 0, 0, 0, flags)
    return bytes(header) + code.ljust(text_size, b"\xcc") + bytes(rdata).ljust(data_size, b"\0")


def make_case(wanted=None, seed=1, shape="ebp8", tokens=True, lookup=True,
              executable=True, decoys=0, wrong_source=False, wrong_call=False):
    wanted = set(ENCODED) if wanted is None else set(wanted)
    rng = random.Random(seed)
    code = bytearray()
    for i in range(decoys):
        code += snippet(b"ordinary padding", rng.getrandbits(64), shape)
    for _, identifier, _, plaintext in GEN.TARGETS:
        if identifier in wanted:
            code += snippet(plaintext, rng.getrandbits(64), shape, wrong_source, wrong_call)
    data = b"SQLite format 3\0" + (TOKEN_FORMATS if tokens else b"")
    return pe_image(bytes(code), data, lookup, executable)


def scan(engine, target):
    result = subprocess.run([engine, "--traits-dir", str(ROOT), "--format", "json", str(target)],
                            check=True, capture_output=True, text=True)
    decoder = json.JSONDecoder()
    rest = result.stdout.lstrip()
    files = []
    while rest:
        report, end = decoder.raw_decode(rest)
        files.extend(report["files"])
        rest = rest[end:].lstrip()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--sample", type=Path)
    args = parser.parse_args()
    all_targets = set(ENCODED)
    cases = {}
    for shape in ("ebp8", "ebp32", "esp8", "mixed"):
        cases["rekeyed-" + shape + ".exe"] = (make_case(seed=197 + len(shape), shape=shape), HOSTILE)
    cases["after-many-decoys.exe"] = (make_case(seed=999, decoys=16), HOSTILE)
    for identifier in ("x86-xorshift-api-host", "x86-xorshift-document-method-prefix",
                       "x86-xorshift-dpapi-prefix", "x86-xorshift-send-request-prefix"):
        cases["without-" + identifier + ".exe"] = (make_case(all_targets - {identifier}), set())
    cases["browser-only.exe"] = (make_case(tokens=False), {BROWSER, SEND})
    cases["discord-only.exe"] = (make_case(all_targets - {"x86-xorshift-login-columns-prefix"}), {DISCORD, SEND})
    cases["no-credential-source.exe"] = (make_case(all_targets - {"x86-xorshift-login-columns-prefix"}, tokens=False), set())
    cases["credential-tool-no-sender.exe"] = (make_case({"x86-xorshift-login-columns-prefix", "x86-xorshift-dpapi-prefix"}), set())
    cases["ordinary-bot.exe"] = (make_case({"x86-xorshift-api-host", "x86-xorshift-document-method-prefix", "x86-xorshift-send-request-prefix"}, tokens=False), set())
    cases["wrong-source.exe"] = (make_case(wrong_source=True), set())
    cases["wrong-call.exe"] = (make_case(wrong_call=True), set())
    cases["nonexecuting-data.exe"] = (make_case(executable=False), set())
    cases["no-dynamic-lookup.exe"] = (make_case(lookup=False), set())
    with tempfile.TemporaryDirectory(prefix="native-xorshift-controls-") as directory:
        scratch = Path(directory)
        for name, (contents, _) in cases.items():
            (scratch / name).write_bytes(contents)
        files = {Path(f["path"]).name: f for f in scan(args.cleave, scratch)}
        for name, (_, expected) in cases.items():
            traits = {t["id"] for t in files[name].get("traits", [])}
            assert traits & HOSTILE == expected, (name, expected, traits & HOSTILE)
            if name.startswith("rekeyed-") or name == "after-many-decoys.exe":
                assert set(ENCODED.values()) <= traits, (name, set(ENCODED.values()) - traits)
                assert RUN in traits, name
            if name in {"wrong-source.exe", "wrong-call.exe", "nonexecuting-data.exe"}:
                assert not traits & set(ENCODED.values()), name
    if args.sample:
        files = scan(args.cleave, args.sample)
        traits = {t["id"]: t for f in files for t in f.get("traits", [])}
        assert HOSTILE <= traits.keys(), HOSTILE - traits.keys()
        assert all(traits[t]["crit"] == 5 for t in HOSTILE)
        assert RUN in traits
    print(f"PASS: {len(cases)} controls" + (" and supplied executable" if args.sample else ""))


if __name__ == "__main__":
    main()
