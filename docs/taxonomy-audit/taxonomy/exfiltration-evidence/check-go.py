# /// script
# dependencies = ["pyyaml"]
# ///
"""Check the Go exfiltration review and explicitly documented changes."""
import copy
import json
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
review = json.loads((HERE / "go-moves.json").read_text())
for move in review["moves"]:
    doc = yaml.safe_load((ROOT / move["destination"]).read_text())
    name = move["new"].split("::")[1]
    rule = next(r for r in doc["composite_rules"] if r["id"] == name)
    before = {**copy.deepcopy(move["defaults"]), **copy.deepcopy(move["before"])}
    after = {**(doc.get("defaults") or {}), **rule}
    for value in (before, after):
        value.pop("id", None)
        value.pop("desc", None)
    if name == "dns-and-environment-observations":
        for key in ("attack", "mbc", "unless", "downgrade"):
            before.pop(key, None)
        before["crit"] = "baseline"
        before["for"] = ["go"]
        before["all"][1]["id"] = "micro-behaviors/os/env/read/variable::go-env-access"
    assert before == after, move["old"]
assert len(review["removed"]) == 1
assert not (ROOT / "objectives/exfiltration/sensitive-data/source/go.yaml").exists()
print("Verified three reviewed rules and the generic wrapper removal")
