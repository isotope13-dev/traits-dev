"""Focused static carrier checks. Never execute a sample or generated variant.

Usage: python3 check.py --cleave PATH --audit-root /tmp/triage/sightings-iso
The audit root supplies privately retained specimens; no malware is embedded
in this helper or checked into the repository. Output defaults to /tmp.
"""
import argparse
import hashlib
import json
import pathlib
import subprocess


IDS = {
    "swift": "well-known/malware/dropper/resource-carrier::tail-xor-constructor-carrier",
    "po": "well-known/malware/dropper/resource-carrier::repaired-base64-reflection-carrier",
}
BEHAVIOR_IDS = {
    "swift": "objectives/anti-static/obfuscation/reflection/invoke::padded-resource-stage-activation",
    "po": "objectives/anti-static/obfuscation/reflection/invoke::repaired-resource-split-name-dispatch",
}
DIRS = {
    "swift": "efafbcd8c1833e58202139b5877cffdafff021bcb0b8da527e984db8d5f87e38",
    "po": "f10b51e14e75e99314449a1d974c556a262ac7b695568e2b2f496d2e38731b16",
}
MEMBERS = {"swift": "SWIFT_ADVICE.exe", "po": "PO_26-1922-20061.exe"}


def replace(data, old, new):
    assert len(old) == len(new) and old in data, (old, len(old), len(new))
    return data.replace(old, new)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        result, end = decoder.raw_decode(text)
        yield result
        text = text[end:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cleave", required=True)
    ap.add_argument("--audit-root", type=pathlib.Path, required=True)
    ap.add_argument("--output", type=pathlib.Path,
                    default=pathlib.Path("/tmp/triage/sightings-iso/outer-controls"))
    ap.add_argument("--iso-root", type=pathlib.Path, default=pathlib.Path("/tmp/sightings/iso"))
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    cases = []
    data = {k: (args.audit_root / DIRS[k] / "unpacked" / MEMBERS[k]).read_bytes()
            for k in DIRS}

    def add(name, kind, blob, expect=True, iso=False, proof=None, behavior_expect=None):
        if iso:
            carrier = (args.iso_root / (DIRS[kind] + ".iso")).read_bytes()
            original = data[kind]
            assert carrier.count(original) == 1 and len(blob) == len(original)
            blob = carrier.replace(original, blob)
        path = args.output / (name + (".iso" if iso else ".exe"))
        path.write_bytes(blob)
        cases.append({"name": name, "path": str(path), "sha256": sha(blob),
                      "id": IDS[kind], "expect": expect, "proof": proof,
                      "iso": iso, "behavior_id": BEHAVIOR_IDS[kind],
                      "behavior_expect": expect if behavior_expect is None else behavior_expect})

    for kind in DIRS:
        add(kind + "-original", kind, data[kind])
        add(kind + "-original-container", kind, data[kind], iso=True)

    swift = data["swift"]
    old_cipher = (args.audit_root / DIRS["swift"] / "resources" / "Blue").read_bytes()
    stage = (args.audit_root / DIRS["swift"] / "stage1.dll").read_bytes()
    assert swift.count(old_cipher) == 1
    key = "Green".encode("utf-16be")[:5]
    old_state = old_cipher[-1] ^ 0x70
    assert bytes(b ^ old_state ^ key[i % 5] for i, b in enumerate(old_cipher[:-1])) == stage
    for new_key, new_mask in [("Amber", 0x70), ("Ivory", 0x22), ("Other", 0x53)]:
        new_bytes = new_key.encode("utf-16be")[:5]
        state = old_cipher[-1] ^ new_mask
        cipher = bytes(b ^ state ^ new_bytes[i % 5] for i, b in enumerate(stage)) + old_cipher[-1:]
        variant = replace(swift, old_cipher, cipher)
        variant = replace(variant, "Green".encode("utf-16le"), new_key.encode("utf-16le"))
        needle = bytes.fromhex("03 03 8e 69 17 da 91 1f 70 61")
        assert variant.count(needle) == 1
        variant = replace(variant, needle, needle[:-2] + bytes([new_mask]) + needle[-1:])
        assert bytes(b ^ state ^ new_bytes[i % 5] for i, b in enumerate(cipher[:-1])) == stage
        proof = {"decoded_stage_sha256_unchanged": sha(stage), "key": new_key, "mask": new_mask}
        name = "swift-key-mask-" + new_key.lower()
        add(name, "swift", variant, proof=proof)
        if new_mask == 0x22:
            add(name + "-container", "swift", variant, iso=True, proof=proof)
    renamed = replace(swift, b"FastResourceComparer", b"CacheResourceCompare")
    renamed = replace(renamed, b"Xosh_Maza", b"HiddenRun")
    add("swift-renamed-helpers", "swift", renamed)

    po = data["po"]
    marker_variant = replace(po, "(@@)".encode("utf-16le"), "[##]".encode("utf-16le"))
    marker_variant = replace(marker_variant, b"(@@)", b"[##]")
    marker_variant = replace(marker_variant, "@@@@@^".encode("utf-16le"), "%%%%%%".encode("utf-16le"))
    encoded = (args.audit_root / DIRS["po"] / "resources" / "LoadViot").read_text()
    import base64
    recovered = base64.b64decode(encoded.replace("(@@)", "A")[::-1])
    revised = encoded.replace("(@@)", "[##]")
    assert base64.b64decode(revised.replace("[##]", "A")[::-1]) == recovered
    proof = {"decoded_stage_sha256_unchanged": sha(recovered), "repair_marker": "[##]",
             "type_separator": "%%%%%%"}
    add("po-changed-markers", "po", marker_variant, proof=proof)
    add("po-changed-markers-container", "po", marker_variant, iso=True, proof=proof)
    renamed = replace(po, b"Lighter", b"Carrier")
    renamed = replace(renamed, b"CorrectMarks", b"DecodeGlyphs")
    add("po-renamed-helpers", "po", renamed)
    flags_at = next(m for m in json.loads((args.audit_root / DIRS["po"] / "outer-cil.json").read_text())
                    if m["method"] == "Rate")["rva"] - 0x2000 + 0x200 + 74
    assert po[flags_at:flags_at+5] == bytes.fromhex("20 00 01 00 00")
    variant = po[:flags_at+1] + b"\x18" + po[flags_at+2:]
    add("po-public-static-lookup-flags", "po", variant,
        proof={"invoke_method_bit_retained": True, "added_flags": "Public | Static"})

    # Equal-length instruction variants retain the decoded stages and loading
    # semantics but break the contiguous implementation fingerprint. The
    # concealment finding must stand on its own constituent evidence.
    methods = {kind: json.loads((args.audit_root / DIRS[kind] / "outer-cil.json").read_text())
               for kind in DIRS}

    def instruction_at(kind, method, offset):
        selected = next(m for m in methods[kind] if m["method"] == method)
        return selected["rva"] - 0x2000 + 0x200 + offset

    at = instruction_at("swift", "Xr", 40)
    assert swift[at] == 0xd6
    add("swift-unchecked-allocation-add", "swift", swift[:at] + b"\x58" + swift[at+1:],
        expect=False, behavior_expect=True,
        proof={"change": "add.ovf -> add; length is 41473, so overflow is impossible"})
    at = instruction_at("po", "Rate", 59)
    assert po[at] == 0x28
    add("po-virtual-string-repair", "po", po[:at] + b"\x6f" + po[at+1:],
        expect=False, behavior_expect=True,
        proof={"change": "call -> callvirt for the same non-null String.Replace receiver"})

    # Removing argument noise retains the known decoder/carrier fingerprint
    # but removes the padded-array concealment observation.
    # Change the final dummy Boolean to an unboxed null, leaving five nops
    # for equal length. The slot is unused by the argument shuffle.
    start = instruction_at("swift", "Object", 134)
    end = instruction_at("swift", "Object", 140)
    add("swift-null-padding-slot", "swift", swift[:start] + b"\x14" + bytes(end-start-1) + swift[end:],
        expect=True, behavior_expect=False,
        proof={"change": "unused final boxed Boolean -> null; same array length"})

    # Replace only the handoff method's IL body with a valid null return.
    # Its crypto helpers, API-name metadata and hidden resources remain.
    # These are inert reduction controls, not asserted benign specimens.
    for kind, method in [("swift", "Object"), ("po", "Rate")]:
        methods = json.loads((args.audit_root / DIRS[kind] / "outer-cil.json").read_text())
        selected = next(m for m in methods if m["method"] == method)
        body_offset = selected["rva"] - 0x2000 + 0x200
        original = data[kind]
        # Both samples have their .text raw offset 0x200 and virtual 0x2000.
        assert original[body_offset] & 3 == 3
        header_size = (int.from_bytes(original[body_offset:body_offset+2], "little") >> 12) * 4
        length = int.from_bytes(original[body_offset+4:body_offset+8], "little")
        start = body_offset + header_size
        assert 2 <= length <= 4096
        variant = original[:start] + bytes(length-2) + b"\x14\x2a" + original[start+length:]
        add(kind + "-removed-handoff", kind, variant, expect=False)

    trusted = [
        args.audit_root / "tools/.store/ilspycmd/11.1.0.9782/ilspycmd/11.1.0.9782/tools/net10.0/any/ICSharpCode.Decompiler.dll",
        pathlib.Path("/usr/local/share/dotnet/shared/Microsoft.NETCore.App/10.0.12/System.Net.Mail.dll"),
        pathlib.Path("/usr/local/share/dotnet/shared/Microsoft.NETCore.App/10.0.12/System.Reflection.Emit.dll"),
        pathlib.Path("/usr/local/share/dotnet/shared/Microsoft.NETCore.App/10.0.12/System.Private.CoreLib.dll"),
    ]
    for path in trusted:
        if path.is_file():
            for kind in DIRS:
                cases.append({"name": "trusted-" + path.name + "-" + kind,
                              "path": str(path), "id": IDS[kind], "expect": False,
                              "behavior_id": BEHAVIOR_IDS[kind], "behavior_expect": False})
    reports = {}
    for case in cases:
        if case["path"] not in reports:
            run = subprocess.run([args.cleave, "--traits-dir", ".", "--format=json", case["path"]],
                                 text=True, capture_output=True, check=True)
            reports[case["path"]] = list(documents(run.stdout))
        files = [f for report in reports[case["path"]] for f in report["files"]]
        root = files[0]
        found = next((t for t in root["traits"] if t["id"] == case["id"]), None)
        case["actual"] = found is not None
        behavior = next((t for t in root["traits"] if t["id"] == case["behavior_id"]), None)
        case["behavior_actual"] = behavior is not None
        case["pass"] = (case["actual"] == case["expect"] and
                        case["behavior_actual"] == case["behavior_expect"])
        if case.get("iso"):
            case["inherited_findings"] = []
            for trait in [found, behavior]:
                if not trait:
                    continue
                children = [f["id"] for f in files[1:]
                            if any(t["id"] == trait["id"] for t in f["traits"])]
                case["inherited_findings"].append({"id": trait["id"],
                    "source": trait.get("from", trait.get("src", trait.get("srcs"))),
                    "child_matching_ids": children})
                case["pass"] &= bool(children)
    result = {"cases": cases, "passed": sum(c["pass"] for c in cases), "total": len(cases),
              "trait_assertions": len(cases) * 2}
    (args.output / "review.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({"passed": result["passed"], "total": result["total"]}))
    if result["passed"] != result["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
