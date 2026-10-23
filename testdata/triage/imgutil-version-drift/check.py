"""Check neutral observations and retained credential behavior consumers."""
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
REGISTRY = "metadata/lang/source/naming/setting::registry-auth-config-text"
AUTHS = "metadata/lang/source/syntax/key-value::quoted-auths-field"
CAPTURE = "objectives/credential-access/capture/input::password-written-near-input"
DOCKER_READ = "objectives/credential-access/cloud/token/cli::docker-config-auth-marker"
ATTACK = "objectives/execution/autoinstall/credential-gate::credential-probes-gate-remote-package-runner"
OLD = {
    "objectives/credential-access/capture/input::registry-auth-password-login",
    "objectives/credential-access/cloud/token/cli::docker-config-auth-evidence--auths",
}
cases = {
    HERE / "registry-config.go": ({REGISTRY: 3}, set()),
    HERE / "registry-unauthorized.go": ({}, {REGISTRY}),
    HERE / "registry-login.go": ({REGISTRY: 3}, {CAPTURE}),
    HERE / "password-recording.go": ({CAPTURE: 4}, {REGISTRY}),
    HERE / "auths-field.js": ({AUTHS: 3}, {DOCKER_READ}),
    HERE / "auths-reference.js": ({}, {AUTHS, DOCKER_READ}),
    HERE / "docker-config-read.py": ({AUTHS: 3, DOCKER_READ: 3}, set()),
}
for name in ("credential-gated-runner.js", "renamed-credential-runner.js"):
    cases[ROOT / "testdata/taxonomy/vsix-triage-2026-10-20" / name] = ({ATTACK: 5}, set())

result = subprocess.run(
    ["cleave", "--traits-dir", str(ROOT), "--format", "json", "analyze", *map(str, cases)],
    check=True, capture_output=True, text=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout
seen = set()
while remaining.strip():
    document, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for entry in document["files"]:
        path = pathlib.Path(entry["path"])
        if path not in cases:
            continue
        findings = {trait["id"]: trait["crit"] for trait in entry["traits"]}
        required, forbidden = cases[path]
        assert not (OLD | forbidden) & findings.keys(), (path, findings)
        for trait, severity in required.items():
            assert findings.get(trait) == severity, (path, trait, findings.get(trait))
        seen.add(path)
assert seen == cases.keys(), (seen, cases.keys())
print(f"Passed {len(seen)} controls, including two existing hostile fixtures.")
