"""Run controls outside testdata so test-path exclusions cannot hide failures."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
with tempfile.TemporaryDirectory(prefix="drift-controls-") as directory:
    targets = []
    for case in cases:
        target = Path(directory) / Path(case["path"]).name
        shutil.copyfile(root / case["path"], target)
        targets.append(str(target))
    result = subprocess.run(
        ["cleave", "--traits-dir", str(root), "--format", "json", "analyze", *targets],
        check=True, capture_output=True, text=True,
    )
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    findings = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        for file in report["files"]:
            findings[Path(file["path"]).name] = {
                trait["id"] for trait in file.get("traits", [])
            }
        remaining = remaining[end:].lstrip()
    for case in cases:
        actual = findings[Path(case["path"]).name]
        assert set(case["matched"]) <= actual, (case["path"], "missing", actual)
        assert not set(case["not_matched"]) & actual, (case["path"], "unexpected", actual)
        print("PASS", Path(case["path"]).name)
