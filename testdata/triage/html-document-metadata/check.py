"""Verify HTML metadata boundaries without executing embedded scripts."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
engine = os.environ.get("CLEAVE", "cleave")
# Remove the testdata path, which intentionally suppresses the Unicode finding.
with tempfile.TemporaryDirectory(prefix=".html-metadata-", dir=ROOT) as temporary:
    paths = {}
    for case in cases:
        source = ROOT / case["path"]
        target = Path(temporary) / source.name
        shutil.copyfile(source, target)
        paths[case["path"]] = target
    result = subprocess.run(
        [engine, "--traits-dir", str(ROOT), "--min-crit", "component",
         "--format", "jsonl", *map(str, paths.values())],
        text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    files = {str(Path(f["path"]).resolve()): f
             for line in result.stdout.splitlines()
             for f in json.loads(line)["files"]}
    for case in cases:
        traits = {t["id"] for t in files[str(paths[case["path"]])]["traits"]}
        assert set(case["required_emitted"]) <= traits, (case["path"], set(case["required_emitted"]) - traits)
        assert not set(case["forbidden_emitted"]) & traits, (case["path"], traits & set(case["forbidden_emitted"]))
        # Root matching is checked on an active document and a rootless fragment.
        # Unreferenced baseline traits may be stripped from scan output.
        if paths[case["path"]].name not in ("active.html", "fragment.html"):
            continue
        root_trait = "metadata/document/html::html-root-at-start"
        trace = subprocess.run(
            [engine, "--traits-dir", str(ROOT), "test-rules",
             str(paths[case["path"]]), "--rules", root_trait],
            text=True, capture_output=True, check=True,
        ).stdout
        assert ("\nMATCHED " + root_trait + " (trait)" in trace) == (root_trait in case["matched"]), trace
print(f"{len(cases)} HTML metadata controls passed")
