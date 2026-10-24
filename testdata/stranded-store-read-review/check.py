"""Check static observations only; never execute the AppleScript fixtures."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--installer", type=Path)
parser.add_argument("--decoded-command", type=Path)
args = parser.parse_args()
base = Path(__file__).parent
rules = [
    "objectives/credential-access/keychain/theft::password-phishing-keychain-store-read-profile",
    "objectives/credential-access/browser/chromium::password-phishing-chromium-store-read-profile",
]
cases = [(base / name, expected)
         for name, expected in json.loads((base / "cases.json").read_text()).items()]
for path in (args.installer, args.decoded_command):
    if path:
        cases.append((path, [True, True]))
for path, expected in cases:
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", ".",
         "test-rules", str(path), "--rules", ",".join(rules)],
        capture_output=True, text=True, check=True,
    )
    actual = [any(line.startswith("MATCHED " + rule + " ")
                  for line in result.stdout.splitlines()) for rule in rules]
    assert actual == expected, (path, expected, actual, result.stdout, result.stderr)
    print(f"{path.name}: {actual}", flush=True)
