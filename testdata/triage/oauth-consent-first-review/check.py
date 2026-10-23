#!/usr/bin/env python3
"""Check consent observations and retain independent attack coverage."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OAUTH = "micro-behaviors/communications/http/oauth::"
REMOVED = "objectives/credential-access/cloud/token/oauth::"
env = dict(os.environ, CLEAVE_VALIDATE="0")
# Paths outside testdata prevent fixture/path suppressors from hiding a match.
scratch = os.environ.get("TRIAGE_SCRATCH")
with tempfile.TemporaryDirectory(prefix="consent-review-", dir=scratch) as tmp:
    for path in HERE.glob("*.js"):
        shutil.copyfile(path, Path(tmp) / path.name)
    for src, name in [
        ("testdata/hostile/reconfirm-phish-harvest.html", "reconfirm.html"),
        ("testdata/hostile/powershell-aes-xor-remcos.bin", "encrypted-remcos.bin"),
    ]:
        shutil.copyfile(ROOT / src, Path(tmp) / name)
    run = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--json", tmp], text=True, capture_output=True, env=env, check=True,
    )
    files = [f for line in run.stdout.splitlines()
             for f in json.loads(line)["files"]]
    reports = {Path(f["path"]).name: f for f in files}
    for name in ("placeholder-navigation.js", "gmail-client.js",
                 "certificate-name.js", "mixed-scopes.js"):
        traits = {t["id"]: t for t in reports[name]["traits"]}
        for observation in ("google-oauth-authorize-url", "google-gmail-scope-mail",
                            "oauth-offline-access-url", "oauth-consent-prompt-parameter"):
            assert traits[OAUTH + observation]["crit"] == 3, (name, observation)
        assert not any(t["crit"] >= 4 for t in traits.values()), name
        assert not any(t.startswith(REMOVED) for t in traits), name
    for name in ("identity-client.js", "identity-array.js", "mixed-scopes.js"):
        traits = {t["id"]: t for t in reports[name]["traits"]}
        scope_atom = ("openid-email-profile-scope-array" if name == "identity-array.js"
                      else "openid-email-profile-scope-string")
        assert traits[OAUTH + scope_atom]["crit"] == 3, name
        assert traits[OAUTH + "oauth-offline-access-url"]["crit"] == 3, name
        assert traits[OAUTH + "oauth-consent-prompt-parameter"]["crit"] == 3, name
    assert not any(t["id"] == OAUTH + "google-oauth-authorize-url"
                   for t in reports["name-only.js"]["traits"])
    phishing = {t["id"] for t in reports["reconfirm.html"]["traits"]
                if t["crit"] == 5}
    assert "objectives/credential-access/phishing/landing::reconfirm-prefilled-credential-harvest" in phishing
    payloads = [f for f in files if "encrypted-remcos.bin" in f["path"]]
    assert len(payloads) >= 3, "Decoded payloads must also be scanned"
    required = {
        "objectives/evasion/process/injection/hollowing/process::unmap-runpe-hollowing",
        "well-known/malware/rat/remcos::remcos-native-rat-agent",
        "well-known/malware/rat/remcos::remcos-browser-store-deletion",
    }
    native = [f for f in payloads if f["type"] == "pe" and any(
        t["id"] == "well-known/malware/rat/remcos::remcos-native-agent-banner"
        for t in f["traits"])]
    assert native, "Missing decrypted Remcos PE"
    for f in native:
        traits = {t["id"]: t for t in f["traits"]}
        assert required <= traits.keys()
        assert all(traits[t]["crit"] == 5 for t in required)
        assert traits["micro-behaviors/data/embedded/payload/resource::resource-command-process-io-profile"]["crit"] == 3

print("PASS: seven OAuth controls, phishing control, encrypted Remcos layers")
