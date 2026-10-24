#!/usr/bin/env python3
"""Static matcher controls; fixture commands are never executed."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
parser.add_argument("--work-dir", required=True)
a = parser.parse_args()
here = Path(__file__).resolve().parent
root = here.parent.parent
prefix = "micro-behaviors/communications/http/download/curl::"
relative = prefix + "curl-relative-dotfile-output"
hidden = prefix + "shell-curl-hidden-output"
output = prefix + "curl-output-file"
raw_ip = "objectives/evasion/file-hiding/dotfile-create::raw-ip-hidden-background-download"
execute = "objectives/execution/payload/file-exec::shell-hidden-temp-download-execute"
config_cases = {
    "goreleaser-yaml.sh", "goreleaser-yml.sh", "golangci-yml.sh",
    "golangci-yaml.sh", "quoted-config.sh", "config-url-visible-output.sh",
    "releaser.yml", "gochecks.yml",
}
positive_cases = {
    "goreleaser-suffix.sh": {relative, hidden},
    "golangci-suffix.sh": {relative, hidden},
    "mixed.sh": {relative, hidden},
    "config-url-hidden-output.sh": {relative, hidden},
    "hidden-temp-config.sh": {hidden, execute},
    "raw-ip-background.sh": {relative, raw_ip},
}
# Scan copies outside testdata: test-directory suppressors otherwise prevent
# the raw-IP consumer from firing and would make its preservation check inert.
with tempfile.TemporaryDirectory(prefix="fortio-controls-", dir=a.work_dir) as work:
    work = Path(work)
    for name in config_cases | set(positive_cases):
        shutil.copyfile(here / name, work / name)
    result = subprocess.run(
        [a.cleave, "--traits-dir", str(root), "analyze", "--format", "json", str(work)],
        env=dict(os.environ, CLEAVE_SKIP_CACHE="1"),
        capture_output=True, text=True, check=True,
    )
    remaining = result.stdout.strip()
    reports = {}
    while remaining:
        report, end = json.JSONDecoder().raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for file in report["files"]:
            name = Path(file["path"].split("!!")[0]).name
            reports.setdefault(name, {}).update({t["id"]: t["crit"] for t in file.get("traits", [])})
    assert len(reports) == len(config_cases) + len(positive_cases), reports.keys()
    for name in config_cases:
        traits = reports[name]
        assert not ({relative, hidden} & set(traits)), (name, traits)
        assert not any(c >= 4 for c in traits.values()), (name, traits)
        # gochecks' conditional run block is currently marked incomplete by
        # the engine; the enclosing workflow still retains the HTTP fact.
        download = "micro-behaviors/communications/http/curl::workflow-curl-http-request" if name == "gochecks.yml" else output
        assert traits.get(download) == 3, (name, download, traits)
    for name, required in positive_cases.items():
        assert required <= set(reports[name]), (name, required - set(reports[name]))
        assert all(reports[name][trait] >= 4 for trait in required), (name, reports[name])
    print(str(len(reports)) + " config/output and retained-consumer controls passed")
