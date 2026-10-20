"""Run inert positive and near-miss controls for S3 release-diff corrections."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


here = Path(__file__).resolve().parent
repo = here.parent.parent
cases = json.loads((here / "cases.json").read_text())
# Paths under testdata can activate generic testing exclusions. Scan copies in
# a neutral directory so the negative controls exercise the actual matchers.
temporary = tempfile.TemporaryDirectory(prefix=".s3-controls-", dir=repo)
staged = Path(temporary.name)
for name in cases:
    shutil.copyfile(here / name, staged / name)
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(repo),
     "--format", "json", "--all-files", *[str(staged / name) for name in cases]],
    capture_output=True, text=True, check=True,
)
if result.stderr.strip():
    raise AssertionError(result.stderr)

# The directory/multipath renderer can concatenate JSON records without LF.
decoder = json.JSONDecoder()
pending = result.stdout.strip()
files = {}
while pending:
    document, end = decoder.raw_decode(pending)
    pending = pending[end:].lstrip()
    for item in document.get("files", [document]):
        files[Path(item["path"]).name] = item

for name, case in cases.items():
    findings = {t["id"]: t for t in files[name].get("traits", [])}
    traits = set(findings)
    missing = set(case.get("present", [])) - traits
    unexpected = set(case.get("absent", [])) & traits
    assert not missing, (name, "missing", sorted(missing))
    assert not unexpected, (name, "unexpected", sorted(unexpected))
    for trait, count in case.get("evidence_counts", {}).items():
        assert len(findings[trait].get("spans", [])) == count, (name, trait)
    # Transparent OR composites may be deduplicated from emitted findings.
    # Verify their matching independently of presentation.
    if case.get("matched_rules"):
        debug = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(repo),
             "test-rules", str(staged / name), "--rules",
             ",".join(case["matched_rules"])],
            capture_output=True, text=True, check=True,
        )
        for trait in case["matched_rules"]:
            assert any(line.startswith("MATCHED " + trait + " ")
                       for line in debug.stdout.splitlines()), debug.stdout
    print("PASS", name)
temporary.cleanup()
print(f"Passed {len(cases)} focused controls")
