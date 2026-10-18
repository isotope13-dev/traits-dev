"""Check decoder capability, pipeline binding, and objective boundaries.

Copies controls outside testdata so test-directory exclusions cannot mask them.
Never executes the shell snippets.
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
DEC = "micro-behaviors/data/decode/"
PIPE = "micro-behaviors/process/create/shell/pipeline::base64-decode-shell-stdin"
OBJ = "objectives/anti-static/obfuscation/encoding/base64::double-base64-pipe-sh"
SEQ = DEC + "multiple-encoding::xxd-base64-decode-sequence"
STACK = DEC + "multiple-encoding::stacked-decode-pipeline"
DOUBLE = DEC + "base64::double-base64-decode"

CASES = [
    ("layered", 'echo "$h" | xxd -r -p | base64 -d | base64 -d | sh\n',
     {SEQ: 3, STACK: 3, DOUBLE: 3, PIPE: 3, OBJ: 4}, []),
    ("single", 'echo "$value" | base64 -d | sh\n', {PIPE: 3}, [OBJ, DOUBLE, SEQ]),
    ("data", 'echo "$value" | base64 -d | base64 -d > output.txt\n',
     {STACK: 3, DOUBLE: 3}, [PIPE, OBJ, SEQ]),
    ("mixed", 'echo "$value" | xxd -r -p | base64 -d > output.txt\n',
     {STACK: 3, SEQ: 3}, [PIPE, OBJ, DOUBLE]),
    ("sequence", 'xxd -r -p input.hex\nbase64 -d other.txt\n',
     {SEQ: 3}, [PIPE, STACK, DOUBLE, OBJ]),
    ("independent", 'echo "$value" | base64 -d | base64 -d > output.txt\n'
     'echo "$other" | base64 -d | sh\n', {DOUBLE: 3, PIPE: 3}, [OBJ]),
    ("substitution", 'echo "$(base64 -d input.txt)" | sh\n', {}, [PIPE, OBJ]),
    ("longopts", 'echo "$value" | base64 --decode | base64 --decode | sh\n',
     {STACK: 3, DOUBLE: 3, PIPE: 3, OBJ: 4}, [SEQ]),
]

with tempfile.TemporaryDirectory(prefix="decoder-controls-", dir=os.environ.get("TMPDIR")) as tmp:
    for name, source, present, absent in CASES:
        path = Path(tmp) / (name + ".sh")
        path.write_text(source)
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
             "--format", "json", str(path)],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        if "raw" in report:
            report = report["raw"]
        traits = {t["id"]: t["crit"] for f in report["files"] for t in f.get("traits", [])}
        for trait, criticality in present.items():
            assert traits.get(trait) == criticality, (name, trait, traits.get(trait), result.stderr)
        for trait in absent:
            assert trait not in traits, (name, trait)
        print(name + ": PASS")
