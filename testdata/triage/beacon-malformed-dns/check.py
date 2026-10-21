#!/usr/bin/env python3
"""Focused synthetic controls; never execute the fixture machine code."""
import argparse
import concurrent.futures
import json
import pathlib
import struct
import subprocess

C2 = "objectives/command-and-control/dns/tunneling::numbered-hex-frame-tasking"
FAMILY = "well-known/malware/rat/cobalt-strike/reflective-loader::mzre-reflective-beacon-carrier"
BOOT = bytes.fromhex("4d5a5245e8000000005b89df5589e581c3247f0000ffd368f0b5a256680400000057ffd0")
CONTROL = bytes.fromhex("334424288944240c747f8bc883e1f081f9f0000000757250e806e5fffff644241001597417")
ONE = b"%s1%08x%08x.%x%x.%s"
FOUR = b"%s4%08x%08x%08x%08x%08x.%08x%08x%08x%08x%08x%08x%08x."


def fixture(omit=(), damaged=False, varied=False):
    d = bytearray(65536)
    d[:len(BOOT)] = BOOT
    if "bootstrap" in omit:
        d[:4] = b"MZ\x90\x00"
    struct.pack_into("<I", d, 60, 128)
    d[128:132] = b"SA\0\0" if damaged else b"PE\0\0"
    struct.pack_into("<HHIIIHH", d, 132, 0x14c, 2, 0, 0, 0, 224, 0x2102)
    o = 152
    struct.pack_into("<H", d, o, 0x10b)
    for off, value in ((16, 4096), (20, 4096), (24, 8192), (28, 0x10000000),
                       (32, 4096), (36, 512), (56, 12288), (60, 512), (92, 16)):
        struct.pack_into("<I", d, o + off, value)
    struct.pack_into("<H", d, o + 68, 2)
    for index, (name, va, raw, flags) in enumerate(((b".text", 4096, 512, 0x60000020),
                                                  (b".rdata", 8192, 1024, 0x40000040))):
        struct.pack_into("<8sIIIIIIHHI", d, 376 + index * 40,
                         name, 512, va, 512, raw, 0, 0, 0, 0, flags)
    code = bytearray(CONTROL)
    if varied:
        code[3] = 0x38
        code[7] = 0x18
        code[9] = 0x41
        code[25:29] = bytes.fromhex("01020304")
        d[17:21] = bytes.fromhex("78560000")
    if "control" not in omit:
        d[512:512 + len(code)] = code
    cursor = 1024
    for tag, value in (("one", ONE), ("four", FOUR), ("dns", b"DNSAPI.dll"),
                       ("reflective", b"_ReflectiveLoader@4"),
                       ("generic", b"HTTP/1.1 CreateNamedPipeA")):
        if tag not in omit:
            d[cursor:cursor + len(value)] = value
            cursor += len(value) + 1
    return bytes(d)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    root = pathlib.Path(__file__).resolve().parents[3]
    args.output.mkdir(parents=True, exist_ok=True)
    cases = [("complete", (), False, False, True, True),
             ("altered-pe-signature", (), True, False, True, True),
             ("varied-addresses", (), False, True, True, True),
             ("ordinary-reflective", ("one", "four", "control"), False, False, False, False),
             ("frames-only", ("control", "bootstrap", "reflective"), False, False, False, False)]
    for omit in ("one", "four", "control", "dns", "reflective", "bootstrap"):
        cases.append(("without-" + omit, (omit,), False, False,
                      omit in ("reflective", "bootstrap"), False))

    def check(case):
        name, omit, damaged, varied, c2, family = case
        path = args.output / (name + ".dll")
        path.write_bytes(fixture(omit, damaged, varied))
        result = subprocess.run([args.cleave, "--traits-dir", str(root), "--format", "json", str(path)],
                                capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        traits = {t["id"] for t in report["files"][0]["traits"]}
        assert (C2 in traits) == c2, (name, "C2", traits)
        assert (FAMILY in traits) == family, (name, "family", traits)
        return name

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for name in pool.map(check, cases):
            print("PASS", name)


if __name__ == "__main__":
    main()
