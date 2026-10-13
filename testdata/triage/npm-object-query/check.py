"""Static regression scans; none of the package code is executed."""
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
QUERY = "objectives/exfiltration/http/query::node-oob-object-profile-query-exfil"
HOOK = "objectives/supply-chain/recon-exfil/install-hook/recon::npm-install-oob-object-profile-query"
POC = "objectives/supply-chain/impersonation/depconf::npm-disclosed-depconf-host-profile-beacon"
DNS = "objectives/exfiltration/side-channel/dns::node-oob-hex-profile-http-dns-label"


def scan(path):
    result = subprocess.run(
        [CLEAVE, "--traits-dir", str(ROOT), "--format", "json", str(path)],
        capture_output=True, text=True, check=True,
        env={**os.environ, "CLEAVE_SKIP_CACHE": "1", "CLEAVE_NO_UPDATE_CHECK": "1"},
    )
    return json.loads(result.stdout)["files"][0]["traits"]


def pack(path, members):
    with tarfile.open(path, "w:gz") as output:
        for name, contents in members.items():
            data = contents.encode()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            output.addfile(info, io.BytesIO(data))


def check(path, required=(), forbidden=(), no_hostile=False):
    traits = scan(path)
    hostile = {t["id"] for t in traits if t["crit"] == 5}
    assert set(required) <= hostile, (path.name, "missing", set(required) - hostile)
    assert not set(forbidden) & hostile, (path.name, "unexpected", hostile)
    if no_hostile:
        assert not hostile, (path.name, hostile)
    print(path.name, len(hostile), "hostile findings", flush=True)


with tempfile.TemporaryDirectory(prefix="object-profile-controls-") as scratch:
    scratch = Path(scratch)
    with tarfile.open(HERE / "sample.tgz") as source:
        members = {m.name: source.extractfile(m).read().decode() for m in source if m.isfile()}
    original = scratch / "original.tgz"
    pack(original, members)
    check(original, (QUERY, HOOK, POC, DNS))

    renamed = dict(members)
    for name, text in renamed.items():
        text = text.replace("@myorder-frontend-commons/analytics", "@example/component")
        text = text.replace("poc.js", "worker.js")
        text = text.replace("db4jftohu4noreqdanngpnb3ger45ykrt.oast.fun", "fresh.oob.operator.net")
        for old, new in (("info", "profile"), ("qs", "encoded"), ("path", "route"),
                         ("beacon", "sendReport"), ("safe", "guarded"), ("os", "system")):
            # Preserve the format-defined request-options `path` property.
            text = re.sub(r"\b" + old + r"\b(?!\s*:)", new, text)
        text = text.replace("require('system')", "require('os')")
        renamed[name] = text
    renamed["package/worker.js"] = renamed.pop("package/poc.js")
    pack(scratch / "renamed.tgz", renamed)
    check(scratch / "renamed.tgz", (QUERY, HOOK, POC, DNS))

    stripped = {name: text for name, text in members.items() if name.endswith((".js", ".json"))}
    stripped["package/poc.js"] = re.sub(r"/\*[\s\S]*?\*/|//[^\n]*", "", stripped["package/poc.js"])
    manifest = json.loads(stripped["package/package.json"])
    manifest["description"] = "Component library"
    manifest.pop("keywords", None)
    stripped["package/package.json"] = json.dumps(manifest)
    pack(scratch / "no-disclosure.tgz", stripped)
    check(scratch / "no-disclosure.tgz", (QUERY, HOOK, DNS), (POC,))

    code = members["package/poc.js"]
    # A profile assembled for logging must not convict when another object is sent.
    unrelated = code.replace("var path = '/beacon/' + TOKEN + '?' + qs;",
        "var other = Object.keys({nonce: TOKEN}).map(function(k) { return k; }).join('&');\n"
        "var path = '/probe?' + other;")
    unrelated = unrelated.replace("beacon(label + '.' + OOB)", "beacon(OOB)")
    (scratch / "unrelated-query.js").write_text(unrelated)
    check(scratch / "unrelated-query.js", forbidden=(QUERY,), no_hostile=True)

    # No transfer: the profile remains in a local log.
    no_request = code.replace("http.get(", "logOnly(")
    (scratch / "no-request.js").write_text(no_request)
    check(scratch / "no-request.js", forbidden=(QUERY,), no_hostile=True)

    # Mapping keys instead of values does not transmit the host/user record.
    keys_only = code.replace("String(info[k])", "String(k)")
    keys_only = keys_only.replace("beacon(label + '.' + OOB)", "beacon(OOB)")
    (scratch / "keys-only.js").write_text(keys_only)
    check(scratch / "keys-only.js", forbidden=(QUERY,), no_hostile=True)

    # An unrelated OOB mention must not turn a first-party hostname into an attack.
    other_zone = code.replace("'db4jftohu4noreqdanngpnb3ger45ykrt.oast.fun'", "'api.vendor.net'")
    other_zone += "\n// OOB reference only: unrelated.oast.fun\n"
    (scratch / "unrelated-zone.js").write_text(other_zone)
    check(scratch / "unrelated-zone.js", forbidden=(QUERY, DNS), no_hostile=True)

    claim = scratch / "claim.js"
    claim.write_text("// Authorized dependency-confusion PoC research.\nmodule.exports = {};\n")
    assert not [t for t in scan(claim) if t["crit"] >= 4]
    print("claim.js: no suspicious or hostile findings", flush=True)

print("8 object-query regression controls passed")
