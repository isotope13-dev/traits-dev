"""Scan positive and near-miss fixtures; never execute their code."""
import json, os, shutil, subprocess, tempfile
from pathlib import Path
root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
paths = list(dict.fromkeys(c["path"] for c in cases))
# Remove the testdata container, preserving skills/<name>/ member semantics.
# Otherwise legacy path-based test exclusions would hide live positive cases.
with tempfile.TemporaryDirectory(prefix="rule-review-", dir=root) as temporary:
    scan_paths = {}
    for path in paths:
        target = Path(temporary) / Path(path).relative_to("testdata/taxonomy")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / path, target)
        scan_paths[path] = str(target)
    r = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--json", *scan_paths.values()], cwd=root, capture_output=True, text=True, check=True)
reports = {f["path"]: f for line in r.stdout.splitlines() if line.strip() for f in json.loads(line)["files"]}
if os.environ.get("REVIEW_REPORT"):
    Path(os.environ["REVIEW_REPORT"]).write_text(r.stdout)
errors = []
for c in cases:
    traits = {t["id"]: t for t in reports[scan_paths[c["path"]]].get("traits", [])}
    # Exceptions are intentionally absent from emitted reports. Their effect
    # is checked by the corresponding not_matched hostile findings.
    emitted = set(c.get("matched", [])) - {
        "objectives/evasion/security-bypass/llm/override::prompt-injection-documentation-known-benign-context"
    }
    missing = emitted - traits.keys()
    unexpected = set(c.get("not_matched", [])) & traits.keys()
    if missing or unexpected:
        errors.append((c["path"], sorted(missing), sorted(unexpected)))
    for name, severity in c.get("criticalities", {}).items():
        if name in traits and traits[name]["crit"] != severity:
            errors.append((c["path"], name, traits[name]["crit"], severity))
assert not errors, errors
print(f"{len(cases)} behavior, placement and near-miss controls passed")
