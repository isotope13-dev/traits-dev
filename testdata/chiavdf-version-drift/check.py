#!/usr/bin/env python3
"""Check token prose, authenticated git, and retained upload/download coverage."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
syntax = "metadata/lang/source/syntax/call::github-token-fetch-shaped-text"
fetch = "micro-behaviors/communications/http/client/library::fetch-cmd"
nginx = "micro-behaviors/communications/http/auth::nginx-basic-auth-directive"
basic = "micro-behaviors/communications/http/auth::authorization-basic-header-token"
upload = "objectives/supply-chain/recon-exfil/secrets::fetch-github-token"
exfil = "objectives/supply-chain/recon-exfil/secrets::github-token-exfil"
cases = {
    "checkout.sh": ({basic}, {fetch, nginx, upload, exfil}),
    "downloader.sh": ({fetch}, {nginx}),
    "nginx.sh": ({nginx}, {fetch}),
    "documented-fetch.yml": ({syntax}, {upload, exfil}),
    "token-fetch-auth.yml": ({syntax}, {upload, exfil}),
    # The transparent github-token-exfil wrapper can be filtered from reports;
    # its concrete upload finding must remain visible.
    "token-fetch.yml": ({syntax, upload}, set()),
}
for name, (required, forbidden) in cases.items():
    # Composite manifests require the platform-mandated action.yml basename.
    target = (scratch / "documented-fetch" / "action.yml"
              if name == "documented-fetch.yml" else scratch / name)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__).parent / name, target)
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
         "--format", "json", str(target)],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(result.stdout)
    found = {t["id"] for f in report["files"] for t in f.get("traits", [])}
    assert required <= found, (name, "missing", required - found)
    assert not forbidden & found, (name, "unexpected", forbidden & found)
    print(name + ": passed")
