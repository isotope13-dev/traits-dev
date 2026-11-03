#!/usr/bin/env python3
"""Check Swift request bindings, attempted cron use and triage claim limits."""

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
    request = '''import Foundation
var upload = URLRequest(url: endpoint)
upload.httpMethod = "POST"
upload.httpBody = payload
'''
    cron = '''import Foundation
let worker = Process()
worker.launchPath = "/usr/bin/crontab"
worker.arguments = ["-"]
let PERSIST_PATH = "/tmp/.agent"
let crontab = "\\(PERSIST_PATH) &\\n"
let inputPipe = Pipe()
worker.standardInput = inputPipe
try? worker.run()
inputPipe.fileHandleForWriting.write(crontab.data(using: .utf8)!)
'''
    zero = '''import Foundation
try? "".write(to: URL(fileURLWithPath: "/var/adm/wtmp"), atomically: true, encoding: .utf8)
'''
    fixtures = {
        "request.swift": request,
        "renamed.swift": request.replace("upload", "transmission"),
        "custom-object.swift": request.replace("URLRequest", "CustomObject"),
        "other-receiver.swift": request.replace("upload.http", "unrelated.http"),
        "comment.swift": "/*\n" + request + "\n*/\n",
        "cron.swift": cron,
        "renamed-cron.swift": cron.replace("worker", "launcher").replace("PERSIST_PATH", "destination").replace("inputPipe", "channel").replace("crontab =", "schedule =").replace("write(crontab.", "write(schedule."),
        "unused-cron.swift": cron.replace("worker.arguments", "other.arguments"),
        "zero.swift": zero,
        "nonempty.swift": zero.replace('"".write', '"new record".write'),
        "zero-comment.swift": "/*\n" + zero + "\n*/\n",
        "path-post.swift": request + 'let filename = "~/.ssh/authorized_keys"\n',
        "read-post.swift": request + 'let filename = "~/.ssh/authorized_keys"\nlet text = try? String(contentsOfFile: filename)\nlet route = "/collect"\n',
        "helper-names.swift": 'func attemptSSHPropagation() {}\nfunc attemptRPCPropagation() {}\n',
    }
    fixtures["exfil-label.swift"] = 'let label = "EXFIL:DATA"\n'
    fixtures["ssh-directory.swift"] = 'let directory = home + "/.ssh"\nlet entries = try? FileManager.default.contentsOfDirectory(atPath: directory)\n'
    tcp = """for octet in 1...254 {
    let connection = socket(AF_INET, SOCK_STREAM, 0)
    let result = connect(connection, destination, length)
}
"""
    fixtures["tcp-range.swift"] = tcp
    fixtures["tcp-half-open.swift"] = tcp.replace("1...254", "0..<255")
    fixtures["socket-pool.swift"] = tcp.replace("let result = connect(connection, destination, length)", "")
    fixtures["unrelated-connect.swift"] = tcp.replace("let result = connect(connection, destination, length)", "") + "let result = connect(fd, endpoint, count)\n"
    fixtures["delivery-clues.swift"] = tcp + '''let image = try Data(contentsOf: URL(fileURLWithPath: executable))
let command = "cat > /tmp/.agent && chmod +x /tmp/.agent"
for peer in candidates {
    sendCopy(destination: peer, image: image)
}
'''
    fixtures["profile-label.swift"] = 'let label = "EXFIL:DATA"\nlet profile = "HOSTNAME=x KERNEL=y ENV=z"\n'
    post = "micro-behaviors/communications/http/post::swift-urlrequest-post-method"
    body = "micro-behaviors/communications/http/request/body/construction::swift-urlrequest-http-body"
    config = "micro-behaviors/os/autorun/cron/modify::swift-crontab-stdin-configuration"
    ssh_list = "micro-behaviors/fs/directory/readdir/language::swift-ssh-directory-listing"
    erase = "objectives/evasion/indicator-removal/accounting::swift-login-accounting-zero-write"
    read_post = "micro-behaviors/fs/read/file/content/unspecified::swift-authorized-keys-read-post-clues"
    tcp_loop = "micro-behaviors/communications/socket/connect/attempt::swift-range-tcp-connect-loop"
    delivery = "objectives/lateral-movement/worm/network::swift-subnet-executable-delivery-attempt"
    profile_label = "objectives/exfiltration/stealer/system-info/profile::swift-socket-profile-exfil"
    required = {
        "request.swift": {post, body}, "renamed.swift": {post, body},
        "cron.swift": {config}, "renamed-cron.swift": {config},
        "zero.swift": {erase}, "read-post.swift": {read_post},
        "tcp-range.swift": {tcp_loop}, "tcp-half-open.swift": {tcp_loop},
        "ssh-directory.swift": {ssh_list},
        "delivery-clues.swift": {delivery}, "profile-label.swift": {profile_label},
    }
    forbidden = {
        "custom-object.swift": {post, body}, "other-receiver.swift": {post, body},
        "comment.swift": {post, body}, "unused-cron.swift": {config},
        "nonempty.swift": {erase}, "zero-comment.swift": {erase},
        "path-post.swift": {read_post},
        "socket-pool.swift": {tcp_loop}, "unrelated-connect.swift": {tcp_loop},
    }
    with tempfile.TemporaryDirectory(prefix="swift-improve-") as directory:
        work = Path(directory)
        for name, source in fixtures.items():
            (work / name).write_text(source)
        result = subprocess.run(
            [str(repo.parent / "cleave/target/release/cleave"), "--traits-dir", str(repo),
             "--format=json", str(work)], text=True, capture_output=True, check=True,
        )
        observed = {}
        for report in decode_reports(result.stdout):
            for file in report["files"]:
                observed[Path(file["path"]).name] = {t["id"]: t for t in file.get("traits", [])}
        for name, expected in required.items():
            assert expected <= observed[name].keys(), (name, expected - observed[name].keys())
        for name, excluded in forbidden.items():
            assert not excluded & observed[name].keys(), (name, excluded & observed[name].keys())
        for name in fixtures:
            ceiling = 5 if name in {"zero.swift", "delivery-clues.swift", "profile-label.swift"} else 4
            assert not any(t["crit"] >= ceiling for t in observed[name].values()), (name, observed[name])
    print(f"Swift improvement controls: {len(fixtures)} passed")


if __name__ == "__main__":
    main()
