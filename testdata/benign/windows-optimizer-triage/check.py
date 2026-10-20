"""Check authorized tuning and exclusion-removal boundaries from cleave JSON."""
import json
import sys
from pathlib import Path

decoder = json.JSONDecoder()
remaining = Path(sys.argv[1]).read_text()
files = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for item in report["files"]:
        files[Path(item["path"]).name] = item

process = "micro-behaviors/os/security/defender::defender-exclusion-process"
policy = "micro-behaviors/os/registry/keys/policy::"
policies = {
    policy + "hvci-scenario-registry-path",
    policy + "vbs-enable-policy-value",
    policy + "speculative-execution-mitigation-policy-value",
}
positive = {"optimizer.ps1", "optimizer-carrier.exe"}
negative = {
    "remove-exclusion.ps1", "parameter-only.ps1", "path-add-process-remove.ps1",
    "removal-carrier.exe", "unrelated-settings.ps1",
}
for name in sorted(positive | negative):
    traits = files[name]["traits"]
    ids = {t["id"] for t in traits}
    assert not any(t["crit"] == 5 for t in traits), name
    suspicious = {t["id"] for t in traits if t["crit"] == 4}
    assert suspicious == ({process} if name in positive else set()), (name, suspicious)
    if name in positive:
        assert policies <= ids, (name, policies - ids)
    if name == "unrelated-settings.ps1":
        assert not policies & ids, name
    print("PASS", name)
