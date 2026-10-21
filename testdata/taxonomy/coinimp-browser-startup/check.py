import json
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[3]
CASES = [ROOT / "testdata/taxonomy/coinimp-browser-startup/cases.json",
         ROOT / "testdata/taxonomy/coinhive-miner-startup/cases.json",
         ROOT / "testdata/taxonomy/cryptoloot-miner-startup/cases.json"]

def check(case):
    result = subprocess.run(["cleave", "--traits-dir", str(ROOT), "--format", "json",
                             str(ROOT / case["path"])], text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    traits = [t for f in json.loads(result.stdout)["files"] for t in f["traits"]]
    ids = {t["id"] for t in traits}
    assert set(case.get("matched", [])) <= ids, (case["path"], "missing", set(case.get("matched", [])) - ids)
    assert not set(case.get("not_matched", [])) & ids, (case["path"], "unexpected", set(case.get("not_matched", [])) & ids)
    if "max_crit" in case:
        assert max([t["crit"] for t in traits], default=0) <= case["max_crit"], (case["path"], traits)
    return case["path"]

cases = [case for path in CASES for case in json.loads(path.read_text())["fixtures"]]
with ThreadPoolExecutor(max_workers=3) as pool:
    for path in pool.map(check, cases):
        print("PASS", path, flush=True)
print(f"Passed {len(cases)} controls")
