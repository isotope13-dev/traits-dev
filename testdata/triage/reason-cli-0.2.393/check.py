#!/usr/bin/env python3
"""Compile inert Mach-O controls; distinguish imports from strings/definitions.

No generated binary is executed. Requires macOS clang; outputs stay in /tmp.
"""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
APIS = {
    "SecKeyCreateRandomKey": "micro-behaviors/crypto/asymmetric/key::apple-seckey-generate-import",
    "SecKeyCopyExternalRepresentation": "micro-behaviors/crypto/asymmetric/key::apple-seckey-export-import",
    "SecKeyCreateSignature": "micro-behaviors/crypto/sign::apple-seckey-sign-import",
    "SecCodeCheckValidity": "micro-behaviors/os/security/gatekeeper::apple-running-code-validity-import",
    "SecStaticCodeCheckValidity": "micro-behaviors/os/security/gatekeeper::apple-file-code-validity-import",
    "CGPreflightScreenCaptureAccess": "micro-behaviors/hardware/display/screen::macos-screen-capture-permission-check-import",
    "CGRequestScreenCaptureAccess": "micro-behaviors/hardware/display/screen::macos-screen-capture-permission-request-import",
}


def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        obj, end = decoder.raw_decode(text)
        yield from obj["files"]
        text = text[end:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--sample-dir", type=Path)
    args = parser.parse_args()
    cases = {
        "imports": ("\n".join(f"extern void {name}(void);" for name in APIS)
                    + "\nvoid control(void) {" + "".join(f"{name}();" for name in APIS) + "}", set(APIS.values())),
        "strings": ("const char *names[] = {" + ",".join(json.dumps(name) for name in APIS) + "};", set()),
        "definitions": ("\n".join(f"void {name}(void) {{}}" for name in APIS), set()),
        "near-imports": ("\n".join(f"extern void {name}Decoy(void);" for name in APIS)
                         + "\nvoid control(void) {" + "".join(f"{name}Decoy();" for name in APIS) + "}", set()),
    }
    with tempfile.TemporaryDirectory(prefix="reason-apple-api-controls-") as directory:
        paths = []
        expected = {}
        for name, (source, wanted) in cases.items():
            src = Path(directory) / (name + ".c")
            dst = Path(directory) / (name + ".dylib")
            src.write_text(source)
            subprocess.run(["clang", "-arch", "x86_64", "-dynamiclib",
                            "-Wl,-undefined,dynamic_lookup", str(src), "-o", str(dst)], check=True)
            paths.append(dst)
            expected[dst.name] = wanted
        if args.sample_dir:
            base = args.sample_dir / "package/bin"
            for relative, wanted in [
                ("libreason_device_keychain.dylib", {APIS[k] for k in list(APIS)[:3]}),
                ("Background/Reason.app/Contents/MacOS/ReasonBackgroundIdentity", {APIS[k] for k in list(APIS)[3:5]}),
                ("Background/Reason.app/Contents/Helpers/ReasonPermissionTile", {APIS[k] for k in list(APIS)[5:]}),
            ]:
                paths.append(base / relative)
                expected[paths[-1].name] = wanted
        result = subprocess.run([args.cleave, "--traits-dir", str(ROOT), "--format", "json",
                                 *map(str, paths)], check=True, text=True, capture_output=True)
        seen = set()
        for report in reports(result.stdout):
            name = Path(report["path"]).name
            actual = {t["id"] for t in report.get("traits", [])} & set(APIS.values())
            assert actual == expected[name], (name, actual, expected[name])
            seen.add(name)
            print(f"PASS {name}: {len(actual)} API imports")
        assert seen == set(expected), (seen, set(expected))


if __name__ == "__main__":
    main()
