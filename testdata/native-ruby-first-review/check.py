"""Static regression checks; never execute the Ruby or PE fixtures."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FD = "micro-behaviors/process/fd/stdio::"
SHELL = "objectives/command-and-control/reverse-shell/fd-redirect::ruby-reopened-stdio-shell"
SHUTDOWN = "objectives/impact/system/shutdown::packet-flood-privileged-shutdown"
MOVES = {
    "objectives/anti-static/obfuscation/payload/encrypted::packed-winhttp-memory-loader":
        "micro-behaviors/communications/http/client/winhttp::winhttp-resource-protection-api-set",
    "objectives/anti-static/obfuscation/payload/resource::extracted-resource-api-resolution-loader":
        "micro-behaviors/mem/protect/modify::resource-process-protection-api-set",
    "objectives/command-and-control/backdoor/evasive::mismatched-encrypted-resource-shell-loader":
        "micro-behaviors/process/create/shellexec::resource-shellexecute-debugger-api-set",
    "well-known/malware/virus/expiro::expiro-high-entropy-rsrc-pe-parser-infector":
        "micro-behaviors/data/format/pe-parser::high-entropy-resource-pe-validation-api-set",
    "objectives/evasion/masquerade/brand/installer::yandex-installer-version-resource":
        "metadata/binary/resource/identity::yandex-installer-resource-label",
    "objectives/evasion/masquerade/brand/installer::yandex-product-version-resource":
        "metadata/binary/resource/identity::yandex-product-version-resource-label",
    FD + "ruby-stdout-reopen": FD + "ruby-output-stream-reopen",
}


def read_report(path):
    result = json.loads(path.read_text().splitlines()[0])
    return result.get("raw", result)


def traits(file):
    return {t["id"]: t for t in file.get("traits", [])}


def compare(before, after):
    previous = {f["id"]: f for f in before["files"]}
    current = {f["id"]: f for f in after["files"]}
    assert previous.keys() == current.keys(), "archive member coverage changed"
    changes = []
    for file_id, old_file in previous.items():
        old, new = traits(old_file), traits(current[file_id])
        for trait_id, trait in old.items():
            target = MOVES.get(trait_id, trait_id)
            assert target in new, (file_id, "lost", trait_id)
            expected = 3 if trait_id in list(MOVES)[:4] else trait["crit"]
            assert new[target]["crit"] == expected, (file_id, target, "severity")
        extra = new.keys() - {MOVES.get(t, t) for t in old}
        assert extra <= {SHUTDOWN}, (file_id, "unexpected consumer change", extra)
        changes.append({"file_id": file_id, "risk_before": old_file.get("risk"),
                        "risk_after": current[file_id].get("risk"), "added": sorted(extra)})
    return changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", type=Path)
    parser.add_argument("--storm", type=Path, help="Original outer StormAttack sample")
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    paths = sorted(HERE.glob("*.rb"))
    with tempfile.TemporaryDirectory(prefix="native-ruby-review-") as temp:
        if args.storm:
            source = args.storm.read_bytes()
            assert b"ExitWindowsEx" in source
            control = Path(temp) / "without-shutdown-api.exe"
            control.write_bytes(source.replace(b"ExitWindowsEx", b"ExitWindowsEy"))
            paths.append(control)
        command = [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--json"]
        output = subprocess.run(command + [str(p) for p in paths], check=True,
                                text=True, capture_output=True).stdout
        reports = {}
        for line in output.splitlines():
            report = json.loads(line)
            reports[Path(report["files"][0]["path"]).name] = report
        for name in ["streams.rb", "error-stream.rb", "global-streams.rb"]:
            found = traits(reports[name]["files"][0])
            assert found[SHELL]["crit"] == 5, name
            assert FD + "ruby-stdin-reopen" in found, name
            assert FD + "ruby-output-stream-reopen" in found, name
        log = traits(reports["log-streams.rb"]["files"][0])
        assert FD + "ruby-output-stream-reopen" in log
        assert not any(t["crit"] >= 4 for t in log.values()), "ordinary log redirection"
        for name in ["quoted-streams.rb", "unrelated-stream.rb"]:
            found = traits(reports[name]["files"][0])
            assert not any(t in found for t in [FD + "ruby-stdin-reopen",
                           FD + "ruby-output-stream-reopen", SHELL]), name
        if args.storm:
            found = {t["id"] for f in reports["without-shutdown-api.exe"]["files"]
                     for t in f.get("traits", [])}
            assert SHUTDOWN not in found
            assert "objectives/impact/dos/attack/flood::native-raw-udp-burst-flood" in found
            assert "objectives/command-and-control/remote-command/tasking::packet-flood-download-launch-control" in found
    result = {"ruby_controls": 6, "shutdown_control": bool(args.storm)}
    if args.evidence_dir:
        evidence = args.evidence_dir
        result["samples"] = [compare(read_report(evidence / f"before-{i}.json"),
                                     read_report(evidence / f"after-{i}.json")) for i in range(3)]
        result["external_controls"] = [compare(read_report(evidence / f"control-before-{i}.json"),
                                               read_report(evidence / f"control-after-{i}.json"))
                                       for i in range(3)]
    if args.record:
        args.record.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
