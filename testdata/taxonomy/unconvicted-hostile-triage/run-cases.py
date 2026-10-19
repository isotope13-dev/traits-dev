"""Scan copies outside test paths so production test exclusions cannot mask FPs.

Regression coverage for the unconvicted-hostile triage round:

- ``iex-ci-install-command.ps1``: a CI step re-executing a command string the
  repo's own earlier steps assembled (``$env:INSTALL_COMMAND`` from
  ``steps.*.outputs.command``) is automation, not an environment-staged
  payload, so ``invoke-expression-env-variable`` stays silent; the opaque
  control ``iex-opaque-env.ps1`` still fires it.
- ``popup-lockup-tight.js`` vs ``popup-api-scattered.js``: the tight fixture
  attempts random movement and repeated focus within a 100 ms interval.
  These are suspicious
  UI interference, not proof of popup lockup or resource exhaustion.
  Scattered API references do not establish either callback relationship.
- ``setresuid-spaced.c`` vs ``setresuid-unspaced.c``: the setresuid-root
  atom sees through normal C comma spacing either way, while a lone call
  no longer self-corroborates into ``native-setresuid-escalation``; the
  ``setresuid-pair.c`` control (root user-id request beside a group-side
  setter) still convicts it.
- ``ransom-marker-tp.o`` vs ``interop-locked-fp.o``: ``photo.jpg.locked``
  is still a ransomware suffix marker, while a qualified Streams-API
  interop name (``Ns.streams.locked``, cf. ``ReadableStream.locked``) is a
  dotted code identifier, not a renamed victim file.
- ``store-execute-cmd.js`` vs ``c2-exec-postback.js``: a vetted data-store
  write through ``execute(r.cmd)`` is the command pattern, not remote
  tasking; neither fixture establishes received tasking or output-to-request
  flow, so neither convicts.
- ``rust-fetch-noexec/build.rs`` vs ``rust-fetch-spawn/build.rs``: an HTTP
  fetch beside a ``python -c`` discovery query (``.output()``) is not
  fetch-and-run; a fetch beside a ``.spawn()`` launch does not by itself
  establish abuse.
- ``jest-worker-cleanup.zip`` vs ``group-kill-untracked.sh``: an e2e
  harness killing its pidfile-tracked worker group is cleanup (the zip
  exercises the archive-member path, where shell-gated atoms evaluate);
  an untracked ``kill -9 -${var}`` still fires.
- ``mcp-updater-detached.js`` vs ``mcp-backdoor-detached.js``: neither
  obfuscated token configuration nor detached execution establishes a
  backdoor or staged payload. The latter fixture actually throws before
  reaching its imports; neutral source capabilities remain visible.
- ``consent-env-upload.py`` vs ``steal-env-upload.py``: a CLI that refuses
  to run unless the operator exports credential env vars is delegated
  consent; a silent env-secret POST without it still convicts.
- ``system-cleanup.sh`` vs ``random-maintenance.sh``: log truncation
  beside package-cache cleaning is system maintenance, not
  anti-forensics; the same truncation without maintenance context still
  reads as indicator removal.
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
