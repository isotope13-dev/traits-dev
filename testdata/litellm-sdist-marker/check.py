#!/usr/bin/env python3
"""Keep incident indicators separate from proof of payload execution.

Creates inert controls in a temporary directory; never imports sample code.
The October attribution and sdist/wheel distinction are documented at:
https://opensourcemalware.com/blog/litellm-1-107-0-pypi-wheel-contains-a-credential-stealer-and-persistent-python-backdoor
https://safedep.io/litellm-pypi-compromise-credential-stealer-backdoor/
"""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        value, end = decoder.raw_decode(text)
        yield value
        text = text[end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--sample-manifest", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    prefix = "well-known/malware/stealer/privcollect::"
    generic = "metadata/build/maturin::maturin-wheel-data-directory"
    marker = prefix + "maturin-cook-data-directory"
    build = prefix + "litellm-cook-build-marker"

    with tempfile.TemporaryDirectory(prefix="litellm-sdist-controls-") as work:
        work = Path(work)
        cases = []
        for name, package, value, required, forbidden in (
            ("incident", "litellm", 'data = "cook"', {generic, marker, build}, set()),
            ("other-package", "example", 'data = "cook"', {generic, marker}, {build}),
            ("renamed-data", "litellm", 'data = "assets"', {generic}, {marker, build}),
            ("absent", "litellm", "", set(), {generic, marker, build}),
            ("comment", "litellm", '# data = "cook"', set(), {generic, marker, build}),
        ):
            path = work / name / "pyproject.toml"
            path.parent.mkdir()
            path.write_text('[project]\nname = "' + package + '"\n'
                            '[build-system]\nbuild-backend = "maturin"\n'
                            '[tool.maturin]\n' + value + '\n')
            cases.append((name, path, required, forbidden))

        markers = work / "markers.py"
        markers.write_text('LABEL = "privcollect"\nURL = "http://www.litellm.dev/healthcheck"\n')
        cases.append(("indicator-text", markers,
                      {prefix + "privcollect-litellm-dev-markers"}, set()))

        wheel = work / "example-1.0-py3-none-any.whl"
        with zipfile.ZipFile(wheel, "w") as archive:
            archive.writestr("example-1.0.dist-info/METADATA",
                             "Metadata-Version: 2.1\nName: example\nVersion: 1.0\n")
            archive.writestr("example-1.0.data/purelib/cook.pth", "import cook\n")
            archive.writestr("example-1.0.data/purelib/cook.py", 'VALUE = "ordinary library"\n')
            archive.writestr("example-1.0.data/purelib/sitecustomize.py", "pass\n")
        cases.append(("startup-indicators", wheel,
                      {prefix + "litellm-wheel-startup-markers"}, set()))

        if args.sample_manifest:
            cases.append(("original-sdist-manifest", args.sample_manifest,
                          {generic, marker, build}, set()))

        for name, path, required, forbidden in cases:
            result = subprocess.run(
                [args.cleave, "--traits-dir", str(root), "--format", "json", "analyze", str(path)],
                check=True, capture_output=True, text=True,
            )
            findings = [trait for doc in documents(result.stdout)
                        for file in doc.get("files", []) for trait in file.get("traits", [])]
            ids = {trait["id"] for trait in findings}
            assert required <= ids, (name, "missing", sorted(required - ids))
            assert not forbidden & ids, (name, "unexpected", sorted(forbidden & ids))
            assert not [trait for trait in findings if trait.get("crit", 0) >= 4], (
                name, "indicators alone must not convict",
                [(trait["id"], trait["crit"]) for trait in findings if trait.get("crit", 0) >= 4],
            )
            assert not any("/teampcp::" in item for item in ids), (name, "incorrect actor attribution")
            print("PASS", name)
        print(str(len(cases)) + " focused controls passed")


if __name__ == "__main__":
    main()
