#!/usr/bin/env python3
"""Archive compression-bomb must require whole-archive expansion.

`objectives/impact/dos/resource::archive-compression-bomb` convicts only
when a single member's peak expansion, the whole archive's overall
expansion, the member count, and the unpacked total all agree. A
gigabyte-scale framework whose most repetitive header compresses ~250x
but whose overall ratio is ~4x (tensorflow-cpu 2.16.1: 1.1 GiB unpacked,
10180 members, overall ratio 0.22) must not convict: the peak-ratio leg
alone describes one compressible member, not a bomb.

Run `python3 testdata/archive-bomb-overall-ratio/check.py <scratch-directory>`.
Fixtures are built outside testdata so file-path suppressors cannot mask
the findings under test.
"""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

BOMB = 'objectives/impact/dos/resource::archive-compression-bomb'
OVERALL = 'metadata/file/archive::archive-high-overall-compression-expansion'
PEAK = 'metadata/file/archive::archive-high-compression-expansion'


def build(path: Path, members: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for name, data in members.items():
            zf.writestr(name, data)


def scan(root: Path, target: Path) -> set[str]:
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    seen = set()
    report = json.loads(result.stdout)
    files = report.get('files', report if isinstance(report, list) else [])
    for entry in files:
        for trait in entry.get('traits', []):
            seen.add(trait['id'])
    return seen


def main() -> None:
    scratch = Path(sys.argv[1])
    scratch.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[2]

    # Highly compressible content: overall expansion far above 20x.
    dense = scratch / 'dense.zip'
    build(dense, {'repetitive.bin': b'A' * 300_000})
    seen = scan(root, dense)
    assert OVERALL in seen, sorted(seen)
    assert PEAK in seen, sorted(seen)
    assert BOMB not in seen, sorted(seen)
    print('dense.zip: overall-ratio fires, bomb stays quiet (too small): passed')

    # Incompressible content: overall expansion near 1x.
    import random
    rng = random.Random(1234)
    blob = bytes(rng.randrange(256) for _ in range(300_000))
    sparse = scratch / 'sparse.zip'
    build(sparse, {'random.bin': blob})
    seen = scan(root, sparse)
    assert OVERALL not in seen, sorted(seen)
    assert BOMB not in seen, sorted(seen)
    print('sparse.zip: overall-ratio absent, bomb absent: passed')


if __name__ == '__main__':
    main()
