"""Static matcher controls; never execute these fixture programs."""
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
cases = json.loads((root / "cases.json").read_text())
run = subprocess.run(["cleave", "--traits-dir", ".", "--format", "json",
                      *(str(root / case["file"]) for case in cases)],
                     capture_output=True, text=True)
if run.returncode:
    raise SystemExit(run.stderr or run.stdout)
by_path = {}
remaining = run.stdout.strip()
while remaining:
    result, end = json.JSONDecoder().raw_decode(remaining)
    by_path.update({f["path"]: {t["id"] for t in f.get("traits", [])}
                    for f in result["files"]})
    remaining = remaining[end:].strip()
for case in cases:
    ids = by_path[str(root / case["file"])]
    assert set(case["present"]) <= ids, (case["file"], "missing", set(case["present"]) - ids)
    assert not set(case["absent"]) & ids, (case["file"], "unexpected", set(case["absent"]) & ids)
    requested = case.get("debug_present", []) + case.get("debug_absent", [])
    if requested:
        debug = subprocess.run(["cleave", "--traits-dir", ".", "test-rules",
                                str(root / case["file"]), "--rules", ",".join(requested)],
                               check=True, capture_output=True, text=True)
        matched = {line.split()[1] for line in debug.stdout.splitlines()
                   if line.startswith("MATCHED ")}
        assert set(case.get("debug_present", [])) <= matched, debug.stdout
        assert not set(case.get("debug_absent", [])) & matched, debug.stdout
    print("PASS", case["file"])
