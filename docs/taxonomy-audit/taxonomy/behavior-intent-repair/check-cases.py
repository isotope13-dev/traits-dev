"""Check atomscan JSONL reports; later reports replace earlier cases."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
MOVES = json.loads((HERE / "moves.json").read_text())["moves"]
IDS = {move["new"] for move in MOVES}
EXPECTED = {
    "credential-upload.js": {"vscode-credential-search-upload-preparation"},
    "credential-search-only.js": set(),
    "miner-service-stop.sh": {"service-disruption-with-miner-rival-clues"},
    "ordinary-service-stop.sh": set(),
    "service-cleanup.elf": {"systemd-cleanup-indicators"},
    "service-config-only.elf": set(),
    "service-cleanup.sh": set(),
    "service-config-only.sh": set(),
    "install-calculator.py": {
        "install-hook-calculator-execution-indicators", "exec-call-launches-calculator"
    },
    "calculator-only.py": {"exec-call-launches-calculator"},
    "calculator-unix.py": {"exec-call-launches-unix-calculator"},
    "calculator-macos.py": {"launch-command-opens-macos-calculator"},
    "install-only.py": set(),
    "generic-exports.js": set(),
    "crypto-interface.js": {
        "exports-encrypt-interface", "exports-cipher-interface",
        "exports-crypto-utilities-interface", "named-encryption-exports",
        "named-key-crypto-exports", "named-cipher-crypto-exports",
        "exports-crypto-interface", "cipher-factory-named-export-assignment",
        "hash-factory-named-export-assignment", "signature-factory-named-export-assignment",
        "node-crypto-export-import-near",
    },
    "crypto-operation.js": {
        "exports-encrypt-interface", "exports-crypto-interface",
        "node-crypto-export-import-near", "node-crypto-export-import-operation",
    },
    "insomnia-calculator.tgz": {
        "insomnia-plugin-calculator-execution-indicators", "exec-call-launches-calculator"
    },
    "insomnia-only.tgz": set(),
}

actual = {}
for report in sys.argv[1:]:
    for line in Path(report).read_text().splitlines():
        envelope = json.loads(line)
        grouped = {}
        for file in envelope["raw"]["files"]:
            name = Path(file["path"].split("!!")[0]).name
            grouped.setdefault(name, set()).update(
                trait["id"].split("::")[1]
                for trait in file.get("traits", []) if trait["id"] in IDS
            )
        actual.update(grouped)

for name, expected in EXPECTED.items():
    assert name in actual, f"Missing report: {name}"
    assert actual[name] == expected, (name, "expected", sorted(expected), "actual", sorted(actual[name]))
covered = set().union(*EXPECTED.values())
assert covered == {identifier.split("::")[1] for identifier in IDS}
print(f"Passed {len(EXPECTED)} cases; every relocated rule has a positive case")
