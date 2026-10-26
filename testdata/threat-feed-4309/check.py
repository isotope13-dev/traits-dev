"""Verify path variants and benign near misses without executing fixtures."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
parser.add_argument("--fixtures", type=Path, required=True)
parser.add_argument("--report", type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
subprocess.run([args.cleave, "--traits-dir", str(root), "--json",
                str(args.fixtures), "-o", str(args.report)], check=True)
rules = {"micro-behaviors/fs/path/secret-config::" + name for name in (
    "cargo-credentials-path-marker", "rubygems-credentials-path-marker",
    "composer-auth-file")}
negative = {"near-miss.py", "wrong-boundary.py", "prose.py",
            "unrelated-crypto-exec.py"}
positive = {"joined.py", "joined.js", "joined.ts", "joined.go", "joined.rb",
            "Joined.java", "Joined.cs", "joined.rs", "joined.php",
            "windows.ps1", "windows.js", "path-catalog.py"}
seen = set()
for line in args.report.read_text().splitlines():
    report = json.loads(line)
    for file in report["files"]:
        name = Path(file["path"]).name
        assert name in positive | negative, name
        seen.add(name)
        traits = {trait["id"]: trait for trait in file.get("traits", [])}
        expected = rules if name in positive else set()
        assert rules & traits.keys() == expected, (name, rules & traits.keys())
        assert not any(t["crit"] == 5 for t in traits.values()), name
        assert all(traits[r]["crit"] == 3 for r in expected), name
        assert "objectives/execution/payload/script-eval::python-decrypted-payload-script-eval" not in traits
assert seen == positive | negative, seen
print(f"PASS: {len(seen)} fixtures; path facts remain notable; no hostile controls")
