"""Check precise response-host, key-token and Lua-call boundaries."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
cases = json.loads((HERE / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--json", "analyze", *[str(HERE / name) for name in cases]],
    check=True, capture_output=True, text=True,
)
observed = {}
# JSON strings may contain Unicode NEL characters; only LF separates reports.
for line in result.stdout.split("\n"):
    if line:
        for item in json.loads(line).get("files", []):
            observed[Path(item["path"]).name] = {
                trait["id"] for trait in item.get("traits", [])
            }
count = 0
for name, expected in cases.items():
    assert name in observed, name
    for rule, wanted in expected.items():
        actual = rule in observed[name]
        assert actual == wanted, (name, rule, wanted, actual)
        count += 1
print(f"PASS: {len(cases)} fixtures, {count} assertions")
