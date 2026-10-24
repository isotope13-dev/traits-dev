"""Check parsed command positions without executing the shell fixtures."""
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TRAIT = "objectives/anti-static/obfuscation/encoding/hex::shell-ansi-hex-command-word"
EXPECTED = {
    "command-word.sh": True,
    "data-and-documentation.sh": False,
    "plaintext-command.sh": False,
    "nonhex-command.sh": False,
}

run = subprocess.run(
    ["cleave", "--no-update-check", "--traits-dir", str(ROOT), "--json",
     *(str(HERE / name) for name in EXPECTED)],
    capture_output=True, text=True, check=True,
)
seen = set()
for line in run.stdout.splitlines():
    for file in json.loads(line)["files"]:
        if file.get("depth", 0) != 0:
            continue
        name = Path(file["path"]).name
        matches = [t for t in file.get("traits", []) if t["id"] == TRAIT]
        assert bool(matches) == EXPECTED[name], (name, matches, run.stderr)
        assert all(t["crit"] == 4 for t in matches), matches
        seen.add(name)
        print("PASS", name, bool(matches))
assert seen == set(EXPECTED), seen
