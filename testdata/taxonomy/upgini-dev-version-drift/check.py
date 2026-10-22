"""Check retained observations, branch context, and placement boundaries."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROFILE = "micro-behaviors/os/sysinfo/profile::"
CALLBACK = "metadata/lang/source/syntax/member::visitor-id-arrow-callback"
QUERY = "micro-behaviors/communications/http/post::kaggle-api-key-secret-request-context"
BODY = "micro-behaviors/communications/http/request/body::swift-urlrequest-http-body"
POST = "micro-behaviors/communications/http/post::swift-urlrequest-post-method"
RECORD = "micro-behaviors/data/serialize/schema-credential::js-quoted-identity-password-fields"


def scan(path):
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", str(path)], capture_output=True, text=True, check=True,
    )
    return [t for f in json.loads(result.stdout)["files"] for t in f.get("traits", [])]


with tempfile.TemporaryDirectory(prefix="notebook-identity-controls-") as tmp:
    tmp = Path(tmp)
    archive = tmp / "renamed.zip"
    with zipfile.ZipFile(archive, "w") as out:
        out.write(HERE / "notebook-context.py", "lib/identity.py")
        out.write(HERE.parent / "upgini-version-drift/tracking.py", "lib/transport.py")
    cases = [
        (HERE / "notebook-context.py", [CALLBACK, QUERY,
            PROFILE + "notebook-browser-fingerprint-ip-context",
            PROFILE + "notebook-browser-host-identity-context",
            PROFILE + "notebook-fingerprint-secret-error-identity-context",
            "micro-behaviors/os/sysinfo/network::python-sha256-node-id"], []),
        (archive, ["micro-behaviors/communications/http/telemetry::kaggle-secret-query-tracking-json-context"], []),
    ]
    for name, source, required, absent in [
        ("callback.py", 'code = "result => result.visitorId"\n', [CALLBACK], [QUERY]),
        ("secret-client.py", '''from requests import post
url = "https://www.kaggle.com/requests/GetUserSecretByLabelRequest"
response = post(url, json={"Label": "api-key"})
secret = response.json()["result"]["secret"]
''', [QUERY], [PROFILE + "notebook-fingerprint-secret-error-identity-context"]),
        ("body.swift", 'request.httpMethod = "PUT"\nrequest.httpBody = data\n', [BODY], [POST]),
        ("post.swift", 'request.httpMethod = "POST"\nrequest.httpBody = data\n', [BODY, POST], []),
        ("record.js", 'const record = {"email": user, "password": password};\n', [RECORD], []),
        ("record-near.js", 'const record = {"email": user, "displayName": name};\n', [], [RECORD]),
    ]:
        path = tmp / name
        path.write_text(source)
        cases.append((path, required, absent))
    for path, required, absent in cases:
        traits = scan(path)
        ids = {t["id"] for t in traits}
        assert set(required) <= ids, (path, "missing", set(required) - ids)
        assert not set(absent) & ids, (path, "unexpected", set(absent) & ids)
        assert not any(t["crit"] == 5 for t in traits), (path, "unsupported hostile finding")
        print(path.name, "passed", flush=True)
print(f"{len(cases)} development-release controls passed")
