"""Check DTD construction, expansion, constant URLs, and inert comments."""
import json
import os
from pathlib import Path
import subprocess
import xml.parsers.expat as expat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())["fixtures"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *[str(ROOT / c["path"]) for c in cases]],
    text=True, capture_output=True,
)
remaining = result.stdout.lstrip()
decoder = json.JSONDecoder()
files = {}
while remaining:
    document, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in document["files"]:
        files[Path(file["path"]).name] = file
assert len(files) == len(cases), (result.returncode, result.stderr)
for case in cases:
    file = files[Path(case["path"]).name]
    traits = {t["id"] for t in file["traits"]}
    assert set(case["matched"]) <= traits, (case["case_id"], "missing")
    assert not set(case["not_matched"]) & traits, (case["case_id"], "unexpected")
    if case["case_id"] in {"comment-only.dtd", "ordinary-nested.dtd"}:
        assert all(t["crit"] < 4 for t in file["traits"]), case["case_id"]

# Resolve everything in memory: never use an HTTP or local-file resolver.
for name, expected in [("callback.dtd", True), ("decimal-escape.dtd", True),
                       ("declaration-only.dtd", False)]:
    requests = []
    payload = (HERE / name).read_bytes()

    def configure(parser):
        parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_ALWAYS)

        def external(context, base, system, public):
            requests.append(system)
            if system == "memory://payload.dtd":
                child = parser.ExternalEntityParserCreate(context)
                configure(child)
                child.Parse(payload, True)
            return 1

        parser.ExternalEntityRefHandler = external

    parser = expat.ParserCreate()
    configure(parser)
    parser.Parse(b'<!DOCTYPE r SYSTEM "memory://payload.dtd" '
                 b'[<!ENTITY % content "SYNTHETIC_SECRET_927">]><r/>', True)
    sent = any("SYNTHETIC_SECRET_927" in url for url in requests)
    assert sent == expected, (name, requests)
print(f"Passed {len(cases)} trait cases and 3 in-memory expansion traces")
