"""Static scans only: research prose must not suppress behavioral findings."""
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CLEAVE = os.environ.get("CLEAVE", "cleave")
HOST_RECON = "objectives/exfiltration/oob/callback::oob-service-http-host-recon"
POST_PROFILE = "objectives/supply-chain/recon-exfil/npm-install-targeting::js-sysinfo-oast-https-post-exfil"
INSTALL_PROFILE = "objectives/exfiltration/stealer/system-info/profile::npm-install-hook-host-profile-post-hardcoded-host"
ENV_THEFT = "objectives/exfiltration/stealer/env::node-host-profile-env-exfil"
GET_SURVEY = "objectives/discovery/system/profile::js-oob-get-hostname-cooccurrence"


def scan(path):
    result = subprocess.run(
        [CLEAVE, "--traits-dir", str(ROOT), "--format", "json", str(path)],
        capture_output=True, text=True, check=True,
        env={**os.environ, "CLEAVE_SKIP_CACHE": "1"},
    )
    return json.loads(result.stdout)["files"][0]


def archive(path, members):
    with tarfile.open(path, "w:gz") as output:
        for name, contents in members.items():
            data = contents.encode()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            output.addfile(info, io.BytesIO(data))


def findings(report, crit):
    return {t["id"] for t in report["traits"] if t["crit"] >= crit}


def check_beacon(path):
    report = scan(path)
    hostile = findings(report, 5)
    assert len(hostile) >= 3, (path.name, hostile)
    assert {HOST_RECON, POST_PROFILE, INSTALL_PROFILE} <= hostile, (path.name, hostile)
    assert ENV_THEFT not in findings(report, 0), path.name
    print(f"{path.name}: {len(hostile)} hostile traits")


with tempfile.TemporaryDirectory(prefix="depconf-controls-") as scratch:
    scratch = Path(scratch)
    with tarfile.open(HERE / "sample.tgz") as source:
        members = {m.name: source.extractfile(m).read().decode() for m in source if m.isfile()}
    original = scratch / "original.tgz"
    original.write_bytes((HERE / "sample.tgz").read_bytes())
    check_beacon(original)

    renamed = {name.replace("postinstall.js", "probe.js"): contents for name, contents in members.items()}
    for name in renamed:
        renamed[name] = renamed[name].replace("postinstall.js", "probe.js").replace("@coopeuch/button", "@example/component")
        renamed[name] = renamed[name].replace("s4yhii.com", "example.net")
        for old, new in (("npmContext", "registryDetails"), ("ciMarkers", "buildMarkers"), ("NPM_KEYS", "CONFIG_KEYS"), ("consumer", "parentProject")):
            renamed[name] = re.sub(r"\b" + old + r"\b", new, renamed[name])
    archive(scratch / "renamed.tgz", renamed)
    check_beacon(scratch / "renamed.tgz")

    stripped = {name: contents for name, contents in members.items() if name.endswith((".js", ".json"))}
    for name in stripped:
        if name.endswith(".js"):
            stripped[name] = re.sub(r"^\s*//.*$", "", stripped[name], flags=re.MULTILINE)
    manifest = json.loads(stripped["package/package.json"])
    manifest["description"] = "Component library"
    manifest.pop("contentPolicy", None)
    stripped["package/package.json"] = json.dumps(manifest)
    archive(scratch / "no-disclosure.tgz", stripped)
    check_beacon(scratch / "no-disclosure.tgz")

    # A claim without collection or transfer has no attack behavior to convict.
    claim = scratch / "claim.js"
    claim.write_text("// Authorized security PoC dependency-confusion research beacon.\nmodule.exports = {};\n")
    assert not findings(scan(claim), 4)
    print("claim.js: no suspicious or hostile traits")

    diagnostic = scratch / "local.js"
    diagnostic.write_text("const os = require('os');\nconsole.log({host: os.hostname(), interfaces: os.networkInterfaces()});\n")
    assert not findings(scan(diagnostic), 4)
    print("local.js: no suspicious or hostile traits")

    # GET plus host lookup is co-occurrence, without proven data transfer.
    survey = scratch / "survey.js"
    survey.write_text("// Authorized security PoC dependency-confusion research.\nconst os = require('os');\nconst https = require('https');\nconsole.log(os.hostname());\nhttps.get('https://canary.oob.example.net/probe', r => r.resume());\n")
    report = scan(survey)
    assert GET_SURVEY in findings(report, 4)
    assert not findings(report, 5)
    print("survey.js: suspicious survey remains visible despite research claim")

    prior = scratch / "disclosed.js"
    prior.write_bytes((ROOT / "testdata/triage/research-beacon-msdt-html/disclosed-beacon.js").read_bytes())
    assert {HOST_RECON, POST_PROFILE} <= findings(scan(prior), 5)
    print("disclosed.js: OOB host reporting remains hostile despite research claim")

print("7 regression controls passed")
