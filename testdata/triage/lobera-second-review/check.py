#!/usr/bin/env python3
"""Check rule placement, retained attacks, and benign near misses."""
import json
from pathlib import Path
import subprocess
import tempfile
import shutil

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())
scratch = root.parents[1] / "scratch"
with tempfile.TemporaryDirectory(prefix="lobera-controls-", dir=scratch) as work:
  staged_cases = []
  for case in cases:
    source = root / case["path"]
    # Run the content under a neutral runtime path, avoiding test-directory
    # exclusions; retain nested identity directories where the path is evidence.
    rel = case["path"].split("lobera-second-review/")[-1] if "lobera-second-review/" in case["path"] else source.name
    staged = Path(work) / rel
    staged.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, staged)
    staged_cases.append((case, staged))
  proc = subprocess.run(["cleave", "--traits-dir", str(root), "--format", "json", work], text=True, capture_output=True)
  assert proc.returncode == 0, proc.stderr
  reports = []
  pending = proc.stdout.lstrip()
  decoder = json.JSONDecoder()
  while pending:
    report, end = decoder.raw_decode(pending)
    reports.append(report)
    pending = pending[end:].lstrip()
  by_path = {f["path"]: f for report in reports for f in report["files"]}
  for case, staged in staged_cases:
    traits = {t["id"] for t in by_path[str(staged)].get("traits", [])}
    missing = set(case["present"]) - traits
    unexpected = set(case["absent"]) & traits
    assert not missing and not unexpected, (case["path"], sorted(missing), sorted(unexpected))
    print("PASS", case["path"])
print(f"Passed {len(cases)} cases")
