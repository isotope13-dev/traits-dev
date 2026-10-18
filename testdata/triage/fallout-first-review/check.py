"""Static controls; never execute specimens. Requires pefile and autoit-ripper.

Run with --samples-root and --work-dir pointing outside this repository.
Private specimens and derived PE controls are retained only in --work-dir.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import struct
import subprocess

import pefile
from autoit_ripper import extract
from autoit_ripper.autoit_unpack import EA05_MAGIC, read_string
from autoit_ripper.decompress import decompress
from autoit_ripper.opcodes import OPCODES, TokenStream
from autoit_ripper.utils import ByteStream, EA06Decryptor, crc_data

ROOT = Path(__file__).resolve().parents[3]
FAMILY = "well-known/malware/worm/yuner::"
PROP = FAMILY + "yuner-compiled-propagation-signature"
SAB = FAMILY + "yuner-compiled-sabotage-signature"
RELAY = "objectives/command-and-control/reverse-shell/stream-bridge::dotnet-tcp-cmd-stream-bridge"
RETIRED = {
    "objectives/persistence/login/startup/registry::managed-run-key-mutation-members",
    "objectives/lateral-movement/usb-worm/autorun::autoit-hybris-yuner-compiled-worm",
    "objectives/lateral-movement/usb-worm/autorun::hybris-yuner-usb-propagating-worm",
}
TOKENS = ["TcpClient", "NetworkStream", "set_RedirectStandardInput",
          "set_RedirectStandardOutput", "cmd.exe", "ProcessStartInfo",
          "set_FileName", "Start"]
OUT_LOOP = bytes.fromhex(
    "02 7B 01 00 00 04 06 6F 01 00 00 0A 00 02 7B 02 00 00 04 "
    "6F 02 00 00 0A 6F 03 00 00 0A 25 0A 14 FE 01 16 FE 01 0B 07 2D D7 2A")
IN_LOOP = bytes.fromhex(
    "02 7B 01 00 00 04 6F 01 00 00 0A 06 6F 02 00 00 0A 00 02 "
    "7B 02 00 00 04 6F 03 00 00 0A 25 0A 14 FE 01 16 FE 01 0B 07 2D D2 2A")


def benign_udf_overlay(original):
    """Retain just the shared UDF definitions in a valid EA06 container."""
    base = original.index(EA05_MAGIC) + 40
    stream = ByteStream(original[base:])
    decoder = EA06Decryptor()
    stream.skip_bytes(4)
    read_string(stream, decoder, decoder.au3_ResSubType)
    read_string(stream, decoder, decoder.au3_ResName)
    fields = base + stream._offset
    assert stream.u8() == 1
    size = stream.u32() ^ decoder.au3_ResSize
    stream.skip_bytes(24)
    start = base + stream._offset
    packed = decoder.decrypt(stream.get_bytes(size), decoder.au3_ResContent)
    tokens = decompress(ByteStream(packed))
    ts = TokenStream(tokens)
    ts.u32()
    # Stop before executable top-level Opt statements. Everything retained
    # is a function definition; none of those definitions is invoked.
    lines = 0
    while lines < 136:
        opcode = ts.u8()
        if opcode == 127:
            lines += 1
        else:
            OPCODES[opcode](ts)
    tokens = struct.pack("<I", lines) + tokens[4:ts._offset]
    header = bytearray(original[:start])
    struct.pack_into("<BIII", header, fields, 0,
                     len(tokens) ^ decoder.au3_ResSize,
                     len(tokens) ^ decoder.au3_ResSize,
                     crc_data(tokens) ^ decoder.au3_ResCrcCompressed)
    result = (bytes(header) + decoder.decrypt(tokens, decoder.au3_ResContent)
              + original[start + size:])
    recovered = extract(result)
    assert recovered and len(recovered) == 1
    source = recovered[0][1].decode()
    assert "_STRINGENCRYPT" in source and source.rstrip().endswith("EndFunc")
    assert all(x not in source for x in ("RegWrite", "ProcessClose", "FileCopy", "Opt ("))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples-root", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--case", action="append", help="Run only the named case")
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    worm = (args.samples_root / "f446e51fcc60/2026-10-18_7430700f2efe4490908caeb0bc7f2769_coinminer_elex_stop_yuner").read_bytes()
    managed = (args.samples_root / "415b6cd022b6/pyunkangyul.us_new.exe").read_bytes()
    native = (args.samples_root / "1fa1c1986cde/2026-10-18_6c2bdd56149e688dd5186a5e94727a90_elex_glassworm_wannacry").read_bytes()
    cases = []

    def case(name, data, present=(), absent=(), no_hostile=False):
        cases.append((name, data, set(present), set(absent), no_hostile))

    mailbox = "objectives/execution/payload/file-exec::pop3-tagged-exe-association-loader"
    association = "objectives/evasion/hijack-execution-flow/file-association::extensionless-executable-association-wrapper"
    case("native-original.exe", native, [mailbox, association])
    # Preserve the updater's separate X gate. Its presence must not substitute
    # for a missing mailbox attachment gate.
    old_gate = bytes.fromhex("80 7C 24 3E 58 0F 85")
    assert native.count(old_gate) == 1
    case("native-mailbox-tag-removed.exe", native.replace(old_gate, old_gate[:4] + b"Y" + old_gate[5:]),
         [association, "metadata/binary/instruction::x86-nine-byte-argument-x-tag-call-gate"], [mailbox])
    case("renamed-worm.exe", worm, [PROP, SAB])
    case("appended-padding.exe", worm + bytes(4096), [PROP, SAB])
    image = pefile.PE(data=worm)
    overlay = image.get_overlay_data_start_offset()
    case("runtime-without-script.exe", worm[:overlay], absent=[PROP, SAB], no_hostile=True)
    case("shared-udf-only.exe", benign_udf_overlay(worm), absent=[PROP, SAB], no_hostile=True)
    old_prefix = bytes.fromhex("F2 F5 7B 45 12 EF E4 FF E8 93 BB C9 04 50 69 37 6B 43 CA 52 AF AD")
    case("old-prefix-only.exe", worm[:overlay] + b"AU3!EA06" + old_prefix,
         absent=[PROP, SAB], no_hostile=True)
    relocated = bytearray(worm[:overlay] + bytes(512) + worm[overlay:])
    last = image.sections[-1]
    struct.pack_into("<I", relocated, last.get_field_absolute_offset("SizeOfRawData"),
                     last.SizeOfRawData + 512)
    case("relocated-overlay.exe", bytes(relocated), [PROP, SAB])
    # Remove each role separately: another family's fingerprint may still
    # identify the mutant, but the signature missing its role must disappear.
    roles = {
        "document": ("D3 F5 CC 88 A4 35 FA F9 94 10 36 A7 8B D3 1C 35 0E 51 4C A2 26 D5 4A FD", PROP, SAB),
        "usb": ("DD CB 78 8F A0 E0 EE CE 04 68 F2 17 63", PROP, SAB),
        "autorun": ("B9 D8 38 18 04 1F 1C C4 E3 55 C0 07 D1 C4 F7 1A 88 3A C4 78 C8 2E 0D 95", PROP, SAB),
        "avkill": ("63 60 8A D9 20 A9 5B F5 0F 0E 97 2A B9 47 C4 42 B0 73 03 D1 7B 54 5E BB", SAB, PROP),
        "regtools": ("32 A3 4E 1C 3D C8 78 A7 20 92 23 73 4B CA B7 BB F1 BD A9 4C 34 BB B9 4D", SAB, PROP),
        "restore": ("99 6C E3 25 E3 3C 07 1A BA 81 30 57 69 DB 00 82 05 6D C6 30 FF 45 61 12", SAB, PROP),
    }
    for name, (hexbytes, missing, retained) in roles.items():
        token = bytes.fromhex(hexbytes)
        assert worm.count(token) == 1
        case("no-" + name + ".exe", worm.replace(token, bytes(len(token))), [retained], [missing])
    case("managed-original.exe", managed, [RELAY])
    # Import the established inert managed-PE fixture generator.
    spec = importlib.util.spec_from_file_location("managed_controls", ROOT / "testdata/managed-records-review/verify.py")
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    case("api-cooccurrence.exe", fixture.build_pe(TOKENS), absent=[RELAY], no_hostile=True)
    case("outbound-loop-only.exe", fixture.build_pe(TOKENS, OUT_LOOP), absent=[RELAY], no_hostile=True)
    case("inbound-loop-only.exe", fixture.build_pe(TOKENS, IN_LOOP), absent=[RELAY], no_hostile=True)
    case("paired-relay-loops.exe", fixture.build_pe(TOKENS, OUT_LOOP + IN_LOOP), [RELAY])
    changed_rids = (OUT_LOOP + IN_LOOP).replace(b"\x01\x00\x00\x04", b"\x75\x00\x00\x04")
    changed_rids = changed_rids.replace(b"\x03\x00\x00\x0a", b"\x62\x00\x00\x0a")
    case("changed-metadata-rids.exe", fixture.build_pe(TOKENS, changed_rids), [RELAY])

    if args.case:
        cases = [item for item in cases if item[0] in args.case]
        assert len(cases) == len(set(args.case)), "Unknown case name"

    def scan(item):
        name, data, present, absent, no_hostile = item
        path = args.work_dir / name
        path.write_bytes(data)
        proc = subprocess.run([args.cleave, "--traits-dir", str(ROOT), "--json", str(path)],
                              check=True, capture_output=True, text=True)
        report = json.loads(proc.stdout)
        traits = {t["id"]: t for f in report["files"] for t in f.get("traits", [])}
        ids = set(traits)
        assert present <= ids, (name, "missing", sorted(present - ids))
        assert not absent & ids, (name, "unexpected", sorted(absent & ids))
        assert not RETIRED & ids, (name, "retired", sorted(RETIRED & ids))
        if no_hostile:
            assert not any(t["crit"] == 5 for t in traits.values()), (name, "unexpected hostile")
        return {"case": name, "passed": True,
                "required": sorted(present), "forbidden": sorted(absent)}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(scan, cases))
    output = {"passed": len(results), "total": len(cases), "cases": results}
    (args.work_dir / "results.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
