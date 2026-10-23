#!/usr/bin/env python3
"""Check SSH context without executing any fixture's commands.

Copy controls outside testdata so testing-path suppressors cannot hide matches.
Usage: CLEAVE=/path/to/cleave python3 testdata/loki-inline-interpreter/check.py /scratch/path
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
remote = "micro-behaviors/process/create/eval::ssh-inline-interpreter-command"
remote_shell = "micro-behaviors/process/create/shell/command-string::ssh-inline-shell-network-or-base64-command"
perl = "micro-behaviors/process/create/eval::perl-inline-command"
propagation = "objectives/lateral-movement/ssh/propagation::sshpass-remote-interpreter-launch"
retired = "objectives/lateral-movement/ssh/propagation::ssh-launches-inline-payload"
results = []
for fixture in sorted(Path(__file__).parent.glob("*.sh")):
    target = scratch / fixture.name
    shutil.copyfile(fixture, target)
    output = subprocess.check_output(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
         "--format", "json", str(target)], text=True,
    )
    report = json.loads(output)
    traits = {t["id"]: t["crit"] for f in report["files"]
              for t in f.get("traits", [])}
    is_remote = fixture.name in ("ssh-python.sh", "ssh-perl.sh", "key-admin.sh")
    assert (remote in traits) == is_remote, fixture.name
    assert (remote_shell in traits) == (fixture.name == "ssh-bash.sh"), fixture.name
    assert (propagation in traits) == fixture.name.startswith("ssh-"), fixture.name
    assert retired not in traits, fixture.name
    if fixture.name in ("local-delay.sh", "separate-command.sh", "ssh-perl.sh"):
        assert traits.get(perl) == 3, fixture.name
    if fixture.name == "key-admin.sh":
        assert traits[remote] == 3, fixture.name
    results.append({"file": fixture.name, "traits": traits})
    print("PASS", fixture.name)
(scratch / "results.json").write_text(json.dumps(results, indent=2) + "\n")
