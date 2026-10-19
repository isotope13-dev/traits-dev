"""Check Graph SDK writes, credential reuse, and read/documentation boundaries."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent
RBAC = "micro-behaviors/os/security/auth/rbac::"
CLOUD = "micro-behaviors/os/security/auth/cloud::"
ROLE = RBAC + "entra-global-admin-role-grant"
WRITE = CLOUD + "graph-identity-credential-create"
CHAIN = RBAC + "entra-admin-grant-credential-login-references"
RETIRED = "objectives/persistence/login/oauth::entra-admin-grant-credential-reuse"
SDK_ROLE = RBAC + "graph-directory-role-sdk-call"
JS_ROLE = RBAC + "graph-directory-role-js-sdk-post"
SDK_APP = CLOUD + "graph-application-password-sdk-call"
SDK_PRINCIPAL = CLOUD + "graph-principal-password-sdk-call"
SDK_CSHARP = CLOUD + "graph-application-password-csharp-sdk-call"
JS_CRED = CLOUD + "graph-identity-credential-js-sdk-post"
CALLS = {SDK_ROLE, JS_ROLE, SDK_APP, SDK_PRINCIPAL, SDK_CSHARP, JS_CRED}

cases = {}
for ext, role, cred in (("py", SDK_ROLE, SDK_APP), ("cs", SDK_ROLE, SDK_CSHARP),
                        ("js", JS_ROLE, JS_CRED), ("ts", JS_ROLE, JS_CRED)):
    cases[f"graph-client.{ext}"] = ({ROLE, WRITE, CHAIN, role, cred}, set())
for ext in ("py", "cs", "js"):
    cases[f"read-only.{ext}"] = (set(), CALLS | {ROLE, WRITE, CHAIN})
    cases[f"source-documentation.{ext}"] = (set(), CALLS | {ROLE, WRITE, CHAIN})
    credential_call = {"py": SDK_APP, "cs": SDK_CSHARP, "js": JS_CRED}[ext]
    cases[f"reader-role.{ext}"] = ({credential_call}, {ROLE, CHAIN})
cases["principal-client.py"] = ({ROLE, WRITE, CHAIN, SDK_PRINCIPAL}, {SDK_APP})
cases["principal-read.py"] = (set(), CALLS | {ROLE, WRITE, CHAIN})
cases["unrelated-post.js"] = (set(), {JS_ROLE, JS_CRED, ROLE, WRITE, CHAIN})
cases["role-read-credential-write.js"] = ({JS_CRED}, {JS_ROLE, ROLE, CHAIN})
cases["role-write-credential-read.js"] = ({JS_ROLE, ROLE}, {JS_CRED, WRITE, CHAIN})
cases["log-code.cs"] = (set(), CALLS | {ROLE, WRITE, CHAIN})

result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else "cleave", "--traits-dir", ".", "--json",
     *[str(BASE / name) for name in cases]], cwd=ROOT, check=True,
    capture_output=True, text=True)
observed = {}
for line in result.stdout.splitlines():
    for file in json.loads(line)["files"]:
        observed[Path(file["path"]).name] = {t["id"] for t in file.get("traits", [])}
        assert not any(t["id"] == RETIRED for t in file.get("traits", [])), file["path"]
        for trait in file.get("traits", []):
            if trait["id"] == CHAIN:
                assert trait["crit"] == 3, file["path"]
for name, (required, forbidden) in cases.items():
    assert name in observed, f"No analysis for {name}"
    assert required <= observed[name], f"{name}: missing {required - observed[name]}"
    assert not forbidden & observed[name], f"{name}: unexpected {forbidden & observed[name]}"
print(f"PASS: {len(cases)} Graph SDK fixtures")
