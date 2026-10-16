"""Scan copies outside test paths so production test exclusions cannot mask FPs.

Regression coverage for the unconvicted-hostile triage round:

- ``iex-ci-install-command.ps1``: a CI step re-executing a command string the
  repo's own earlier steps assembled (``$env:INSTALL_COMMAND`` from
  ``steps.*.outputs.command``) is automation, not an environment-staged
  payload, so ``invoke-expression-env-variable`` stays silent; the opaque
  control ``iex-opaque-env.ps1`` still fires it.
- ``popup-lockup-tight.js`` vs ``popup-api-scattered.js``: a moving-popup
  lockup drives open/move/focus/screen-reads from one tight timer loop. Legs
  scattered kilobytes apart across a wrapper library surface must not
  convict; legs inside one small loop still do.
- ``setresuid-spaced.c`` vs ``setresuid-unspaced.c``: the setresuid-root
  atom sees through normal C comma spacing either way.
- ``ransom-marker-tp.o`` vs ``interop-locked-fp.o``: ``photo.jpg.locked``
  is still a ransomware suffix marker, while a qualified Streams-API
  interop name (``Ns.streams.locked``, cf. ``ReadableStream.locked``) is a
  dotted code identifier, not a renamed victim file.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(root), CLEAVE_SKIP_CACHE='1', SCAN_NO_UPDATE='1')
with tempfile.TemporaryDirectory(prefix='unconvicted-hostile-triage-', dir=args.scratch) as neutral:
    for case in cases:
        source = root / case['path']
        rel = source.relative_to(Path(__file__).with_name('files'))
        target = Path(neutral) / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        # atomscan exits nonzero when it reports hostile/suspicious content,
        # which is exactly what the positive controls below assert, so a
        # finding exit status is success here; only an empty report is an
        # error.
        result = subprocess.run(['atomscan', '--format', 'json', str(target)],
                                env=env, capture_output=True, text=True, check=False)
        assert result.stdout.strip(), (case['path'], result.returncode, result.stderr[-500:])
        reports = [json.loads(line) for line in result.stdout.splitlines()]
        matched = {trait['id'] for report in reports for file in report['raw']['files']
                   for trait in file.get('traits', [])}
        missing = set(case['matched']) - matched
        unexpected = set(case['not_matched']) & matched
        assert not missing and not unexpected, (case['path'], missing, unexpected)
        print(f"PASS {case['path']}", flush=True)
