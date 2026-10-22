"""Scan fixture bytes as data, away from test-path suppressors; never run them."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--scratch", required=True)
args = parser.parse_args()
here = Path(__file__).resolve().parent
root = here.parents[2]
env_upload = "objectives/exfiltration/stealer/env::node-filtered-env-curl-stdin"
cron = "objectives/persistence/system/cron/job::node-credential-sweep-remote-shell-cron"
cron_entry = "micro-behaviors/os/autorun/cron::cron-curl-shell-entry"
concat = "micro-behaviors/data/string/concat::js-os-identity-concat"
array = "metadata/lang/source/literal::egress-command-array-head"
identity = "objectives/supply-chain/recon-exfil/dns::js-https-identity-subdomain-beacon"
retired = {
    "micro-behaviors/data/string/concat::js-os-identity-label-concat",
    "micro-behaviors/process/create/permission-agent::egress-operation-deny-list",
}
with tempfile.TemporaryDirectory(prefix="acquit-controls-", dir=args.scratch) as temp:
    paths = []
    for source in [*here.glob("*.js"), *here.glob("*.py")]:
        if source.name == "check.py":
            continue
        dest = Path(temp) / source.name
        shutil.copyfile(source, dest)
        paths.append(dest)
    for source in [
        root / "testdata/benign/node-cron-healthcheck.js",
        root / "testdata/hostile/js-host-dns-beacon-controls.js",
        root / "testdata/hostile/dns-identity-label-egress.zip",
        root / "testdata/depconf-import-beacon/identity-beacon.tgz",
    ]:
        dest = Path(temp) / source.name
        shutil.copyfile(source, dest)
        paths.append(dest)
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
         "--format", "json", *map(str, paths)],
        check=True, capture_output=True, text=True,
    )
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    files = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for file in report["files"]:
            files[Path(file["path"]).name] = {
                trait["id"]: trait["crit"] for trait in file.get("traits", [])
            }
    assert all(not retired.intersection(traits) for traits in files.values())
    assert files["collector.js"][env_upload] == 4
    assert files["collector.js"][cron] == 5
    for name in ["other-upload-buffer.js", "different-env-key.js", "nonsecret-env-filter.js"]:
        assert env_upload not in files[name], name
    assert files["report-only.js"][concat] == 3
    assert identity not in files["report-only.js"]
    assert files["https-identity.js"][identity] == 4
    assert files["ssh-argv.py"][array] == 3
    assert files["permission-list.py"][array] == 3
    for name in ["cron-one-space.py", "cron-two-spaces.py", "cron-reboot.py"]:
        assert files[name][cron_entry] == 3, name
    assert cron not in files["node-cron-healthcheck.js"]
    assert env_upload not in files["node-cron-healthcheck.js"]
    assert files["js-host-dns-beacon-controls.js"]["objectives/exfiltration/dns/lookup::js-host-identity-dns-beacon"] == 5
    assert files["dns-identity-label-egress.zip"]["objectives/exfiltration/dns/lookup::python-identity-label-dns-beacon"] == 5
    assert files["identity-beacon.tgz"]["objectives/exfiltration/http/query::node-env-hex-identity-query-exfil"] == 5
print("PASS: bound environment upload, cron registration, source claims, retained archive/DNS coverage")
