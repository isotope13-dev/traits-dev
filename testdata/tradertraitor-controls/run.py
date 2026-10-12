#!/usr/bin/env python3
"""Static regression scan; never executes samples. Exit 0 means every case passed.

Run from any directory: python3 testdata/tradertraitor-controls/run.py
The ignored samples/ fixtures are included in the integration transfer bundle.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(os.environ.get("TRADERTRAITOR_SAMPLE_DIR",
                              str(ROOT / "samples/hostile/tradertraitor")))
OUT = Path(os.environ.get("TRADERTRAITOR_RESULTS", "/tmp/tradertraitor-results.json"))
SAMPLES = {
    "terraform-provider-awsbeta_v1.0.0": ("9d78ece09457907b730d139e4e0c64dd", 4),
    "safari_updater.sh": ("73adaea97f003735335505858c1c6def", 3),
    "roofdeck-macos-arm64": ("2b81aceab0142472d94eb42e500b27b1", 4),
    "roofdeck-windows.exe": ("9d88b4494c7bc27b10358b68a899ad54", 4),
}


def main():
    expected = {}
    def source_path(name):
        if name == "safari_updater.sh":
            return ROOT / "testdata/hostile/tradertraitor-safari-updater.sh"
        return FIXTURES / name

    with tempfile.TemporaryDirectory(prefix="tradertraitor-cases-") as tmp:
        inputs = Path(tmp)
        for name, (md5, count) in SAMPLES.items():
            data = source_path(name).read_bytes()
            assert hashlib.md5(data).hexdigest() == md5, name + " hash mismatch"
            shutil.copyfile(source_path(name), inputs / name)
            expected[name] = count

        def variant(source, name, substitutions, expected_count):
            data = source_path(source).read_bytes()
            for old, new in substitutions:
                assert old in data, (source, old)
                if not source.endswith(".sh"):
                    assert len(old) == len(new), (old, new)
                data = data.replace(old, new)
            (inputs / name).write_bytes(data)
            expected[name] = expected_count

        variant("terraform-provider-awsbeta_v1.0.0", "renamed-provider", [
            (b"awsbeta", b"cloudxx"), (b"safari_updater", b"worker_updater")], 3)
        host = b"diagnose.hashicorp-terraform.io"
        replacement = b"telemetry.vendor.example".ljust(len(host), b"x")
        variant("terraform-provider-awsbeta_v1.0.0", "rotated-provider-domain", [
            (host, replacement)], 4)
        variant("terraform-provider-awsbeta_v1.0.0", "provider-without-stager", [
            (b"write failed: %wchmod failed: %wstart failed: %w",
             b"write status: %wchmod status: %wstart status: %w")], 0)
        variant("roofdeck-macos-arm64", "roofdeck-without-reverse-shell", [
            (b"Reverse shell started successfully.",
             b"Local session started successfully.")], 0)
        variant("safari_updater.sh", "renamed-font-loader.sh", [
            (b"@@ENDFONT@@", b"@@DATAEND@@"),
            (b"SAVE_PATH", b"DEST_PATH"), (b"ENC_PATH", b"SRC_PATH")], 3)
        variant("safari_updater.sh", "font-decoder-without-execute-mode.sh", [
            (b"chmod +x", b"printf x")], 0)
        for name in ["font-preview.sh", "encrypted-installer.sh", "nostr-client.rs"]:
            shutil.copyfile(ROOT / "testdata/tradertraitor-controls" / name, inputs / name)
            expected[name] = 0
        shutil.copyfile(ROOT / "samples/benign/tradertraitor-controls/null-provider",
                        inputs / "official-null-provider")
        expected["official-null-provider"] = 0

        env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), CLEAVE_SKIP_CACHE="1")
        proc = subprocess.run([
            "atomscan", "--no-update", "--follow=none", "--mode=slow",
            "--level", "25", "--format=json", str(inputs)],
            capture_output=True, text=True, env=env)
        # Atomscan returns nonzero when hostile artifacts are found.
        results = []
        seen = set()
        for line in proc.stdout.splitlines():
            report = json.loads(line)
            for file in report.get("raw", {}).get("files", []):
                name = Path(file["path"]).name
                if name not in expected:
                    continue
                severe = [t for t in file["traits"] if t["crit"] in (4, 5)]
                hostile = [t["id"] for t in severe if t["crit"] == 5]
                level = report["ml"]["lvl"]
                want = expected[name]
                passed = (len(hostile) >= want and 0 <= level <= 25) if want else not hostile
                results.append({"file": name, "hostile_count": len(hostile),
                                "hostile_traits": hostile, "level": level,
                                "expected_hostile_min": want, "passed": passed})
                seen.add(name)
        missing = sorted(set(expected) - seen)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps({"level": 25, "cases": results,
                                   "missing": missing}, indent=2) + "\n")
        for result in results:
            print(("PASS" if result["passed"] else "FAIL"), result["file"],
                  "hostile=" + str(result["hostile_count"]), "level=" + str(result["level"]))
        if missing or any(not result["passed"] for result in results):
            print(proc.stderr[-4000:])
            raise SystemExit("Failed cases or missing results: " + repr(missing))


if __name__ == "__main__":
    main()
