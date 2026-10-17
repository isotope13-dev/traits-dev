#!/usr/bin/env python3
"""Check shared WinRT exports and JSON bytecode reference boundaries."""
import argparse
import json
import marshal
from pathlib import Path
import py_compile
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    repo = here.parents[2]
    loads = "micro-behaviors/data/parse/json::json-loads-pyc-name"
    dumps = "micro-behaviors/data/serialize/json::json-dumps-pyc-name"
    codec = "micro-behaviors/data/codec::python-json-transform-reference"
    fields = {"micro-behaviors/data/format/json::" + name + "-field"
              for name in ["file-path", "local-path", "server-path", "executed", "last-access", "command"]}
    factory = "micro-behaviors/os/com/class-factory::dll-get-activation-factory-export"
    retired = "well-known/app/infrastructure/windows-text-input-formatter::timf-dll-get-activation-factory"
    fixtures = {
        "json-loads": ("import json\nvalue = json.loads(payload)\n", {loads}),
        "json-dumps": ("import json\nvalue = json.dumps(payload)\n", {dumps}),
        "pickle-loads": ("import pickle\nvalue = pickle.loads(payload)\n", set()),
        "marshal-loads": ("import marshal\nvalue = marshal.loads(payload)\n", set()),
        "pickle-dumps": ("import pickle\nvalue = pickle.dumps(payload)\n", set()),
        "download-path": ('value = "Downloads"\n', set()),
        "json-download-path": ('import json\nvalue = "Downloads"\n', set()),
        "plain-variable-names": (
            'file_path = local_path = server_path = executed = last_access = command = None\n', set()),
        "json-field-keys": (
            'value = \'{"file_path":"x","local_path":"x","server_path":"x",'
            '"executed":false,"last_access":0,"command":"read"}\'\n', fields),
    }
    with tempfile.TemporaryDirectory(prefix="winrt-json-bytecode-") as temporary:
        root = Path(temporary)
        expected = {}
        for name, (source, matches) in fixtures.items():
            path = root / (name + ".py")
            path.write_text(source)
            py_compile.compile(str(path), cfile=str(path.with_suffix(".pyc")),
                               dfile="fixture.py", doraise=True)
            expected[name + ".pyc"] = matches
        # Marshal version 0 uses four-byte string lengths rather than the
        # short ASCII records written by current CPython defaults.
        for name in ["json-loads", "json-dumps"]:
            source, matches = fixtures[name]
            header = (root / (name + ".pyc")).read_bytes()[:16]
            legacy = root / (name + "-legacy.pyc")
            legacy.write_bytes(header + marshal.dumps(compile(source, "fixture.py", "exec"), 0))
            expected[legacy.name] = matches
        for name, matches in [("winrt.pe", {factory}), ("reference-only.pe", set())]:
            shutil.copyfile(here / name, root / name)
            expected[name] = matches
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(repo), "--format", "json", "analyze", str(root)],
            text=True, capture_output=True, check=True,
        )
        remaining = result.stdout
        decoder = json.JSONDecoder()
        seen = {}
        while remaining.strip():
            report, end = decoder.raw_decode(remaining.lstrip())
            remaining = remaining.lstrip()[end:]
            for file in report.get("files", []):
                name = Path(file["path"]).name
                if name in expected:
                    ids = {trait["id"] for trait in file.get("traits", [])}
                    observed = ids & ({loads, dumps, codec, factory, retired} | fields)
                    assert observed == expected[name], (name, observed, expected[name])
                    assert not any(i.startswith("well-known/app/infrastructure/windows-text-input-formatter::")
                                   for i in ids), (name, "unrelated component identity")
                    seen[name] = observed
        assert seen.keys() == expected.keys(), ("missing results", expected.keys() - seen.keys())
        print("PASS: {} controls (Python bytecode {}, shared WinRT export)".format(
            len(seen), __import__("sys").version.split()[0]))


if __name__ == "__main__":
    main()
