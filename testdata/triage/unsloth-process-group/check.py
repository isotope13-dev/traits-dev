"""Check group-termination placement without test-path suppression.

Only static analysis is performed. Pass --scratch outside testdata.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--scratch", type=Path, required=True)
args = parser.parse_args()
here = Path(__file__).resolve().parent
root = here.parents[2]
old = "objectives/persistence/system/init/script::process-group-kill"
new = "micro-behaviors/process/terminate/command::process-group-kill"
init = "objectives/persistence/system/init/script::"
consumers = {init + name for name in (
    "init-process-group-killer", "init-process-hunter", "init-aggressive-process-control"
)}
cases = [
    (here / "supervisor.sh", True, False),
    (here / "init-hunter.sh", True, True),
    (here / "single-pid.sh", False, False),
    (here / "probe-group.sh", False, False),
    (root / "testdata/taxonomy/unconvicted-hostile-triage/files/group-kill-untracked.sh", True, False),
    (root / "testdata/taxonomy/unconvicted-hostile-triage/files/jest-worker-cleanup.zip", False, False),
]
env = dict(os.environ, CLEAVE_VALIDATE="0", CLEAVE_TRAITS_DIR=str(root))
with tempfile.TemporaryDirectory(prefix="group-termination-", dir=args.scratch) as folder:
    for source, expected, hunting in cases:
        target = Path(folder) / source.name
        shutil.copyfile(source, target)
        run = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
             "--format", "json", str(target)],
            env=env, capture_output=True, text=True, check=True,
        )
        report = json.loads(run.stdout)
        traits = {t["id"]: t for f in report["files"] for t in f.get("traits", [])}
        assert old not in traits, source
        assert (new in traits) == expected, source
        if expected:
            assert traits[new]["crit"] == 3, source
            assert "atk" not in traits[new], source
        if hunting:
            assert consumers <= traits.keys(), source
            assert traits[init + "init-process-hunter"]["crit"] == 5, source
            assert traits[init + "init-aggressive-process-control"]["crit"] == 5, source
        else:
            assert not consumers & traits.keys(), source
        print("PASS", source.name, flush=True)
