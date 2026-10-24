"""Check saved atomscan reports without executing any specimen code."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--reports", type=Path, required=True)
args = parser.parse_args()
here = Path(__file__).resolve().parent
moves = json.loads((here / "moves.json").read_text())
renames = {entry["old"]: entry["new"] for entry in moves}


def reports(name):
    return [json.loads(line) for line in (args.reports / name).read_text().splitlines()]


def findings(file, rename=False):
    result = {}
    for t in file.get("traits", []):
        id = renames.get(t["id"], t["id"]) if rename else t["id"]
        result[id] = max(t["crit"], result.get(id, 0))
    return result


def compare(before, after):
    def bucket(report):
        result = {}
        for f in report["raw"]["files"]:
            key = (f["path"], f["sha"])
            result.setdefault(key, {"traits": []})["traits"].extend(f.get("traits", []))
        return result
    left, right = bucket(before), bucket(after)
    assert len(before["raw"]["files"]) == len(after["raw"]["files"])
    assert left.keys() == right.keys(), "analyzed member population changed"
    losses, reductions = [], []
    for key, old in left.items():
        a, b = findings(old, True), findings(right[key])
        losses.extend({"path": key[0], "id": id} for id in a.keys() - b.keys())
        reductions.extend(
            {"path": key[0], "id": id, "before": a[id], "after": b[id]}
            for id in a.keys() & b.keys()
            if b[id] < a[id]
        )
    assert not losses, losses[:5]
    assert not reductions, reductions[:5]
    def counts(report):
        # Count distinct IDs across all members and fetched artifacts.
        levels = {}
        for file in report["raw"]["files"]:
            for t in file.get("traits", []):
                levels[t["id"]] = max(t["crit"], levels.get(t["id"], 0))
        return {
            "hostile": sum(v == 5 for v in levels.values()),
            "suspicious": sum(v == 4 for v in levels.values()),
            "notable": sum(v == 3 for v in levels.values()),
        }
    return {
        "analyzed_files": len(before["raw"]["files"]),
        "compared_file_keys": len(left),
        "before": counts(before),
        "after": counts(after),
        "ml_probability_before": before["ml"]["prob"],
        "ml_probability_after": after["ml"]["prob"],
        "ml_level_before": before["ml"]["lvl"],
        "ml_level_after": after["ml"]["lvl"],
        "lost_findings": losses,
        "severity_reductions": reductions,
    }


result = {}
for i, name in enumerate(["craft-native", "vcredist", "nvidia-skills"]):
    result[name] = compare(reports(f"before-{i}.json")[0], reports(f"final-{i}.json")[0])
result["clawhub-isolated"] = compare(
    reports("clawhub-before.json")[0], reports("clawhub-final.json")[0]
)

left = {d["raw"]["files"][0]["path"]: d for d in reports("retained-before.jsonl")}
right = {d["raw"]["files"][0]["path"]: d for d in reports("retained-final.json")}
result["external_positive_fixtures"] = {
    path: compare(report, right[path]) for path, report in left.items()
}

controls = {
    Path(d["raw"]["files"][0]["path"]).name: findings(d["raw"]["files"][0])
    for d in reports("controls-final.json")
}
kafka = "micro-behaviors/communications/messaging/pubsub::python-kafka-produce-call"
spctl = "micro-behaviors/os/security/gatekeeper::node-spctl-launch"
s3 = "micro-behaviors/communications/transfer::s5cmd-s3-upload-command"
session = "objectives/credential-access/phishing/mfa-relay::phishing-kit-operator-session-loop"
whoami = "micro-behaviors/process/identity/query::whoami-cmd-shell"
assert kafka in controls["kafka-positive.py"]
assert kafka not in controls["kafka-import-only.py"]
assert kafka not in controls["unrelated-produce.py"]
assert spctl in controls["spctl-positive.js"]
assert spctl not in controls["spctl-negative.js"]
assert s3 in controls["s3-upload.sh"]
assert s3 not in controls["s3-download.sh"]
assert session in controls["operator-session.js"]
assert session not in controls["bridge-ping.js"]
assert all(v < 4 for v in controls["sed-config.sh"].values())
assert "micro-behaviors/fs/write/file/shell::sed-inplace-edit-command" in controls["sed-config.sh"]
# Cleave filters neutral any/needs<=1 aggregators from compact scan output.
# The retained primitive must remain visible, and test-rules must confirm the
# grouping still resolves for its Rustdoor consumer.
assert "micro-behaviors/process/user/query::whoami-command-separator" in controls["whoami-positive.sh"]
assert f"MATCHED {whoami} (composite)" in (args.reports / "whoami-check.txt").read_text()
assert whoami not in controls["whoami-negative.sh"]
assert not any(id.startswith("well-known/malware/") for id in controls["whoami-positive.sh"])

result["focused_controls"] = {"checked": 12, "passed": True}
(here / "scan-comparison.json").write_text(json.dumps(result, indent=2) + "\n")
print("Preserved every mapped finding and severity in all reports; focused controls passed.")
