#!/usr/bin/env python3
"""Reproduce recovered data without executing samples or contacting endpoints.

Dependencies: pefile, pycryptodome.
Run with the audit directory produced during triage:
  python verify.py --audit-root /tmp/hopper-triage-audit

Originals are located through the adjacent initial review, including its
relocated benign paths. Outputs contain decoded data, never executable launches.
The offsets below are evidence anchors for these exact hashes, not detection
rules. They deliberately fail closed if given another specimen.
"""
import argparse
import base64
import gzip
import hashlib
import json
import re
import struct
from pathlib import Path

import pefile
from Crypto.Cipher import ARC4


def sha(data):
    return hashlib.sha256(data).hexdigest()


def checked(path, digest):
    data = path.read_bytes()
    assert sha(data) == digest, (str(path), sha(data))
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--audit-root", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    review = json.loads(
        (Path(__file__).parent.parent / "hopper-review-2026-10-20/review.json")
        .read_text()
    )
    samples = {s["index"]: s for s in review["samples"]}

    def original(index):
        s = samples[index]
        candidates = [Path(s["original_path"])]
        if s.get("local_path"):
            candidates.append(Path(s["local_path"]))
        path = next(p for p in candidates if p.is_file())
        return checked(path, s["sha256"])

    results = {}
    trainer = original(4)
    decoded = []
    for match in re.finditer(rb"(?:[A-Za-z0-9+/=]\x00){1000,}", trainer):
        try:
            decoded.append(gzip.decompress(base64.b64decode(
                match.group().decode("utf-16le"), validate=True)))
        except (ValueError, OSError, EOFError):
            continue
    digest = "f1d4195ec595a8fd866c1832de249baf0b811cf1dd285e4af97230809d847667"
    assert any(sha(b) == digest for b in decoded)
    results["trainer_bundle"] = {"sha256": digest, "bytes": 241045}

    reflective = original(24)
    pe_offset = struct.unpack_from("<I", reflective, 0x3C)[0]
    assert pe_offset == 0x100 and reflective[pe_offset:pe_offset + 4] == b"TL\0\0"
    restored = bytearray(reflective)
    restored[pe_offset:pe_offset + 4] = b"PE\0\0"
    pe = pefile.PE(data=bytes(restored))
    assert b"_ReflectiveLoader@4" in {
        s.name for s in pe.DIRECTORY_ENTRY_EXPORT.symbols}
    config = bytes(b ^ 0x2E for b in reflective[0x33A20:0x34A20])
    assert sha(config) == "1a710a32a63f76b0fe426f90b78d6ff0faf34c24f915c1e34cd06349ec1f1537"
    cursor = 0
    fields = []
    while cursor + 6 <= len(config):
        ident, kind, size = struct.unpack_from(">HHH", config, cursor)
        if ident == 0:
            break
        assert kind in (1, 2, 3) and cursor + 6 + size <= len(config)
        value = config[cursor + 6:cursor + 6 + size]
        fields.append({"id": ident, "kind": kind, "size": size,
                       "hex": value.hex()})
        cursor += 6 + size
    assert len(fields) >= 50
    results["reflective_config"] = {
        "sha256": sha(config), "fields": fields,
        "restored_header_copy_sha256": sha(restored),
    }

    dll = checked(
        args.audit_root / "vhd/enCrAshReP.dll",
        "07998a616b57975e656fef18092559ac04f87b1ebf1493958fa64a3f2c08f66f",
    )
    # Key at VA 0x1019ac68 is passed as the third argument to 0x1000fe08.
    # That wrapper converts UTF-16 key/hex strings, then calls the RC4 routine.
    p = pefile.PE(data=dll)
    key_raw = p.get_data(0x19AC68, 64)
    key = key_raw.decode("utf-16le").rstrip("\0").encode("ascii")
    strings = []
    for match in re.finditer(rb"(?:[0-9A-F]\x00){8,}", dll):
        text = match.group().decode("utf-16le")
        if len(text) % 2:
            continue
        value = ARC4.new(key).decrypt(bytes.fromhex(text))
        if sum(32 <= c < 127 for c in value) / len(value) > 0.95:
            strings.append({"offset": hex(match.start()),
                            "text": value.decode("ascii", errors="replace")})
    plain = {s["text"] for s in strings}
    assert r"\\.\ardrv" in plain
    assert r"SOFTWARE\CLASSES\MS-SETTINGS\SHELL\OPEN\COMMAND" in plain
    assert any("CSFALCONSERVICE" in s and "MSMPENG" in s for s in plain)
    results["vhd_rc4_strings"] = strings

    signs = checked(
        args.audit_root / "re/nsis/Signs",
        "1fa1c481c9bc28824a93dee673a5a5afeb4f0497cc4758120938cf7b5ec546a3",
    )
    # Source and length established from decoder instructions, not guessed
    # from entropy. The callback entry is offset 11024 in Signs.
    source = signs[0x4403:0x4403 + 0x1F01C]
    key = struct.pack("<I", 0x786C749A)
    stage = bytes(c ^ key[i % 4] for i, c in enumerate(source))
    assert sha(stage) == "d87c43e225824a6aae3bb4613a448c66669e6b363d91b4fe144464fb67effc3b"
    results["nsis_stage2"] = {"bytes": len(stage), "sha256": sha(stage)}

    variants = {i: original(i) for i in (62, 63, 68, 70)}
    shortest = variants[70]
    # These variants differ only in a 16-byte mutation slot and truncation.
    for index, data in variants.items():
        assert data[:0x126CC] == shortest[:0x126CC]
        assert data[0x126DC:len(shortest)] == shortest[0x126DC:]
    overlay = variants[62][0x14C8B:]
    assert sha(overlay) == "5350dc736d0b67b0d39ea24d57194d795d9f3614d7f994b252ccfa9587ed8991"
    resource_rows = []
    for index, data in variants.items():
        embedded = data[0x14C8B:]
        p = pefile.PE(data=embedded)
        entries = []
        for group in getattr(getattr(p, "DIRECTORY_ENTRY_RESOURCE", None), "entries", []):
            if group.id != 10:  # RT_RCDATA
                continue
            for name in group.directory.entries:
                for language in name.directory.entries:
                    r = language.data.struct
                    start = p.get_offset_from_rva(r.OffsetToData)
                    entries.append({
                        "name": str(name.name or name.id), "declared": r.Size,
                        "available": max(0, min(r.Size, len(embedded) - start)),
                    })
        resource_rows.append({"index": index, "resources": entries})
    results["rifaien"] = resource_rows
    # Missing resources are a terminal evidence limit, not a decryption failure.
    assert all(not any(e["name"] == "~" and e["available"] == e["declared"]
                       for e in row["resources"]) for row in resource_rows)

    carrier = original(45)
    assert carrier[:0x179FF] == carrier[0x2E8B75:0x2E8B75 + 0x179FF]
    results["dism_repeated_prefix"] = {
        "bytes": 0x179FF, "second_offset": "0x2e8b75",
        "sha256": sha(carrier[:0x179FF]),
        "meaning": "Duplicate data, not proof of execution or malware family.",
    }
    text = json.dumps(results, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({"verified": list(results), "count": len(results)}))


if __name__ == "__main__":
    main()
