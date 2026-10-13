import json
import subprocess
from pathlib import Path

cases = json.loads(Path(__file__).with_name("cases.json").read_text())
for case in cases["fixtures"]:
    result = subprocess.run(["cleave", "--traits-dir", ".", "--format", "json", case["path"]], check=True, capture_output=True, text=True)
    report = json.loads(result.stdout)
    traits = {t["id"]: t for f in report["files"] for t in f.get("traits", [])}
    missing = set(case["required_emitted"]) - traits.keys()
    unexpected = set(case["not_matched"] + case["forbidden_emitted"]) & traits.keys()
    if case["path"].endswith("contact.py"):
        debug = subprocess.run(["cleave", "--traits-dir", ".", "test-rules", case["path"], "--rules", case["matched"][0]], check=True, capture_output=True, text=True)
        assert "MATCHED " + case["matched"][0] in debug.stdout, debug.stdout
    convictions = [t["id"] for t in traits.values() if t["crit"] >= 4]
    assert not missing and not unexpected and (not convictions or case.get("malicious")), (case["path"], missing, unexpected, convictions)
    print("PASS", case["path"], flush=True)
