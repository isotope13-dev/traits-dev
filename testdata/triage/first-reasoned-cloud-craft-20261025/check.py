"""Check saved static analyses; never execute a specimen.

Usage: python3 check.py /absolute/path/to/fallout-review
"""
import json
from pathlib import Path
import sys

reports = Path(sys.argv[1])
here = Path(__file__).resolve().parent
prefix = str(here.relative_to(here.parents[2])) + "/"
renames = {
    "micro-behaviors/communications/socket/state-connect::nwconnection-start-source":
        "metadata/lang/source/syntax/call/invocation::swift-queued-start-call-text",
    "micro-behaviors/process/interpreter/reflection/resolve::assembly-load-buffer":
        "micro-behaviors/process/interpreter/reflection/resolve::assembly-load-variable-argument",
    "micro-behaviors/communications/http/upload::shell-curl-form-file-upload":
        "micro-behaviors/communications/http/upload::curl-form-file-attachment",
}
chmod = "micro-behaviors/fs/chmod/executable/mode::chmod-exec-literal-target"
read = "micro-behaviors/fs/read/file/full::csharp-http-response-file-path-read"
collection = "objectives/collection/file-targeting/remote-list::cloud-code-task-selected-file-read"
exfil = "objectives/exfiltration/stealer/file::cloud-task-selected-file-upload"
monitor = "micro-behaviors/network/status::swift-nwpathmonitor-construction"
download = "micro-behaviors/communications/http/download/handler::swift-urlsession-download-task-call"
upload = "micro-behaviors/communications/http/upload::swift-urlsession-upload-task-call"
memory = "micro-behaviors/mem/read/arbitrary::swift-mach-vm-read-overwrite-call"


def objects(path):
    text = path.read_text()
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        report, length = decoder.raw_decode(text)
        text = text[length:]
        yield report


def files(path):
    return {f["path"]: f for report in objects(path) for f in report["files"]}


def traits(file, rename=False):
    return {(renames.get(t["id"], t["id"]) if rename else t["id"]): t["crit"]
            for t in file.get("traits", [])}


def losses(old, new, allowed):
    result = []
    for path, file in old.items():
        assert path in new, path
        assert file["sha"] == new[path]["sha"], path
        before, after = traits(file, True), traits(new[path])
        for id, severity in before.items():
            if after.get(id, -1) < severity:
                assert id in allowed, (path, id, severity, after.get(id))
                result.append({"path": path, "id": id, "criticality": severity})
    return result


before = files(reports / "retention.before.json")
after = files(reports / "controls.final.jsonl")
assert not losses(before, after, set())

positive = {
    "http-path-read.cs": read,
    "network-monitor.swift": monitor,
    "native-download.swift": download,
    "native-upload.swift": upload,
    "self-memory-read.swift": memory,
    "permission-command.js": chmod,
    "permission-busybox.sh": chmod,
    "curl-form-file.sh": "micro-behaviors/communications/http/upload::curl-form-file-attachment",
}
for name, id in positive.items():
    assert id in traits(after[prefix + name]), (name, id)
for name in ["fixed-path.cs", "reassigned-path.cs", "documentation.cs"]:
    ts = traits(after[prefix + name])
    assert read not in ts and collection not in ts, name
assert not {monitor, download, upload, memory} & traits(after[prefix + "documentation.swift"]).keys()
assert chmod not in traits(after[prefix + "permission-prose.js"])
assert "micro-behaviors/communications/http/upload::curl-form-file-attachment" not in traits(after[prefix + "curl-form-text.sh"])

chmod_losses = losses(files(reports / "chmod.before.jsonl"),
                      files(reports / "chmod.after.jsonl"), {chmod})
assert len(chmod_losses) == 4, chmod_losses
assert not losses(files(reports / "curl-form.before.jsonl"),
                  files(reports / "curl-form.after.jsonl"), set())

summary = {"samples": [], "fixture_files": len(after),
           "chmod_control_files": len(files(reports / "chmod.after.jsonl")),
           "curl_form_control_files": len(files(reports / "curl-form.after.jsonl")),
           "chmod_control_losses": chmod_losses,
           "retained_attack_findings": True, "renames": renames}
for name in ["direct", "different", "craft"]:
    old = next(objects(reports / (name + ".before.json")))
    new = next(objects(reports / (name + ".review-final.json")))
    old_files = {f["path"]: f for f in old["raw"]["files"]}
    new_files = {f["path"]: f for f in new["raw"]["files"]}
    assert old_files.keys() == new_files.keys(), name
    lost = losses(old_files, new_files, {chmod} if name == "craft" else set())
    root_old = old["raw"]["files"][0]
    root_new = new["raw"]["files"][0]
    a, b = traits(root_old), traits(root_new)
    if name == "craft":
        assert all(t["crit"] < 4 for f in new_files.values() for t in f.get("traits", []))
        assert len(lost) == 2, lost
    else:
        assert collection in b and read in b, name
        assert (exfil in b) == (name == "direct"), name
    def counts(ts):
        return {"hostile": sum(v == 5 for v in ts.values()),
                "suspicious": sum(v == 4 for v in ts.values()),
                "notable": sum(v == 3 for v in ts.values())}
    summary["samples"].append({
        "name": name, "path": root_new["path"], "sha256": root_new["sha"],
        "verdict": "BENIGN" if name == "craft" else "MALICIOUS",
        "analyzed_files": len(new_files),
        "before": counts(a), "after": counts(b),
        "ml_probability_before": old["ml"]["prob"],
        "ml_probability_after": new["ml"]["prob"],
        "ml_level_before": old["ml"]["lvl"],
        "ml_level_after": new["ml"]["lvl"],
        "losses": lost,
        "added": sorted(b.keys() - {renames.get(id, id) for id in a}),
    })
(here / "review.json").write_text(json.dumps(summary, indent=2) + "\n")
print(f"Passed {len(after)} source controls and {summary['chmod_control_files']} chmod controls")
for sample in summary["samples"]:
    print(sample["name"], sample["verdict"], sample["before"], "->", sample["after"],
          "ML", sample["ml_probability_before"], "->", sample["ml_probability_after"])
