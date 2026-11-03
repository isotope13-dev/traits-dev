#!/usr/bin/env python3
"""Exercise tar review descriptions and newly observed capabilities offline."""

import argparse
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile


CRON = "micro-behaviors/os/autorun/cron/entry::cron-scheduled-command-literal"
MODE = "micro-behaviors/fs/write/file/mode::node-write-owner-only-mode"
LOOKUP = "micro-behaviors/os/container/query::ruby-docker-container-lookup"
CREATE = "micro-behaviors/os/container/create::ruby-docker-container-create"
BUILD = "micro-behaviors/os/container/image::ruby-docker-image-build"
IMAGE = "micro-behaviors/os/container/image::ruby-docker-image-create"
WINDOWS = "metadata/archive/member/extension::archive-windows-script-entry"
JAVASCRIPT = "metadata/archive/member/extension::archive-js-member"
HOOK = "metadata/package/files/included::npm-root-install-script-member"
STORAGE = "metadata/lang/source/naming/function/storage::js-token-config-storage-helper-call"
PASTE = "micro-behaviors/ui/terminal::terminal-paste-instruction-language"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    cleave = str((root / args.cleave).resolve())
    fixtures = {
        "banner.js": 'console.error("* * * * * * PACKAGE DEPRECATED * * * * * *");\n',
        "stars.js": 'console.error("* * * * * * * * * * *");\n',
        "cron.js": 'const job = "*/5 * * * * /usr/bin/cleanup --quiet";\n',
        "cron-wildcard.js": 'const job = "0 2 * * * *.sh";\n',
        "schedule.js": 'const fields = "*/5 * * * *";\n',
        "storage.js": 'writeConfig({appUrl: "https://app.example"});\n',
        "private.js": 'writeFile(file, JSON.stringify(config), {mode: 0o600});\n',
        "private.ts": 'const data: string = "configuration";\nfs.writeFileSync(file, data, {mode: 0o600});\n',
        "decimal.js": 'fs.writeFile(file, data, {"mode": 384});\n',
        "hex.js": 'fs.writeFileSync(file, data, {mode: 0x180});\n',
        "public.js": 'writeFile(file, data, {mode: 0o644});\n',
        "nested-mode.js": 'writeFile(file, data, {permissions: {mode: 0o600}});\n',
        "payload-mode.js": 'writeFile(file, "mode: 0o600", {});\n',
        "comment-mode.js": '// writeFile(file, data, {mode: 0o600});\n',
        "quoted-mode.js": 'const example = "writeFile(file, data, {mode: 0o600})";\n',
        "paste.md": "Create an application token and paste it into the terminal.\n",
        "docker.rb": '''
require "docker"
container = ::Docker::Container.create(config)
::Docker::Container.get(name)
Docker::Container.all
Docker::Container.exist?(name)
Docker::Image.build(dockerfile)
Docker::Image.create({"fromImage" => image})
''',
        "docker-block.rb": '''
with_retries { @container = ::Docker::Container.create(config) }
with_retries { @runner = ::Docker::Container.get(name) }
''',
        "docker-comment.rb": '# Docker::Container.create(config)\n# Docker::Image.build(text)\n',
        "docker-quoted.rb": 'puts "Docker::Container.create(config)"\nputs "Docker::Image.build(text)"\n',
        "docker-lookalike.rb": 'Other::Container.create(config)\nDocker::Container.getter(name)\nDocker::Image.builder(data)\n',
    }
    required = {
        "cron.js": {CRON}, "cron-wildcard.js": {CRON},
        "schedule.js": {"micro-behaviors/os/autorun/cron/entry::cron-schedule-fields-literal"},
        "storage.js": {STORAGE}, "paste.md": {PASTE},
        **{name: {MODE} for name in ("private.js", "private.ts", "decimal.js", "hex.js")},
        "docker.rb": {LOOKUP, CREATE, BUILD, IMAGE},
        "docker-block.rb": {LOOKUP, CREATE},
        "javascript.tgz": {JAVASCRIPT},
        "windows.tgz": {WINDOWS},
        "hook.tgz": {HOOK, JAVASCRIPT},
    }
    forbidden = {
        **{name: {CRON} for name in ("banner.js", "stars.js", "schedule.js")},
        **{name: {MODE} for name in ("public.js", "nested-mode.js", "payload-mode.js", "comment-mode.js", "quoted-mode.js")},
        **{name: {LOOKUP, CREATE, BUILD, IMAGE} for name in ("docker-comment.rb", "docker-quoted.rb", "docker-lookalike.rb")},
        "javascript.tgz": {WINDOWS}, "hook.tgz": {WINDOWS},
    }
    with tempfile.TemporaryDirectory(prefix="tar-improve-controls-") as tmp:
        work = Path(tmp)
        for name, source in fixtures.items():
            (work / name).write_text(source)
        for name, members in {
            "javascript.tgz": {"main.js": "console.log('ready');\n"},
            "windows.tgz": {"script.vbs": 'WScript.Echo "ready"\n'},
            "hook.tgz": {"package/package.json": '{"name":"retired","version":"1.0.0"}',
                         "package/postinstall.js": fixtures["banner.js"]},
        }.items():
            with tarfile.open(work / name, "w:gz") as archive:
                for member, source in members.items():
                    data = source.encode()
                    entry = tarfile.TarInfo(member)
                    entry.size = len(data)
                    archive.addfile(entry, io.BytesIO(data))
        result = subprocess.run(
            [cleave, "--traits-dir", str(root), "--all-files", "--format", "json", str(work)],
            text=True, capture_output=True, check=True,
        )
        files = {Path(f["path"]).name: f for line in result.stdout.split("\n") if line
                 for f in json.loads(line)["files"]}
        obsolete = {
            "micro-behaviors/communications/http/device-code::js-store-token-call",
            "micro-behaviors/ui/terminal::macos-paste-terminal-cue",
            "metadata/package/files/included::npm-archive-root-companion-loader-member",
        }
        names = [*fixtures, "javascript.tgz", "windows.tgz", "hook.tgz"]
        for name in names:
            traits = files[name].get("traits", [])
            ids = {t["id"] for t in traits}
            assert not (required.get(name, set()) - ids), (name, "missing", required[name] - ids)
            assert not (forbidden.get(name, set()) & ids), (name, "unexpected", forbidden.get(name, set()) & ids)
            assert not (obsolete & ids), (name, "obsolete", obsolete & ids)
            assert not [t for t in traits if t["crit"] >= 4], (name, "unexpected severe finding")
            print(f"PASS {name}")
        print(f"{len(names)} tar improvement controls passed")


if __name__ == "__main__":
    main()
