"""Check shared hex precision, generic layout context and capture calls."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CASES = Path(__file__).with_name("cases.json")


def run(*args):
    result = subprocess.run(
        ["cleave", "--traits-dir", str(ROOT), *args],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    return result.stdout


for case in json.loads(CASES.read_text())["fixtures"]:
    report = json.loads(run("--format", "json", case["path"]))
    ids = {t["id"] for f in report["files"] for t in f.get("traits", [])}
    assert set(case["matched"]) <= ids, case
    assert not set(case["not_matched"]) & ids, case
    # Components may match internally while being omitted from final output.
    if case.get("trace_matched"):
        trace = run("test-rules", case["path"], "--rules",
                    ",".join(case["trace_matched"]))
        for trait in case["trace_matched"]:
            assert any(line.startswith(f"MATCHED {trait} (")
                       for line in trace.splitlines()), (case, trait, trace)
    print("PASS", case["path"])

# Existing, independently maintained attack fixture outside this batch.
wheel = "testdata/hostile/supply-chain-corpus/py/pypi-sablewoodcore-dns-creds-exfil-macos.whl"
report = json.loads(run("--format", "json", wheel))
member = next(f for f in report["files"] if f["path"].endswith("/bench.py"))
ids = {t["id"] for t in member.get("traits", [])}
assert "micro-behaviors/data/encode/hex::python-bytes-hex-call" in ids
assert "objectives/exfiltration/stealer/dev-secret::hex-developer-credential-dns-exfil" in ids
print("PASS existing credential DNS attack, including wheel member")
