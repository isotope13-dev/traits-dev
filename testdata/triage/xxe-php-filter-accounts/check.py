"""Check PHP-filter XXE targets and trace expansion using synthetic data only."""
import argparse
import base64
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import xml.parsers.expat as expat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--live-dir", type=Path, required=True,
                    help="Scratch directory outside test paths for live payload checks")
args = parser.parse_args()
args.live_dir.mkdir(parents=True, exist_ok=True)
cases = json.loads((HERE / "cases.json").read_text())["fixtures"]

# Existing test-tree suppressors intentionally suppress hostile findings. Check
# live copies too, so the executable-payload branch is actually exercised.
with tempfile.TemporaryDirectory(prefix="xxe-", dir=args.live_dir) as directory:
    paths = []
    for case in cases:
        path = Path(directory) / Path(case["path"]).name
        shutil.copyfile(ROOT / case["path"], path)
        paths.append(path)
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", *map(str, paths)],
        capture_output=True, text=True, check=True,
    )
    decoder = json.JSONDecoder()
    remaining = result.stdout.lstrip()
    files = {}
    while remaining:
        document, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for file in document["files"]:
            files[Path(file["path"]).name] = file
    assert len(files) == len(cases), result.stderr
    for case in cases:
        name = Path(case["path"]).name
        traits = {trait["id"] for trait in files[name]["traits"]}
        assert set(case["matched"]) <= traits, (name, "missing", traits)
        assert not set(case["not_matched"]) & traits, (name, "unexpected", traits)

# Model a PHP-capable entity resolver without reading any real file or making
# a request. The SYSTEM URI selects only an entry from this in-memory map.
for name, resource in [("passwd.xml", "/etc/passwd"),
                       ("shadow.xml", "/etc/shadow")]:
    requests = []
    output = []
    source = {resource: b"SYNTHETIC_ACCOUNT_RECORD"}
    xml = expat.ParserCreate()
    xml.CharacterDataHandler = output.append

    def resolve(context, base, system, public):
        requests.append(system)
        assert system.startswith("php://filter/")
        assert "convert.base64-encode/resource=" in system
        path = system.split("/resource=", 1)[1]
        child = xml.ExternalEntityParserCreate(context)
        child.CharacterDataHandler = output.append
        child.Parse(base64.b64encode(source[path]), True)
        return 1

    xml.ExternalEntityRefHandler = resolve
    xml.Parse((HERE / name).read_bytes(), True)
    assert len(requests) == 1, requests
    assert base64.b64encode(source[resource]).decode() in "".join(output)

print(f"Passed {len(cases)} live trait cases and 2 in-memory expansion traces")
