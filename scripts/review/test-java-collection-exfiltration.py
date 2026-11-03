#!/usr/bin/env python3
"""Require transfer or sensitive-collection evidence beyond collection paths."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='java-collection-') as tmp:
    root = Path(tmp)
    cases = {
        'PathsOnly': 'static String a="/collect"; static String b="/api/v1/collect";',
        'Transfer': 'static String a="/collect"; static String b="collect?chunk=xURLEncoder.encode";',
        'CollectionWord': 'static String a="/collection"; static String b="collect?chunk=xURLEncoder.encode";',
    }
    for name, body in cases.items():
        (root / f'{name}.java').write_text(f'public class {name} {{ {body} }}\n')
    subprocess.run(['javac', *(str(root / f'{name}.java') for name in cases)], check=True, capture_output=True, text=True)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / f'{name}.class') for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).stem: {t['id'] for t in r.get('traits', [])} for r in reports}
    objective = 'objectives/exfiltration/http/upload::java-http-data-exfiltration'
    assert set(ids) == set(cases), ids.keys()
    assert objective not in ids['PathsOnly'], ids['PathsOnly']
    assert objective in ids['Transfer'], ids['Transfer']
    assert objective not in ids['CollectionWord'], ids['CollectionWord']
    print('Collection paths alone do not assert exfiltration; transfer evidence still does.')
