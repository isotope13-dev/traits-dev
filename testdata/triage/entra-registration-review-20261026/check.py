#!/usr/bin/env python3
"""Static regression controls; none of the specimens or fixtures is executed."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
PREFIX = "objectives/"
REPLAY = PREFIX + "credential-access/cloud/token/oauth::bulk-first-party-refresh-token-replay"
DRS = PREFIX + "credential-access/cloud/token/oauth::device-registration-refresh-token-redemption"
DEVICE = PREFIX + "persistence/login/oauth::replayed-token-device-registration"
MFA = PREFIX + "persistence/login/auth-method::replayed-token-authenticator-replacement"
REMOVAL = PREFIX + "evasion/security-bypass/auth::replayed-token-mfa-method-removal"
REPLACE = PREFIX + "persistence/login/auth-method::authentication-method-replacement-requests"


def controls(directory):
    py = (ROOT / "testdata/hostile/token-replay-mfa.py").read_text()
    js = (ROOT / "testdata/hostile/token-replay-spray.mjs").read_text()
    ps = (ROOT / "testdata/hostile/token-replay-spray.ps1").read_text()
    cases = []

    def add(name, content, yes=(), no=()):
        target = directory / name
        target.write_text(content)
        cases.append((target, set(yes), set(no)))

    add("mfa.py", py, [REPLAY, DRS, MFA, REPLACE, DEVICE, REMOVAL])
    add("spray.mjs", js, [REPLAY, DRS, DEVICE])
    add("mfa.ps1", ps, [REPLAY, DRS, MFA, REPLACE, DEVICE, REMOVAL])
    add("delete-only.py", py.replace(
        'requests.post(\n        "https://graph.microsoft.com/v1.0/me/authentication/microsoftAuthenticatorMethods"',
        'requests.get(\n        "https://graph.microsoft.com/v1.0/me/authentication/microsoftAuthenticatorMethods"'),
        [REPLAY, DRS, DEVICE, REMOVAL], [MFA, REPLACE])
    add("enrollment-get.py", py.replace(
        'requests.post(\n            f"https://enterpriseregistration.windows.net/',
        'requests.get(\n            f"https://enterpriseregistration.windows.net/'),
        [REPLAY, DRS, MFA], [DEVICE])
    add("graph-scope-only.py", py.replace(
        "01cb2876-7ebd-4aa4-9cc9-d28bd4d359a9/.default",
        "https://graph.microsoft.com/.default"), [REPLAY, MFA], [DRS, DEVICE])
    add("device-get.mjs", js.replace(
        "fetch('https://graph.microsoft.com/v1.0/devices', {\n      method: 'POST'",
        "fetch('https://graph.microsoft.com/v1.0/devices', {\n      method: 'GET'"),
        [REPLAY, DRS], [DEVICE])
    add("device-method-body-decoy.mjs", js.replace(
        "method: 'POST',\n      headers: { Authorization: `Bearer ${drs.access_token}`",
        "method: 'GET',\n      decoy: { method: 'POST' },\n      headers: { Authorization: `Bearer ${drs.access_token}`"),
        [REPLAY, DRS], [DEVICE])
    add("auth-get.ps1", ps.replace(
        "Invoke-RestMethod -Method POST -Uri 'https://graph.microsoft.com/v1.0/me/authentication/",
        "Invoke-RestMethod -Method GET -Uri 'https://graph.microsoft.com/v1.0/me/authentication/"),
        [REPLAY, DRS, DEVICE, REMOVAL], [MFA, REPLACE])
    add("device-get.ps1", ps.replace(
        'Invoke-RestMethod -Method POST -Uri "https://enterpriseregistration.windows.net/',
        'Invoke-RestMethod -Method GET -Uri "https://enterpriseregistration.windows.net/'),
        [REPLAY, DRS, MFA], [DEVICE])
    add("unrelated-delete.py", py.replace(
        'me/authentication/microsoftAuthenticatorMethods/{method',
        'devices/{method').replace(
        'me/authentication/phoneMethods/{method', 'devices/{method'),
        [REPLAY, DRS, DEVICE], [MFA, REPLACE, REMOVAL])
    add("ordinary-device-admin.py", '''import requests
requests.post("https://enterpriseregistration.windows.net/tenant/EnrollmentServer/device/", json={"DeviceDisplayName": "Managed device"})
''', (), [REPLAY, DRS, DEVICE, MFA, REPLACE, REMOVAL])
    add("ordinary-device-admin.mjs", '''await fetch('https://graph.microsoft.com/v1.0/devices', { method: 'POST', body: JSON.stringify({displayName: 'Managed device'}) });
''', (), [REPLAY, DRS, DEVICE, MFA, REPLACE, REMOVAL])
    add("quoted-requests.py", '''example = 'requests.post("https://graph.microsoft.com/v1.0/me/authentication/microsoftAuthenticatorMethods")'
''', (), [DEVICE, MFA, REPLACE])
    add("data-names.go", """package names
func example(data CustomData) {
    data.Set("language", "en")
    data.Encode()
}
""", ["metadata/lang/source/naming/function::go-data-set-symbol",
       "metadata/lang/source/naming/function::go-data-encode-symbol"],
       ["micro-behaviors/communications/http/post::url-values-form",
        "micro-behaviors/communications/http/post::url-values-encode"])
    add("quoted-data-names.go", 'package names; var example = "data.Set data.Encode"', (),
        ["metadata/lang/source/naming/function::go-data-set-symbol",
         "metadata/lang/source/naming/function::go-data-encode-symbol"])
    for method in ["PUT", "POST"]:
        add("body-" + method.lower() + ".java", """class Body {
void send(java.net.HttpURLConnection conn) throws Exception {
    conn.setRequestMethod("%s");
    conn.setDoOutput(true);
    conn.getOutputStream().write(new byte[]{1, 2});
}}
""" % method,
            ["metadata/lang/source/shape::jvm-do-output-configuration"] +
            (["micro-behaviors/communications/http/post::java-urlconnection-post-source"] if method == "POST" else []),
            ["micro-behaviors/communications/http/post::java-urlconnection-post-source"] if method == "PUT" else [])
    return cases


def scan(traits, paths):
    command = [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(traits), "--json", *map(str, paths)]
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    if result.stderr.strip():
        raise AssertionError(result.stderr)
    reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    return reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--traits-dir", type=Path, default=ROOT)
    parser.add_argument("--save", type=Path)
    parser.add_argument("--record-only", action="store_true")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="entra-controls-", dir=ROOT / "testdata/triage") as tmp:
        cases = controls(Path(tmp))
        reports = scan(args.traits_dir, [c[0] for c in cases])
        findings = {Path(f['path']).name: {t['id'] for t in f['traits']} for r in reports for f in r['files']}
        assertions = 0
        if not args.record_only:
            for path, yes, no in cases:
                actual = findings[path.name]
                assert not yes - actual, (path.name, "missing", yes - actual)
                assert not no & actual, (path.name, "unexpected", no & actual)
                assertions += len(yes) + len(no)
        if args.save:
            args.save.write_text(json.dumps({"assertions": assertions, "findings": {k: sorted(v) for k, v in findings.items()}}, indent=2))
        print(f"{len(cases)} controls; {assertions} assertions passed")


if __name__ == "__main__":
    main()
