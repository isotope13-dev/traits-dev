"""Check rekeying, missing execution, comments and patched PEB-load controls."""
import json
import os
from pathlib import Path
import subprocess
import sys

here = Path(__file__).resolve().parent
repo = here.parents[1]
if len(sys.argv) > 1:
    source = Path(sys.argv[1]).read_text()
else:
    env = dict(os.environ, CLEAVE_SKIP_CACHE="1")
    source = subprocess.check_output(
        ["cleave", "--traits-dir", str(repo), "--format", "json", str(here)],
        env=env, text=True,
    )
actual = {}
decoder = json.JSONDecoder()
while source.strip():
    report, end = decoder.raw_decode(source.lstrip())
    source = source.lstrip()[end:]
    for item in report.get("files", []):
        actual[Path(item["path"]).name] = sorted(
            trait["id"] for trait in item.get("traits", []) if trait["crit"] == 5
        )
expected = json.loads((here / "expected-hostile.json").read_text())
for name, traits in expected.items():
    assert actual.get(name) == sorted(traits), (name, actual.get(name), traits)
print(f"Passed {len(expected)} date-key browser controls")
