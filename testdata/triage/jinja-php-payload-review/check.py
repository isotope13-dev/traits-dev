#!/usr/bin/env python3
"""Exercise payload signatures from neutral paths, without running payloads."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
REMOTE = "objectives/execution/interpreter/eval/remote::"
FORM = "micro-behaviors/communications/http/form::php-filename-parameter"
OLD = "micro-behaviors/communications/http/upload::escaped-php-upload-filename"
CHAIN = "objectives/execution/exploit/file-upload::php-shell-upload-execution-chain"
WEB = "objectives/command-and-control/backdoor/webshell/request/command::"


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        item, end = decoder.raw_decode(text)
        yield item
        text = text[end:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--scratch-root", type=Path, required=True)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(dir=args.scratch_root, prefix="payload-controls-") as tmp:
        temp = Path(tmp)
        copies = {
            "probe.json": "testdata/triage/advisory-storm-gx-first-review/jinja-payload.json",
            "reference.json": "testdata/triage/advisory-storm-gx-first-review/reference-payload.json",
            "carrier.html": "testdata/hostile/php-shell-upload-chain-controls.html",
            "csrf.html": "testdata/stranded-member-controls/csrf-shell-upload-poc.html",
            "photo.html": "testdata/stranded-member-controls/credentialed-photo-uploader.html",
            "ssti.py": "testdata/triage/security-tool-examples/ssti.py",
            "advisory.json": "testdata/triage/advisory-storm-gx-first-review/GHSA-3f7w-p8vr-4v5f.json",
        }
        for name, source in copies.items():
            shutil.copyfile(ROOT / source, temp / name)
        controls = {
            "popen.json": {"template": "{{ cycler.__init__.__globals__.os.popen('id').read() }}"},
            "system.json": {"template": "{{ cycler.__init__.__globals__.os.system('id') }}"},
            "ordinary.json": {"template": "{{ user.name }}"},
            "reference-only.json": {"template": "{{ x.__init__.__globals__.os.popen }}"},
            "unrelated.json": {"template": "{{ user.name }}", "note": "os.popen('id')"},
        }
        for name, obj in controls.items():
            (temp / name).write_text(json.dumps(obj))
        (temp / "parameter.html").write_text(
            '<html><body><pre>filename="utility.php"</pre></body></html>\n')
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(ROOT), "--format", "json",
             *map(str, sorted(temp.iterdir()))], text=True, capture_output=True, check=True)
        files = [f for report in documents(result.stdout) for f in report["files"]]
        top = {Path(f["path"]).name: f for f in files if "##" not in f["path"]}
        def traits(name):
            return {t["id"]: t["crit"] for t in top[name].get("traits", [])}
        for name in ("probe.json", "reference.json"):
            actual = traits(name)
            assert actual[REMOTE + "jinja-template-code-execution"] == 5, (name, actual)
            assert actual[REMOTE + "jinja-json-os-command-sink"] == 4, (name, actual)
        assert traits("reference.json")[REMOTE + "fsspec-reference-jinja-code-execution"] == 5
        for name in ("popen.json", "system.json"):
            assert traits(name)[REMOTE + "jinja-json-os-command-sink"] == 4
        for name in ("ordinary.json", "reference-only.json", "unrelated.json", "advisory.json"):
            assert REMOTE + "jinja-json-os-command-sink" not in traits(name), (name, traits(name))
        assert REMOTE + "jinja-os-command-sink" in traits("ssti.py")
        for name in ("carrier.html", "csrf.html"):
            actual = traits(name)
            assert actual[FORM] == 3, (name, actual)
            assert actual[CHAIN] == 5, (name, actual)
            assert OLD not in actual
        for name in ("php-command-webshell", "php-tiny-system-request-webshell"):
            assert traits("carrier.html")[WEB + name] == 5
        assert FORM not in traits("photo.html")
        assert CHAIN not in traits("photo.html")
        parameter = traits("parameter.html")
        assert parameter[FORM] == 3
        assert CHAIN not in parameter
        assert not any(t.startswith("micro-behaviors/communications/http/upload::")
                       for t in parameter), parameter
        print(f"PASS: {len(top)} neutral-path inputs; attack coverage and benign near misses")


if __name__ == "__main__":
    main()
