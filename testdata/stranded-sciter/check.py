#!/usr/bin/env python3
"""Check timer placement and DLL-bound DNS ordinals without executing PEs."""
import argparse
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
TIMER = "micro-behaviors/time/schedule/callback::time-set-event"
OLD_TIMER = "micro-behaviors/hardware/input/audio::time-set-event"
DNS = "micro-behaviors/communications/dns/lookup::winsock-name-resolution-ordinal"
OLD_DNS = "micro-behaviors/communications/ip/resolve::winsock-name-resolution-ordinal"
DACIC = "well-known/malware/trojan/dacic::winmm-mscms-noise-imports"
TLS = "micro-behaviors/communications/tls/verify/disable::x86-wininet-ignore-unknown-ca"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", action="store_true")
    parser.add_argument("--scratch-dir", type=Path, required=True)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location(
        "pe_controls", ROOT / "testdata/taxonomy/pe-review-boundaries/check.py")
    controls = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(controls)

    def ordinal_pe(owned, other):
        # Keep WS2_32 present while varying which descriptor owns the ordinal.
        image = controls.pe({"WS2_32.dll": ["placeholder"] * len(owned),
                             "other.dll": ["placeholder"] * len(other)})
        for i, ordinals in enumerate([owned, other]):
            lookup, _, _, _, iat = struct.unpack_from("<IIIII", image, 0xA00 + 20*i)
            for n, ordinal in enumerate(ordinals):
                for table in [lookup, iat]:
                    struct.pack_into("<Q", image, table - 0x3000 + 0xA00 + 8*n,
                                     (1 << 63) | ordinal)
        return image

    timer = OLD_TIMER if args.before else TIMER
    cases = []
    for ordinal in [51, 52]:
        required = {DNS, OLD_DNS} if args.before else {DNS}
        cases.append((f"winsock-owns-{ordinal}", ordinal_pe([ordinal], [777]), required, set()))
        required = {OLD_DNS} if args.before else set()
        forbidden = {DNS} if args.before else {DNS, OLD_DNS}
        cases.append((f"other-dll-owns-{ordinal}", ordinal_pe([115], [ordinal]), required, forbidden))
    cases += [
        ("timer-import", controls.pe({"WINMM.dll": ["timeSetEvent"]}), {timer}, {DACIC}),
        ("timer-name-only", controls.pe({}, data=b"timeSetEvent\0"), set(), {TIMER, OLD_TIMER, DACIC}),
        ("audio-only", controls.pe({"WINMM.dll": ["waveOutOpen"]}), set(), {TIMER, OLD_TIMER, DACIC}),
    ]
    # Preserve the existing malware consumer's import profile across the move.
    profile = controls.pe({
        "WINMM.dll": ["timeSetEvent", "waveOutOpen", "mciSendStringA"],
        "MSCMS.dll": ["CreateColorTransformA", "RegisterCMMW", "TranslateBitmapBits"],
    })
    profile.extend(b"\0" * (65536 - len(profile)))
    cases.append(("dacic-consumer-profile", profile, {timer, DACIC}, set()))
    if not args.before:
        spec = importlib.util.spec_from_file_location(
            "pe32_controls", ROOT / "testdata/native-post-graft-review/run_cases.py")
        pe32 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pe32)

        def tls_pe(setter="InternetSetOptionW", base=0x400000, slot=0xFC):
            code = bytes.fromhex("814dfc000100006a048d45fc506a1f53ff15")
            code = bytearray(code + struct.pack("<I", base + 0x20A0))
            code[2] = code[11] = slot
            image = pe32.pe(b"\xc3" + b"\x90" * 31 + code, b"", base)
            struct.pack_into("<II", image, 0x98 + 104, 0x2000, 40)
            struct.pack_into("<IIIII", image, 0x400, 0x20A0, 0, 0, 0x2070, 0x20A0)
            image[0x470:0x47B] = b"WININET.dll"
            struct.pack_into("<III", image, 0x4A0, 0x20C0, 0x20E0, 0)
            raw = b"\0\0" + setter.encode() + b"\0"
            image[0x4C0:0x4C0+len(raw)] = raw
            image[0x4E0:0x4F3] = b"\0\0InternetReadFile\0"
            return image

        def patched(image, offset, replacement):
            image = bytearray(image)
            image[offset:offset+len(replacement)] = replacement
            return image

        positive = tls_pe()
        cases += [
            ("tls-wide-setter", positive, {TLS}, set()),
            ("tls-ansi-relocated", tls_pe("InternetSetOptionA", 0x500000, 0xF0), {TLS}, set()),
            ("tls-other-mask", patched(positive, 0x224, b"\x02"), set(), {TLS}),
            ("tls-other-buffer", patched(positive, 0x22B, b"\xf8"), set(), {TLS}),
            ("tls-other-option", patched(positive, 0x22E, b"\x1e"), set(), {TLS}),
            ("tls-other-import", patched(positive, 0x232, struct.pack("<I", 0x4020A4)), set(), {TLS}),
            ("tls-nonexecutable-section", patched(positive, 0x178+36, struct.pack("<I", 0x40000040)), set(), {TLS}),
            ("tls-api-name-only", controls.pe({}, data=b"InternetSetOptionW\0SECURITY_FLAG_IGNORE_UNKNOWN_CA\0"), set(), {TLS}),
        ]
    with tempfile.TemporaryDirectory(prefix="sciter-controls-", dir=args.scratch_dir) as temp:
        for name, binary, required, forbidden in cases:
            path = Path(temp, name + ".exe")
            path.write_bytes(binary)
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(ROOT), "--disable", "radare2",
             "--format", "json", temp], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert not any(s in result.stderr for s in ["skipped", "failed to compile"]), result.stderr
        files = {}
        remaining = result.stdout.lstrip()
        while remaining:
            report, end = json.JSONDecoder().raw_decode(remaining)
            files.update({Path(f["path"]).stem: f for f in report["files"]})
            remaining = remaining[end:].lstrip()
        for name, _, required, forbidden in cases:
            ids = {t["id"] for t in files[name].get("traits", [])}
            assert required <= ids, (name, "missing", required - ids)
            assert not forbidden & ids, (name, "unexpected", forbidden & ids)
            if not args.before:
                assert not {OLD_TIMER, OLD_DNS} & ids, (name, "retired ID")
            print("PASS", name, flush=True)


if __name__ == "__main__":
    main()
