"""Static matcher controls; never imports or executes the fixtures."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
ENGINE = os.environ.get("CLEAVE", "cleave")
MARKER = "micro-behaviors/fs/path/app-data::completion-marker-path"
FD_TEXT = "micro-behaviors/fs/proc/info/path::self-fd-directory-reference"
FD_LITERAL = "micro-behaviors/fs/proc/info/path::self-fd-path-literal"
SETTER = "micro-behaviors/data/property/assign::python-set-target-call"
CANCEL = "metadata/file/function::python-cancel-scheduled-definition"
LONG = "metadata/file/profile/string-population::python-string-at-least-100k"


def check(case):
    path, present, absent = case
    result = subprocess.run(
        [ENGINE, "--traits-dir", str(ROOT), "--format", "json", str(path)],
        text=True, capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    matched = {trait["id"] for file in report["files"] for trait in file.get("traits", [])}
    assert set(present) <= matched, (path, set(present) - matched, result.stderr)
    assert not set(absent) & matched, (path, set(absent) & matched)
    return path.name


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="_controls-", dir=HERE) as folder:
        folder = Path(folder)
        large = folder / "large.py"
        small = folder / "small.py"
        large.write_text('UI = "' + "x" * 100001 + '"\n')
        small.write_text('UI = "' + "x" * 99999 + '"\n')
        cases = [
            (HERE / "translation-keys.py", [], [MARKER, SETTER]),
            (HERE / "completion-files.py", [MARKER], [FD_TEXT, FD_LITERAL]),
            (HERE / "ordinary-operations.py", [FD_TEXT, FD_LITERAL, SETTER, CANCEL], [MARKER]),
            (large, [LONG], []),
            (small, [], [LONG]),
        ]
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            for name in pool.map(check, cases):
                print("PASS", name, flush=True)
