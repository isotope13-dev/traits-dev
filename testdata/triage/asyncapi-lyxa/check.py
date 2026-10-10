import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[3]
fixture_dir = Path(__file__).resolve().parent
result = subprocess.run(
    ["cleave", "--traits-dir", str(root), "--format", "json", str(fixture_dir)],
    check=True, capture_output=True, text=True,
)
remaining = result.stdout
files = []
decoder = json.JSONDecoder()
while remaining.strip():
    remaining = remaining.lstrip()
    document, end = decoder.raw_decode(remaining)
    files.extend(document.get("files", [document]))
    remaining = remaining[end:]
for case in json.loads((fixture_dir / "cases.json").read_text())["fixtures"]:
    file = next(f for f in files if f["path"].endswith(case["path"]))
    ids = {t["id"] for t in file.get("traits", [])}
    assert not (set(case["matched"]) - ids), case["path"]
    assert not (set(case["not_matched"]) & ids), case["path"]
print("Three triage regression controls passed")
