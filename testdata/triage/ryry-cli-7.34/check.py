"""Static controls for remote-worker classification and misleading Python facts.

Only the scanner runs. Generated source and archive members are never imported
or executed. Run with --out /tmp/ryry-controls --cleave /path/to/cleave.
"""
import argparse
import ast
import base64
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[3]
FORK = "micro-behaviors/process/fork/clone::python-fork-child-zero-test"
PROXY = "micro-behaviors/communications/proxy/config::urllib3-proxy-manager-construction"
VERSION = "metadata/package/versioning/sentinel::pypi-version-zero"
PROCESS = "micro-behaviors/process/create/subprocess::python-task-api-process-context"
PROFILE = "micro-behaviors/communications/http/telemetry::python-task-api-hardware-profile-context"
IDENTITY = "well-known/dual-use/remote-admin/ryry-cli::ryry-cli-remote-task-worker"
PIP = "micro-behaviors/process/argument/subcommand::python-interpreter-pip-argv"
SELECTED = {FORK, PROXY, VERSION, PROCESS, PROFILE, IDENTITY, PIP}
RETIRED = {
    "objectives/command-and-control/backdoor/tasking/command-polling::python-remote-widget-task-worker",
    "objectives/command-and-control/backdoor/tasking/command-polling::python-remote-process-task-worker",
    "objectives/command-and-control/backdoor/tasking/command-polling::python-remote-profile-task-worker",
    "well-known/malware/backdoor/ryry-cli::ryry-cli-remote-task-worker",
    "well-known/malware/backdoor/ryry-cli::ryry-cli-host-profile-exfil",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cleave", default=os.environ.get("CLEAVE", "cleave"))
    parser.add_argument("--wheel", type=Path, help="Optional wheel integrity and parse-only checks")
    args = parser.parse_args()
    inputs = args.out / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    cases = []

    def source(name, content, expected):
        path = inputs / name
        path.write_text(content)
        cases.append((path, set(expected)))

    for index, (code, expected) in enumerate([
        ('__version__ = "0.0.0"\n', {VERSION}),
        ("version='0.0'\n", {VERSION}),
        ('__version__="7.34"\n', set()),
        ('def capacity():\n    version = "0.0"\n    return version\n', set()),
        ('widget_version = "0.0"\n', set()),
        ('previous_version = "0.0.0"\n', set()),
        ('def fallback():\n    __version__="0.0.0"\n', set()),
        ('# __version__="0.0.0"\n', set()),
        ('__version__="0.0.1"\n', set()),
        ('class State:\n    version="0.0.0"\n', set()),
        ('documentation="""\n__version__="0.0.0"\n"""\n', set()),
    ]):
        source(f"version-{index}.py", code, expected)

    for name in ("pid", "child", "worker_id"):
        for wrapped in (False, True):
            for check in (f"{name} == 0", f"not {name}"):
                code = f"{name} = os.fork()\nif {check}:\n    pass\n"
                if wrapped:
                    code = "def worker():\n" + "".join("    " + line + "\n" for line in code.splitlines())
                source(f"fork-{len(cases)}.py", "import os\n" + code, {FORK})
    for code in (
        "if pid:\n    pass\n",
        "if old_pid == 0:\n    pass\n",
        "if not pid:\n    pass\n",
        "pid = os.getpid()\nif pid == 0:\n    pass\n",
        "child = os.fork()\nif other_pid == 0:\n    pass\n",
        "pid = os.fork()\nif pid != 0:\n    pass\n",
        "pid = os.fork()\nif pid >= 0:\n    pass\n",
        "pid = os.fork()\nif pid == 1:\n    pass\n",
        "pid = os.fork()\npid = os.getpid()\nif pid == 0:\n    pass\n",
        "def a():\n    pid = os.fork()\ndef b():\n    if pid == 0:\n        pass\n",
    ):
        source(f"pid-condition-{len(cases)}.py", code, set())

    for code, expected in (
        ('import urllib3\np = urllib3.ProxyManager("https://relay.example")\n', {PROXY}),
        ('p = requests.packages.urllib3.ProxyManager("https://relay.example")\n', {PROXY}),
        ('from ryry.proxy.manager import ProxyManager\np = ProxyManager()\n', set()),
        ('p = custom.ProxyManager()\n', set()),
        ('class ProxyManager:\n    pass\np = ProxyManager()\n', set()),
        ('name="urllib3.ProxyManager"\n', set()),
    ):
        source(f"proxy-{len(cases)}.py", code, expected)

    for code, expected in (
        ('command=[sys.executable, "-m", "pip", *args]\n', {PIP}),
        ("command = [ sys.executable, '-m', 'pip', 'install', url ]\n", {PIP}),
        ('command=[sys.executable, "-m", "json.tool", *args]\n', set()),
        ('command=[sys.executable, "-c", "pip", *args]\n', set()),
        ('command=[other.executable, "-m", "pip", *args]\n', set()),
        ('command=["-m", sys.executable, "pip"]\n', set()),
        ('documentation="[sys.executable, \'-m\', \'pip\', *args]"\n', set()),
    ):
        source(f"pip-argv-{len(cases)}.py", code, expected)

    api = '''import requests
def GetTask(taskUUID):
    return requests.get("https://worker.example/jobs").json()
def TaskNotify(taskUUID, result):
    return requests.post("https://worker.example/result", json=result)
'''
    process = '''import sys, subprocess
command = [sys.executable, cmd, "--run", inputArgs, "--out", outArgs]
subprocess.Popen(command)
'''
    profile = '''def _aigc_post(value):
    return value
resources = {"cpu": {}, "memory": {}, "disk": {}, "gpu": {}}
'''
    source("worker.py", api + process + profile, {PROCESS, PROFILE})
    source("task-names-only.py", "GetTask = None\ntaskUUID = ''\nTaskNotify = None\n", set())
    source("http-only.py", api, set())
    source("launch-only.py", process, set())

    def archive(name, members, expected):
        path = inputs / name
        with zipfile.ZipFile(path, "w") as wheel:
            for member, content in members.items():
                wheel.writestr(member, content)
        cases.append((path, set(expected)))

    # Preserve archive co-occurrence without pretending it proves value flow.
    archive("distributed.whl", {"worker/api.py": api, "worker/run.py": process,
                               "worker/profile.py": profile}, {PROCESS, PROFILE})
    archive("incomplete.whl", {"worker/api.py": api, "worker/profile.py": profile}, {PROFILE})
    # Renaming members or the collector's wheel name changes no behavior.
    archive("renamed.whl", {"a/x.py": api, "b/y.py": process, "z.py": profile}, {PROCESS, PROFILE})
    ryry_api = api.replace("worker.example", "api.dalipen.com").replace("/jobs", "/aigc/task/getTask")
    archive("identity.whl", {"ryry_cli-7.34.dist-info/METADATA": "Metadata-Version: 2.4\nName: ryry-cli\nVersion: 7.34\n\n",
                            "a.py": ryry_api, "b.py": process}, {PROCESS, IDENTITY})

    result = subprocess.run(
        [args.cleave, "--traits-dir", str(ROOT), "--no-update-check", "--format", "jsonl", str(inputs)],
        capture_output=True, text=True, timeout=600, check=True,
        env={**os.environ, "CLEAVE_SKIP_CACHE": "1", "RAYON_NUM_THREADS": "2"},
    )
    (args.out / "scan.jsonl").write_text(result.stdout)
    reports = {}
    for line in result.stdout.splitlines():
        for report in json.loads(line).get("files", []):
            if "!!" not in report["path"]:
                reports[Path(report["path"]).name] = report
    results = []
    for path, expected in cases:
        report = reports[path.name]
        observed = {t["id"] for t in report.get("traits", [])}
        assert not observed & RETIRED, (path.name, sorted(observed & RETIRED))
        assert observed & SELECTED == expected, (path.name, sorted(observed & SELECTED), sorted(expected))
        for trait in report.get("traits", []):
            if trait["id"] in SELECTED:
                assert trait["crit"] == 3, (path.name, trait)
        results.append({"case": path.name, "passed": True, "matches": sorted(observed & SELECTED)})
    (args.out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"Passed {len(results)} static classification, scope, version, proxy and fork controls")
    if args.wheel:
        with zipfile.ZipFile(args.wheel) as wheel:
            names = wheel.namelist()
            assert len(names) == len(set(names)), "duplicate wheel members"
            assert all(not Path(name).is_absolute() and ".." not in Path(name).parts for name in names)
            record = next(name for name in names if name.endswith(".dist-info/RECORD"))
            verified = 0
            records = list(csv.reader(io.StringIO(wheel.read(record).decode())))
            assert {row[0] for row in records} == set(names), "unrecorded wheel member"
            for name, digest, size in records:
                if not digest:
                    assert name == record
                    continue
                algorithm, encoded = digest.split("=", 1)
                assert algorithm == "sha256"
                content = wheel.read(name)
                actual = base64.urlsafe_b64encode(hashlib.sha256(content).digest()).decode().rstrip("=")
                assert encoded == actual and len(content) == int(size), name
                verified += 1
            sources = [name for name in names if name.endswith(".py")]
            for name in sources:
                ast.parse(wheel.read(name), filename=name)
        integrity = {"members": len(names), "record_hashes_verified": verified,
                     "python_sources_parsed_without_execution": len(sources)}
        (args.out / "wheel-integrity.json").write_text(json.dumps(integrity, indent=2) + "\n")
        print(json.dumps(integrity))


if __name__ == "__main__":
    main()
