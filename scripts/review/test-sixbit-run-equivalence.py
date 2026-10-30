# /// script
# dependencies = ["pyyaml"]
# ///
"""Verify the six-bit run optimization against its former fixed-width matcher."""
from pathlib import Path
import lzma
import random
import re
import yaml

root = Path(__file__).resolve().parents[2]
rule = yaml.safe_load((root / "metadata/binary/code/density/six-bit-byte-run.yaml").read_text())["traits"][0]["if"]
assert rule["type"] == "raw" and rule["section"] == "text"
minimum = rule["length_min"]
assert minimum == 4096
new = re.compile(rule["regex"].removeprefix("(?-u)").encode("ascii"))
old = re.compile(rb"[\x00-\x3f]{4096}")

def agrees(data):
    return bool(old.search(data)) == any(m.end() - m.start() >= minimum for m in new.finditer(data))

randomizer = random.Random(6)
for size in (0, 63, 64, 4095, 4096, 4097, 8192, 10000):
    for _ in range(12):
        data = bytearray(randomizer.randrange(256) for _ in range(size))
        run_length = randomizer.choice([0, min(size, 4095), min(size, 4096), size])
        start = randomizer.randrange(size - run_length + 1)
        data[start:start + run_length] = bytes(randomizer.randrange(64) for _ in range(run_length))
        assert agrees(data), (size, run_length, start)
assert agrees((b"\x01" * 64 + b"\xff") * 10001 + b"\x02" * 4096)
fixture = root / "testdata/hostile/generated/reduced/hostile/coa-npm-sdd-loader.dll.xz"
assert agrees(lzma.decompress(fixture.read_bytes()))
print("Six-bit run presence agrees on boundary, adversarial and PE fixture data")
