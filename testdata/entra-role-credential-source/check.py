"""Check Graph role/credential detection across source languages and near misses."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
ROLE = "micro-behaviors/os/security/auth/rbac::entra-global-admin-role-grant"
CHAIN = "objectives/persistence/login/oauth::entra-privileged-role-credential-add"
POST = "micro-behaviors/os/security/auth/rbac::graph-directory-role-post-call"
ROLE_ID = "micro-behaviors/os/security/auth/rbac::entra-global-admin-role-id"

cases = {}
for name in ("role-and-secrets.go", "role-and-secrets.cs", "service-principal-secrets.cs"):
    cases[f"testdata/entra-role-credential-source/{name}"] = ({ROLE, CHAIN, POST}, set())
for extension in ("py", "js", "ps1"):
    cases[f"testdata/hostile/entra-role-and-secrets.{extension}"] = ({ROLE, CHAIN}, set())
for name in (
    "entra-role-read-and-rotation.cs", "entra-role-source-documentation.cs",
    "entra-role-read-and-secret-rotation.py", "entra-role-documentation.py",
    "entra-role-revoke-and-rotation.ps1",
):
    cases[f"testdata/benign/{name}"] = (set(), {ROLE, CHAIN, POST})
for extension in ("cs", "js"):
    cases[f"testdata/benign/entra-reader-role-and-rotation.{extension}"] = ({POST}, {ROLE, CHAIN})
cases["testdata/benign/entra-global-admin-without-credential.cs"] = ({ROLE, POST}, {CHAIN})

result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else "cleave", "--traits-dir", ".", "--json", *cases],
    cwd=ROOT, check=True, capture_output=True, text=True,
)
observed = {}
for line in result.stdout.splitlines():
    for file in json.loads(line)["files"]:
        observed[file["path"]] = {trait["id"] for trait in file.get("traits", [])}
for path, (required, forbidden) in cases.items():
    assert path in observed, f"No analysis for {path}"
    assert required <= observed[path], f"{path}: missing {required - observed[path]}"
    assert not forbidden & observed[path], f"{path}: unexpected {forbidden & observed[path]}"
# The read-and-rotate near miss deliberately retains the role-ID signal.
assert ROLE_ID in observed["testdata/benign/entra-role-read-and-rotation.cs"]
print(f"PASS: {len(cases)} Graph role/credential source and control fixtures")
