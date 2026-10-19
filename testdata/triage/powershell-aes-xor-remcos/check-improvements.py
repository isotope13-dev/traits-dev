#!/usr/bin/env python3
"""Static regression controls; samples are read and scanned, never executed."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--cleave", type=Path, default=ROOT.parent / "cleave/target/release/cleave")
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
decoded = "metadata/file/encoding::decoded-payload-layer"
mismatch = "metadata/file/extension/identity::pe-content-extension-mismatch"
settings = "metadata/binary/resource/identity::wide-settings-resource-name"
context = "well-known/malware/rat/remcos::remcos-rc4-settings-resource"
cooccurrence = "micro-behaviors/process/deploy::powershell-decrypt-eval-cooccurrence"
linked = "objectives/command-and-control/dropper/script-eval/embedded::ps-aes-iex-stage-loader"

with tempfile.TemporaryDirectory(prefix="remcos-trait-controls-") as tmp:
    tmp = Path(tmp)
    subprocess.run([
        "python3", str(Path(__file__).with_name("extract.py")),
        str(ROOT / "testdata/hostile/powershell-aes-xor-remcos.bin"), str(tmp),
    ], check=True, capture_output=True)
    payload = (tmp / "payload.exe").read_bytes()
    # Extraction coordinates have no author-selected extension. A subsequent
    # archive member has a real filename whose extension must still be checked.
    bodies = {
        "ordinary.vir": payload,
        "carrier.ps1##decimal-byte-array@41": payload,
        "carrier.ps1##base64@41!!member.vir": payload,
        "no-settings.exe": payload.replace("SETTINGS".encode("utf-16le"),
                                           "PREFDATA".encode("utf-16le")),
    }
    no_banner = payload
    for banner in [b"Remcos Agent initialized (", b"BreakingSecurity.net",
                   b"Breaking-Security.Net", b"* REMCOS v", b"Remcos_Mutex_Inj"]:
        no_banner = no_banner.replace(banner, b"X" * len(banner))
    bodies["no-family-banner.exe"] = no_banner
    for name, body in bodies.items():
        (tmp / name).write_bytes(body)
    source = (ROOT / "testdata/benign/powershell-decrypt-unrelated-eval.ps1").read_text()
    (tmp / "renamed-eval.ps1").write_text(
        source.replace("$payloadStatus", "$status").replace("Invoke-Expression", "iex"))
    paths = [tmp / name for name in bodies] + [
        tmp / "renamed-eval.ps1",
        ROOT / "testdata/benign/powershell-named-variable-eval.ps1",
        ROOT / "testdata/benign/powershell-decrypt-unrelated-eval.ps1",
        ROOT / "testdata/stranded-member-controls/crypto-eval-linked.ps1",
    ]
    run = subprocess.run([
        str(args.cleave.resolve()), "--traits-dir", str(ROOT), "--no-update-check",
        "--format", "json", *map(str, paths),
    ], env={**os.environ, "CLEAVE_SKIP_CACHE": "1"},
        text=True, capture_output=True, check=True)
    (args.output / "controls.stderr.txt").write_text(run.stderr)
    # Multiple top-level inputs produce adjacent JSON objects in JSON mode.
    decoder, rest, reports = json.JSONDecoder(), run.stdout, []
    while rest.strip():
        report, end = decoder.raw_decode(rest.lstrip())
        rest = rest.lstrip()[end:]
        reports.append(report)
    files = {f["path"]: f for r in reports for f in r["files"]}
    (args.output / "reports.json").write_text(json.dumps(reports) + "\n")
    result = []
    for path in paths:
        f = files[str(path)]
        ids = {t["id"] for t in f["traits"]}
        if path.name in bodies:
            assert (decoded in ids) == ("##decimal" in path.name), path.name
            assert (mismatch in ids) == path.name.endswith(".vir"), path.name
            assert (settings in ids) == (path.name != "no-settings.exe"), path.name
            assert (context in ids) == (path.name not in {
                "no-settings.exe", "no-family-banner.exe"}), path.name
        elif path.name == "crypto-eval-linked.ps1":
            assert linked in ids, "linked crypto output lost its execution finding"
        else:
            assert all(t["crit"] < 4 for t in f["traits"]), path.name
            assert (cooccurrence in ids) == (path.name != "powershell-named-variable-eval.ps1")
        result.append({"case": path.name, "pass": True})
    (args.output / "controls.json").write_text(json.dumps(result, indent=2) + "\n")
    (args.output / "reports.json").write_text(json.dumps(reports) + "\n")
    print(f"PASS: {len(result)} static improvement controls")
