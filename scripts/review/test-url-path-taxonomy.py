#!/usr/bin/env python3
"""Check generic path traits and their matching boundaries after migration."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='url-path-taxonomy-') as tmp:
    root = Path(tmp)
    cases = {
        'positive.js': 'const a = "/FileUpload"; const b = "/messages?limit=20"; const c = "/video/:/transcode/universal";\n',
        'negative.js': 'const a = "/FileUploader"; const b = "/messages?limit=x"; const c = "/video/:/transcode/other";\n',
    }
    for name, source in cases.items():
        (root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    expected = {
        'micro-behaviors/communications/url/resource-path/file::file-upload-path-reference',
        'micro-behaviors/communications/url/query/selection::messages-limit-query-path',
        'micro-behaviors/communications/url/http-path/route::universal-transcode-route',
    }
    assert set(ids) == set(cases), ids.keys()
    assert expected <= ids['positive.js'], expected - ids['positive.js']
    assert not expected & ids['negative.js'], expected & ids['negative.js']
    print('Generic URL paths match with their original boundaries.')
