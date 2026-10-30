import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import time

WORK = Path('/tmp/png-good-triage')
parser = argparse.ArgumentParser()
parser.add_argument('--images-dir', type=Path, default=Path('/home/t/src/traits-dev/.triage-work/png-good/pngs'))
parser.add_argument('--output', type=Path, default=WORK / 'contained-native-values.jsonl')
args = parser.parse_args()
images = sorted(args.images_dir.glob('*.png'))
completed = set()
dest = args.output
if dest.exists():
    with dest.open() as f:
        completed = {json.loads(line)['sha256'] for line in f if line.strip()}
images = [p for p in images if p.stem not in completed]
groups = [images[i:i + 64] for i in range(0, len(images), 64)]
env = {**os.environ, 'RAYON_NUM_THREADS': '2'}
start = time.monotonic()

def probe(group):
    result = subprocess.run(['/home/t/src/cleave/target/debug/cleave', 'facts', 'values', *map(str, group)],
                            capture_output=True, text=True, env=env, timeout=600)
    if result.returncode:
        raise RuntimeError(result.stderr[-2000:])
    rows = [json.loads(line) for line in result.stdout.split('\n') if line.strip()]
    assert len(rows) == len(group), (len(rows), len(group))
    return [{'sha256': row['file']['stem'], 'values': row} for row in rows]

with dest.open('a') as out, concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for index, rows in enumerate(pool.map(probe, groups), 1):
        for row in rows:
            out.write(json.dumps(row) + '\n')
        out.flush()
        print(index, '/', len(groups), 'elapsed', round(time.monotonic() - start, 1), flush=True)
print('COMPLETE', len(images), 'new unique PNGs;', len(completed) + len(images), 'total', flush=True)
