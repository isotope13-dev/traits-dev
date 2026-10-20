"""Regression controls for response output destination and argv placement."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else "cleave", "--traits-dir", str(root),
     "--json", *[str(p) for p in sorted(fixtures.glob("*.py"))
                 if p.name != "check.py"]],
    capture_output=True, text=True, check=True,
)
assert not result.stderr.strip(), result.stderr
reports = {}
for line in result.stdout.splitlines():
    for report in json.loads(line)["files"]:
        reports[Path(report["path"]).name] = {t["id"] for t in report["traits"]}

file_write = "micro-behaviors/fs/write/file/response-body::python-write-response-read"
stream_write = "micro-behaviors/process/io/stream::python-response-read-to-write"
web_write = "micro-behaviors/fs/write/content::file-write-near-public-web-script-path"
for name, ids in reports.items():
    expects_file = name in {"file-with.py", "file-inline.py", "file-assigned.py", "both.py"}
    expects_stream = name not in {"argv.py", "unrelated-write.py"}
    assert (file_write in ids) == expects_file, (name, "file destination", ids)
    assert (stream_write in ids) == expects_stream, (name, "stream transfer", ids)
    if name in {"stdout.py", "buffer.py", "other-handle.py", "unrelated-write.py"}:
        assert not any(t.startswith("micro-behaviors/fs/write/") for t in ids), (name, ids)
    if name in {"stdout.py", "both.py"}:
        assert (web_write in ids) == (name == "both.py"), (name, ids)
    assert not any("::sys-argv" in t and "/os/sysinfo/" in t for t in ids), (name, ids)

argv = reports["argv.py"]
assert "micro-behaviors/process/argument/positional::python-sys-argv-first-positional" in argv
assert "micro-behaviors/process/argument/positional::python-sys-argv-second-positional" in argv
assert len(reports) == 9, reports.keys()
print(f"Passed {len(reports)} response-destination and argument controls")
